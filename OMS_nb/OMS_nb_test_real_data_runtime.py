# from OMS import OrderManagementSystem
from OMS_beta import OrderManagementSystem  ## beta version for testing and developing
import os
import pandas as pd
import time

def run():
    file_dir = '/Users/boyuwang/Downloads/data_LOBSTER/16Q4/-data-dwn-22-143--AAPL_2016-10-01_2016-12-31_50/'
    all_files = os.listdir(file_dir)
    all_files.sort()

    files_for_training = []
    for i in range(int(len(all_files) / 2)):
        files_for_training.append({'file_OF': all_files[2 * i], 'file_LOB': all_files[2 * i + 1]})

    running_time_all = 0
    for OF_day in files_for_training:
        print(OF_day)

        RunningStartTime = time.perf_counter()
        read_OF_from = file_dir + OF_day['file_OF']
        read_LOB_from = file_dir + OF_day['file_LOB']

        data_OF = pd.read_csv(read_OF_from, header=None,
                              names=['Time', 'Type', 'OrderID', 'Size', 'Price', 'Direction'])

        init_LOB = pd.read_csv(read_LOB_from, header=None, nrows=1).values[0].tolist()
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

        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        OMS.receive_order(orderFlow=data_OF.values)
        running_time = time.perf_counter() - RunningStartTime
        print(f"running_time = {running_time}")
        running_time_all += running_time

    print(f"average running time = {running_time_all / len(files_for_training)}")

if __name__ == '__main__':
    run()

'''
avg submission ~ 2e-6 sec
avg cancel ~ 4e-6 sec
avg exec ~ 15e-6 sec

average running time = 0.6592257962537775 sec

{'file_OF': 'AAPL_2016-10-03_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-03_34200000_57600000_orderbook_50.csv'}
running_time = 2.755098547997477
{'file_OF': 'AAPL_2016-10-04_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-04_34200000_57600000_orderbook_50.csv'}
running_time = 0.8051153599990357
{'file_OF': 'AAPL_2016-10-05_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-05_34200000_57600000_orderbook_50.csv'}
running_time = 0.4802865120000206
{'file_OF': 'AAPL_2016-10-06_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-06_34200000_57600000_orderbook_50.csv'}
running_time = 0.628768744001718
{'file_OF': 'AAPL_2016-10-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-07_34200000_57600000_orderbook_50.csv'}
running_time = 0.6387906099989777
{'file_OF': 'AAPL_2016-10-10_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-10_34200000_57600000_orderbook_50.csv'}
running_time = 0.5969597149996844
{'file_OF': 'AAPL_2016-10-11_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-11_34200000_57600000_orderbook_50.csv'}
running_time = 0.9274049240011664
{'file_OF': 'AAPL_2016-10-12_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-12_34200000_57600000_orderbook_50.csv'}
running_time = 0.8081214920021011
{'file_OF': 'AAPL_2016-10-13_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-13_34200000_57600000_orderbook_50.csv'}
running_time = 0.9184350439973059
{'file_OF': 'AAPL_2016-10-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-14_34200000_57600000_orderbook_50.csv'}
running_time = 0.8407190530015214
{'file_OF': 'AAPL_2016-10-17_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-17_34200000_57600000_orderbook_50.csv'}
running_time = 0.5843628930015257
{'file_OF': 'AAPL_2016-10-18_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-18_34200000_57600000_orderbook_50.csv'}
running_time = 0.5298929499986116
{'file_OF': 'AAPL_2016-10-19_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-19_34200000_57600000_orderbook_50.csv'}
running_time = 0.4290573009966465
{'file_OF': 'AAPL_2016-10-20_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-20_34200000_57600000_orderbook_50.csv'}
running_time = 0.6118830060004257
{'file_OF': 'AAPL_2016-10-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-21_34200000_57600000_orderbook_50.csv'}
running_time = 0.46500320399718476
{'file_OF': 'AAPL_2016-10-24_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-24_34200000_57600000_orderbook_50.csv'}
running_time = 0.375762980998843
{'file_OF': 'AAPL_2016-10-25_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-25_34200000_57600000_orderbook_50.csv'}
running_time = 0.5976628969983722
{'file_OF': 'AAPL_2016-10-26_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-26_34200000_57600000_orderbook_50.csv'}
running_time = 0.8234523029968841
{'file_OF': 'AAPL_2016-10-27_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-27_34200000_57600000_orderbook_50.csv'}
running_time = 0.6315379879997636
{'file_OF': 'AAPL_2016-10-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-28_34200000_57600000_orderbook_50.csv'}
running_time = 0.8244837879974511
{'file_OF': 'AAPL_2016-10-31_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-31_34200000_57600000_orderbook_50.csv'}
running_time = 0.5399472479984979
{'file_OF': 'AAPL_2016-11-01_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-01_34200000_57600000_orderbook_50.csv'}
running_time = 0.8888437470013741
{'file_OF': 'AAPL_2016-11-02_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-02_34200000_57600000_orderbook_50.csv'}
running_time = 0.7721742249996169
{'file_OF': 'AAPL_2016-11-03_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-03_34200000_57600000_orderbook_50.csv'}
running_time = 0.7593163109995658
{'file_OF': 'AAPL_2016-11-04_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-04_34200000_57600000_orderbook_50.csv'}
running_time = 0.7867743429997063
{'file_OF': 'AAPL_2016-11-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-07_34200000_57600000_orderbook_50.csv'}
running_time = 0.5493784729987965
{'file_OF': 'AAPL_2016-11-08_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-08_34200000_57600000_orderbook_50.csv'}
running_time = 0.6798134450000362
{'file_OF': 'AAPL_2016-11-09_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-09_34200000_57600000_orderbook_50.csv'}
running_time = 1.3735066810004355
{'file_OF': 'AAPL_2016-11-10_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-10_34200000_57600000_orderbook_50.csv'}
running_time = 1.4001367439996102
{'file_OF': 'AAPL_2016-11-11_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-11_34200000_57600000_orderbook_50.csv'}
running_time = 0.8960628189997806
{'file_OF': 'AAPL_2016-11-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-14_34200000_57600000_orderbook_50.csv'}
running_time = 0.9850213169993367
{'file_OF': 'AAPL_2016-11-15_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-15_34200000_57600000_orderbook_50.csv'}
running_time = 0.7312863490005839
{'file_OF': 'AAPL_2016-11-16_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-16_34200000_57600000_orderbook_50.csv'}
running_time = 0.7582826420002675
{'file_OF': 'AAPL_2016-11-17_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-17_34200000_57600000_orderbook_50.csv'}
running_time = 0.6775237600013497
{'file_OF': 'AAPL_2016-11-18_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-18_34200000_57600000_orderbook_50.csv'}
running_time = 0.47316710900122416
{'file_OF': 'AAPL_2016-11-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-21_34200000_57600000_orderbook_50.csv'}
running_time = 0.5111587969986431
{'file_OF': 'AAPL_2016-11-22_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-22_34200000_57600000_orderbook_50.csv'}
running_time = 0.5203374960001383
{'file_OF': 'AAPL_2016-11-23_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-23_34200000_57600000_orderbook_50.csv'}
running_time = 0.475358341998799
{'file_OF': 'AAPL_2016-11-25_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-25_34200000_57600000_orderbook_50.csv'}
running_time = 0.24409954799921252
{'file_OF': 'AAPL_2016-11-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-28_34200000_57600000_orderbook_50.csv'}
running_time = 0.4990886720006529
{'file_OF': 'AAPL_2016-11-29_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-29_34200000_57600000_orderbook_50.csv'}
running_time = 0.5122668869989866
{'file_OF': 'AAPL_2016-11-30_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-30_34200000_57600000_orderbook_50.csv'}
running_time = 0.5925591049999639
{'file_OF': 'AAPL_2016-12-01_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-01_34200000_57600000_orderbook_50.csv'}
running_time = 0.681534532999649
{'file_OF': 'AAPL_2016-12-02_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-02_34200000_57600000_orderbook_50.csv'}
running_time = 0.4875159879993589
{'file_OF': 'AAPL_2016-12-05_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-05_34200000_57600000_orderbook_50.csv'}
running_time = 0.6269828420008707
{'file_OF': 'AAPL_2016-12-06_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-06_34200000_57600000_orderbook_50.csv'}
running_time = 0.4908711280004354
{'file_OF': 'AAPL_2016-12-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-07_34200000_57600000_orderbook_50.csv'}
running_time = 0.6723806230002083
{'file_OF': 'AAPL_2016-12-08_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-08_34200000_57600000_orderbook_50.csv'}
running_time = 0.5676108370025759
{'file_OF': 'AAPL_2016-12-09_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-09_34200000_57600000_orderbook_50.csv'}
running_time = 0.5822552829995402
{'file_OF': 'AAPL_2016-12-12_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-12_34200000_57600000_orderbook_50.csv'}
running_time = 0.5289094199979445
{'file_OF': 'AAPL_2016-12-13_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-13_34200000_57600000_orderbook_50.csv'}
running_time = 0.6671428839981672
{'file_OF': 'AAPL_2016-12-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-14_34200000_57600000_orderbook_50.csv'}
running_time = 0.8041048459999729
{'file_OF': 'AAPL_2016-12-15_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-15_34200000_57600000_orderbook_50.csv'}
running_time = 0.6538872749988514
{'file_OF': 'AAPL_2016-12-16_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-16_34200000_57600000_orderbook_50.csv'}
running_time = 0.6146566830029769
{'file_OF': 'AAPL_2016-12-19_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-19_34200000_57600000_orderbook_50.csv'}
running_time = 0.4241883170034271
{'file_OF': 'AAPL_2016-12-20_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-20_34200000_57600000_orderbook_50.csv'}
running_time = 0.3612579660002666
{'file_OF': 'AAPL_2016-12-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-21_34200000_57600000_orderbook_50.csv'}
running_time = 0.36921608799821115
{'file_OF': 'AAPL_2016-12-22_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-22_34200000_57600000_orderbook_50.csv'}
running_time = 0.40050274500026717
{'file_OF': 'AAPL_2016-12-23_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-23_34200000_57600000_orderbook_50.csv'}
running_time = 0.2613251950024278
{'file_OF': 'AAPL_2016-12-27_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-27_34200000_57600000_orderbook_50.csv'}
running_time = 0.25245211299989023
{'file_OF': 'AAPL_2016-12-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-28_34200000_57600000_orderbook_50.csv'}
running_time = 0.37139390100128367
{'file_OF': 'AAPL_2016-12-29_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-29_34200000_57600000_orderbook_50.csv'}
running_time = 0.34701890599899343
{'file_OF': 'AAPL_2016-12-30_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-30_34200000_57600000_orderbook_50.csv'}
running_time = 0.4671142180013703
'''
