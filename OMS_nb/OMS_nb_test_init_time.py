# from OMS import OrderManagementSystem
from OMS_beta import OrderManagementSystem, OrderManagementSystem_nbInit  ## beta version for testing and developing
import os
import pandas as pd
import time
import copy

import sys
sys.path.append(os.path.pardir)
import numpy as np
import matplotlib.pyplot as plt
from Strategies.AlmgrenChriss_EMQV import AlmgrenChriss_EMQV
from Strategies.TWAP import TWAP

# --------Data Index---------- #
colIdx_time = 0
colIdx_type = 1
colIdx_ID = 2
colIdx_size = 3
colIdx_prc = 4
colIdx_direc = 5

orderType_LO = 1
orderType_cancel = 2
orderType_MO = 4

# -----Simulation Set-Up------ #
qty_to_exec = 57000  # ~ 370000/6.5  # ADTV of AAPL from Jan. to Feb. 2017 = 3740336


class SimulationEnvironment:
    def __init__(self, read_OF_from, read_LOB_from, start_T=10 * 3600, T=3600, N=100):
        '''
        Input:
        start_T, T: in seconds
        '''
        self.start_T = start_T  # seconds since midnight
        self.end_T = start_T + T
        self.T = T  # in seconds
        self.N = N
        self.Delta_t = T/N  # in seconds
        self.Delta_t_year = self.Delta_t / (250 * 6.5 * 3600) # in year

        data_OF = pd.read_csv(read_OF_from, header=None,
                              names=['Time', 'Type', 'OrderID', 'Size', 'Price', 'Direction'])
        ## Find the OF in [start_T, start_T + T]
        data_OF = data_OF[(data_OF['Time'] >= self.start_T) & (data_OF['Time'] <= self.start_T + self.T)]
        data_OF = data_OF[(data_OF['Type'] != 5) & (data_OF['Type'] != 7)]
        ## Type 5 is execution of hidden order, which does not affect LOB;
        ## Type 7 is trading halt indicator
        data_OF_idx0 = data_OF.index[0]
        self.data_OF = data_OF.values
        self.time = self.data_OF[0, colIdx_time]

        init_LOB = pd.read_csv(read_LOB_from, header=None, skiprows=data_OF_idx0, nrows=1).values[0].tolist()
        init_AskBook = []
        init_BidBook = []
        for i in range(len(init_LOB)):
            if i % 4 == 0:  # ask price
                init_AskBook.append(init_LOB[i])
            elif i % 4 == 1:  # ask size
                init_AskBook.append(init_LOB[i])
            elif i % 4 == 2:  # bid price
                init_BidBook.append(init_LOB[i])
            else:
                init_BidBook.append(init_LOB[i])

        self.OMS = OrderManagementSystem_nbInit(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook, init_len=10_000)
        ## Note: now all the price in OMS has not been divided by 1e4

        self.ref_price = (init_AskBook[0] + init_BidBook[0]) / 2 / 1e4
        self.ref_revenue = qty_to_exec * self.ref_price
        self.state = {
            "remaining_time": self.T,  # T = 1h = 3600s
            "remaining_shares": qty_to_exec,  # ~10% ADTV of AAPL / 6.5h
            "midPrice": (self.OMS.askPrice + self.OMS.bidPrice)/2
        }

        self.GH_x, self.GH_w = np.polynomial.hermite.hermgauss(deg=15)

    def reset_env(self, read_OF_from, read_LOB_from, start_T=10 * 3600, T=3600, N=100):
        self.__init__(read_OF_from, read_LOB_from, start_T, T, N)
        return self.state


    def reset_LOB(self, init_LOB_flatten, askPrice, bidPrice):
        self.OMS.reset_LOB(init_LOB_flatten=init_LOB_flatten, askPrice=askPrice, bidPrice=bidPrice)


    def handle_action(self, action):
        ## action: in shares
        qty_executed_this_time = 0
        exec_rev_this_time = 0
        for act in action:
            if act:  # action is not empty list
                order = np.array([0, act[0], 0, act[1], act[2], act[3]])  # Time, Type, Order ID, Size, Price, Direction
                exec_res = self.OMS.receive_order(orderFlow=order)
                if act[0] == orderType_MO:
                    # print(f"orderSize = {act[1]}")
                    exec_rev_this_time += exec_res / 1e4  # exec revenue (normal scale)
                    qty_executed_this_time += act[1]      # qty executed
        return exec_rev_this_time, qty_executed_this_time


    def step(self, action):
        # action: [mu, variance]
        done = False
        mu = action[0]  ## in percentage
        pi_var = action[1]

        qt = self.state['remaining_shares'] / qty_to_exec
        St = self.state['midPrice'] / 1e4

        if self.state['remaining_time'] <= self.Delta_t:  # liquidate all the remaining shares
            mu_shares = - self.state['remaining_shares']
            action_mu = [orderType_MO, abs(mu_shares), 0, 1 * (mu_shares <= 0) - 1 * (mu_shares > 0)]
            # action = [Type, Size, Price, Direction]
            dxt, qty_executed_this_time = self.handle_action(action=[action_mu])
            Delta_xt = dxt / qty_to_exec
            done = True

        else:  # not the last decision period
            if pi_var > 0:  # exploration
                # record the current order book:
                current_LOB = self.OMS.LOB.flatten()
                current_askPrice = copy.deepcopy(self.OMS.askPrice)
                current_bidPrice = copy.deepcopy(self.OMS.bidPrice)
                ######
                Delta_xt = 0
                for i in range(self.GH_x.shape[0]):
                    if i > 0:
                        self.reset_LOB(init_LOB_flatten=current_LOB, askPrice=current_askPrice, bidPrice=current_bidPrice)
                    ## immediate execution
                    nu = round((np.sqrt(2 * pi_var) * self.GH_x[i] + mu) * self.Delta_t_year * qty_to_exec)
                    action_nu = [orderType_MO, min(abs(nu), self.state['remaining_shares']), 0, 1 * (nu <= 0) - 1 * (nu > 0)]
                    # action = [Type, Size, Price, Direction]
                    dxt, _ = self.handle_action(action=[action_nu])
                    Delta_xt += self.GH_w[i] * dxt

                Delta_xt = Delta_xt / np.sqrt(np.pi) / qty_to_exec
                self.reset_LOB(init_LOB_flatten=current_LOB, askPrice=current_askPrice, bidPrice=current_bidPrice)

            ## simulate S_{t + \Delta t} for mu
            mu_shares = round(mu * self.Delta_t_year * qty_to_exec)
            action_mu = [orderType_MO, min(abs(mu_shares), self.state['remaining_shares']), 0,
                         1 * (mu_shares <= 0) - 1 * (mu_shares > 0)]  # action = [Type, Size, Price, Direction]
            dxt, qty_executed_this_time = self.handle_action(action=[action_mu])
            if pi_var == 0:
                Delta_xt = dxt / qty_to_exec


        select_OF = self.data_OF[
            (self.data_OF[:, colIdx_time] > self.time) & (self.data_OF[:, colIdx_time] <= self.time + self.Delta_t)]
        if select_OF[-1, colIdx_time] == self.data_OF[-1, colIdx_time]:  # simulation ends
            done = True
        if select_OF.shape[0] == 0:
            # Two possibilities:
            # Case 1. The OF file has come to an end, meaning it is the end of the simulation period.
            # Case 2. It's before the end of the simulation but there's no OF during this period of time.
            if self.data_OF[-1, colIdx_time] <= self.time:  # Case 1
                done = True
            else:  # Case 2
                self.time += self.Delta_t
                self.state.update({
                    "remaining_time": self.end_T - self.time,
                    "remaining_shares": self.state['remaining_shares'] - qty_executed_this_time,
                    "midPrice": (self.OMS.askPrice + self.OMS.bidPrice)/2
                })
        else:
            self.OMS.receive_order(orderFlow=select_OF)

            self.time += self.Delta_t
            self.state.update({
                "remaining_time": self.end_T - self.time,
                "remaining_shares": self.state['remaining_shares'] - qty_executed_this_time,
                "midPrice": (self.OMS.askPrice + self.OMS.bidPrice)/2
            })

        St_Delta_qt = St * mu_shares / qty_to_exec
        Delta_St = (self.OMS.askPrice + self.OMS.bidPrice) / 2 / 1e4 - St
        qt_Delta_St = qt * Delta_St
        QV_penalty = -(Delta_xt + St_Delta_qt + qt_Delta_St) ** 2

        return Delta_xt, QV_penalty, self.state, done


def run_sim(file_dir, files_name, start_T, T, N, choose_agent, episodes, mode='training', save_result=False):
    '''
    start_T, T: in seconds
    '''
    RunningStartTime = time.perf_counter()
    num_training_file = len(files_name)

    ## init algo agent
    algo = choose_agent

    ## init simulator
    env = SimulationEnvironment(read_OF_from=file_dir + files_name[0]['file_OF'],
                                read_LOB_from=file_dir + files_name[0]['file_LOB'],
                                start_T=start_T,
                                T=T,
                                N=N)

    for episode in range(episodes):

        day_start = time.perf_counter()

        # if episode %10 == 0: print(episode)
        print(files_name[episode % num_training_file])

        # reset state and algos
        state = env.reset_env(read_OF_from=file_dir + files_name[episode % num_training_file]['file_OF'],
                              read_LOB_from=file_dir + files_name[episode % num_training_file]['file_LOB'],
                              start_T=start_T,
                              T=T,
                              N=N)
        algo.reset(S0_this_period=env.ref_price)
        done = False

        path_states = []
        path_rewards = []
        while not done:
            path_states.append(copy.deepcopy(state))

            ## execute the action(s)
            algo_mean_var, done_algo = algo.action(state)

            ## obtain the reward and the next state
            Delta_xt, QV_penalty, state, done_sim = env.step(action=algo_mean_var)

            path_rewards.append(Delta_xt + algo.Lambda * QV_penalty)

            if done_sim == True and done_algo == False:
                # Dump all the remaining shares to liquidate
                # action = [Type, Size, Price, Direction]
                print(f"Warning: sim is done but algo is not done!")
                algo_action = [orderType_MO, env.state['remaining_shares'], 0, 1]
                reward, _ = env.handle_action([algo_action])
                path_rewards.append(reward)
            # Problem warning:
            # Sim is done but algo is not
            done = done_algo or done_sim

        feature_list = []
        for state in path_states:
            feature = [0, 0, 0]
            for key, value in state.items():
                if key == 'remaining_time':
                    feature[0] = value / (250 * 6.5 * 3600)  # in years
                elif key == 'remaining_shares':
                    feature[1]= value / qty_to_exec  # in pct
                else:  # midPrice
                    feature[2] = value / 1e4
            feature_list.append(feature)

        feature_matrix = np.array(feature_list)  # list of lists to np.array (N x num_feat)
        path_rewards_np = np.array(path_rewards)
        reward_to_go = path_rewards_np.sum() - path_rewards_np.cumsum() + path_rewards_np

        if episode == 0:
            state_reward = np.concatenate((feature_matrix, reward_to_go.reshape(-1, 1)), axis=1)
        else:
            state_reward_this_time = np.concatenate((feature_matrix, reward_to_go.reshape(-1, 1)), axis=1)
            state_reward = np.concatenate((state_reward, state_reward_this_time), axis=0)

        print(f"day_run_time = {time.perf_counter() - day_start} sec.")

    result_pd = pd.DataFrame(state_reward)
    result_pd_col = ['remaining_time', 'remaining_shares', 'midPrice', 'Gt']
    result_pd.columns = result_pd_col
    if save_result:
        result_pd.to_csv(f"{choose_agent.name}_{file_dir[39:43]}_Lam{choose_agent.Lambda}_Zeta{choose_agent.zeta}_state_reward_{mode}_{round(start_T/3600)}_{round((start_T + T)/3600)}.csv")

    RunningTime = round(time.perf_counter() - RunningStartTime, 3)
    print(f"Running time: {RunningTime} sec for {episodes} episodes.")

    return result_pd


def train(file_dir, files_name, start_T, T, N, choose_agent, train_iteration, PATH_NUM, PE_iter_num, plot=True):
    '''
    start_T, T: in seconds
    '''
    # time for running program
    RunningStartTime = time.perf_counter()
    num_training_file = len(files_name)

    ## init algo agent
    algo = choose_agent

    ## init simulator
    env = SimulationEnvironment(read_OF_from=file_dir + files_name[0]['file_OF'],
                                read_LOB_from=file_dir + files_name[0]['file_LOB'],
                                start_T=start_T,
                                T=T,
                                N=N)

    phi1_list = []
    phi2_list = []
    theta1_list = []
    theta2_list = []
    theta3_list = []
    realized_reward = []

    for iter in range(1, train_iteration+1):
        if iter % 5 == 0: print(iter)
        realized_reward_sum_over_paths = 0
        ## collect samples
        for path in range(PATH_NUM):

            # day_start = time.perf_counter()

            # if episode %10 == 0: print(episode)
            print(files_name[path % num_training_file])

            # reset state and algos
            state = env.reset_env(read_OF_from=file_dir + files_name[path % num_training_file]['file_OF'],
                                  read_LOB_from=file_dir + files_name[path % num_training_file]['file_LOB'],
                                  start_T=start_T,
                                  T=T,
                                  N=N)
            algo.reset(S0_this_period=env.ref_price)
            done = False

            path_states = []
            path_rewards = []
            while not done:
                path_states.append(copy.deepcopy(state))

                ## execute the action(s)
                algo_mean_var, done_algo = algo.action(state)

                ## obtain the reward and the next state
                Delta_xt, QV_penalty, state, done_sim = env.step(action=algo_mean_var)

                path_rewards.append(Delta_xt + algo.Lambda * QV_penalty)

                if done_sim == True and done_algo == False:
                    # Dump all the remaining shares to liquidate
                    # action = [Type, Size, Price, Direction]
                    print(f"Warning: sim is done but algo is not done!")
                    algo_action = [orderType_MO, env.state['remaining_shares'], 0, 1]
                    reward, _ = env.handle_action([algo_action])
                    path_rewards.append(reward)
                # Problem warning:
                # Sim is done but algo is not
                done = done_algo or done_sim

            feature_list = []
            for state in path_states:
                feature = [0, 0, 0]
                for key, value in state.items():
                    if key == 'remaining_time':
                        feature[0] = value / (250 * 6.5 * 3600)  # in years
                    elif key == 'remaining_shares':
                        feature[1] = value / qty_to_exec  # in pct
                    else:  # midPrice
                        feature[2] = value / 1e4
                feature_list.append(feature)

            feature_matrix = np.array(feature_list)  # list of lists to np.array (N x num_feat)
            path_rewards_np = np.array(path_rewards)
            reward_to_go = path_rewards_np.sum() - path_rewards_np.cumsum() + path_rewards_np
            realized_reward_sum_over_paths += np.sum(path_rewards)

            if path == 0:
                state_reward = np.concatenate((feature_matrix, reward_to_go.reshape(-1, 1)), axis=1)
            else:
                state_reward_this_time = np.concatenate((feature_matrix, reward_to_go.reshape(-1, 1)), axis=1)
                state_reward = np.concatenate((state_reward, state_reward_this_time), axis=0)

            # print(time.perf_counter() - day_start, reward_to_go[0])

        tau = state_reward[:, 0]
        q = state_reward[:, 1]
        S = state_reward[:, 2]
        reward_to_go = state_reward[:, 3]

        algo.policyEvaluation(q=q, S=S, reward_to_go=reward_to_go, tau=tau, epoch=iter)
        algo.policyGradient(q=q, tau=tau, epoch=iter)

        phi1_list.append(algo.phi1)
        phi2_list.append(algo.phi2)
        theta1_list.append(algo.theta1)
        theta2_list.append(algo.theta2)
        theta3_list.append(algo.theta3)
        realized_reward.append(realized_reward_sum_over_paths/PATH_NUM)
        print(f"realized_reward_iter={realized_reward[-1]}")

    RunningTime = round(time.perf_counter() - RunningStartTime, 3)
    if plot:
        fig = plt.figure(figsize=(18, 12), dpi=300)
        avg_window = int(train_iteration * 0.1)

        ax00 = plt.subplot2grid((3, 2), (0, 0), colspan=1)
        ax00.plot(phi1_list, label=f"emp={round(np.mean(phi1_list[-avg_window:]), 3)}")
        ax00.title.set_text(f"phi1, ln_r={choose_agent.alpha_phi1}")
        plt.legend()

        ax01 = plt.subplot2grid((3, 2), (0, 1), colspan=1)
        ax01.plot(phi2_list, label=f"emp={round(np.mean(phi2_list[-avg_window:]), 3)}")
        ax01.title.set_text(f"phi2, ln_r={choose_agent.alpha_phi2}")
        plt.legend()

        ax10 = plt.subplot2grid((3, 2), (1, 0), colspan=1)
        ax10.plot(theta1_list, label=f"emp={round(np.mean(theta1_list[-avg_window:]), 6)}")
        ax10.title.set_text(f"theta1, ln_r={choose_agent.alpha_theta1}")
        plt.legend()

        ax11 = plt.subplot2grid((3, 2), (1, 1), colspan=1)
        ax11.plot(theta2_list, label=f"emp={round(np.mean(theta2_list[-avg_window:]), 3)}")
        ax11.title.set_text(f"theta2, ln_r={choose_agent.alpha_theta2}")
        plt.legend()

        ax20 = plt.subplot2grid((3, 2), (2, 0), colspan=1)
        ax20.plot(theta3_list, label=f"emp={round(np.mean(theta3_list[-avg_window:]), 3)}")
        ax20.title.set_text(f"theta3, ln_r={choose_agent.alpha_theta3}")
        plt.legend()

        ax21 = plt.subplot2grid((3, 2), (2, 1), colspan=1)
        ax21.plot(realized_reward, label=f"emp={round(np.mean(realized_reward[-avg_window:]), 6)}")
        ma_window = 10
        realized_rev_ma = (np.convolve(realized_reward, np.ones(ma_window), mode='valid') / ma_window).tolist()
        ax21.plot(list(range(ma_window - 1, len(realized_reward))), realized_rev_ma, label=f"ma_{ma_window}")
        ax21.title.set_text('realized_reward')
        plt.legend()

        fig.suptitle(f"{file_dir[39:43]}, {train_iteration} iters, {PATH_NUM} paths,{RunningTime} sec")
        plt.show()

    return algo, phi1_list, phi2_list, theta1_list, theta2_list, theta3_list, realized_reward


if __name__ == '__main__':

    file_dir = '/Users/boyuwang/Downloads/data_LOBSTER/16Q4/-data-dwn-22-143--AAPL_2016-10-01_2016-12-31_50/'
    all_files = os.listdir(file_dir)
    all_files.sort()

    incomplete_OF_date = ['AAPL_2016-08-31', 'AAPL_2017-01-03', 'AAPL_2017-03-21']

    files_for_training = []
    files_for_validation = []
    files_for_testing = []
    valid_days = 13
    for i in range(int(len(all_files) / 2)):
        if all_files[2 * i][:15] in incomplete_OF_date:
            continue

        if '2017-03' not in all_files[2 * i]:
            files_for_training.append({'file_OF': all_files[2 * i], 'file_LOB': all_files[2 * i + 1]})
        elif i - len(files_for_training) < valid_days:
            files_for_validation.append({'file_OF': all_files[2 * i], 'file_LOB': all_files[2 * i + 1]})
        else:
            files_for_testing.append({'file_OF': all_files[2 * i], 'file_LOB': all_files[2 * i + 1]})

    N = 100
    T_in_year = 1/250/6.5
    T_in_sec = 3600
    start_T_in_sec = 11 * 3600
    Lambda = 50
    zeta = 10
    choose_agent = AlmgrenChriss_EMQV(T=T_in_year,
                                      N=N,
                                      q0=1,
                                      Lambda=Lambda,
                                      zeta=zeta)

    train_iteration = 20
    PE_iter_num = 200
    trained_agent, phi1_list, phi2_list, theta1_list, theta2_list, theta3_list, realized_reward = train(
        file_dir=file_dir,
        files_name=files_for_training,
        start_T=start_T_in_sec,
        T=T_in_sec,
        N=N,
        choose_agent=choose_agent,
        train_iteration=train_iteration,
        PATH_NUM=len(files_for_training),
        PE_iter_num=PE_iter_num,
        plot=True
    )

    # training_res = pd.DataFrame()
    # training_res['phi1'] = phi1_list
    # training_res['phi2'] = phi2_list
    # training_res['theta1'] = theta1_list
    # training_res['theta2'] = theta2_list
    # training_res['theta3'] = theta3_list
    # training_res['realized_r'] = realized_reward
    # training_res.to_csv(f"AC_EMQV_{file_dir[39:43]}_Lam{Lambda}_Zeta{zeta}_training_{train_iteration}iters_{round(start_T_in_sec / 3600)}_{round((start_T_in_sec + T_in_sec) / 3600)}.csv")



    # choose_agent = TWAP(T=T_in_year, N=N, q0=1, Lambda=Lambda, zeta=zeta)
    #
    # result_training = run_sim(file_dir=file_dir,
    #                           files_name=files_for_training,
    #                           start_T=start_T_in_sec,
    #                           T=T_in_sec,
    #                           N=N,
    #                           choose_agent=choose_agent,
    #                           episodes=len(files_for_training),
    #                           mode='training',
    #                           save_result=True)















