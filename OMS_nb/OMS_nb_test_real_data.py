from OMS import OrderManagementSystem
import os
import pandas as pd
import numpy as np
import copy
import datetime

current_path = os.path.dirname(__file__)
backtest_path = os.path.dirname(current_path)
data_path = os.path.dirname(backtest_path)
file_dir = data_path + '/17Q1/-data-dwn-22-143--AAPL_2017-01-01_2017-03-31_50/'

file_name_OF = 'AAPL_2017-01-03_34200000_57600000_message_50.csv'
file_name_LOB = file_name_OF.replace('message', 'orderbook')

read_OF_from = file_dir + file_name_OF
read_LOB_from = file_dir + file_name_LOB

data_OF = pd.read_csv(read_OF_from, header=None).values
data_LOB = pd.read_csv(read_LOB_from, header=None).values

assert len(data_OF) == len(data_LOB)

def lobsterLOB_to_listLOB(init_LOB):
    init_Ask = []
    init_Bid = []
    for i in range(len(init_LOB)):
        if i % 4 == 0:  # ask price
            init_Ask.append(init_LOB[i])
        elif i % 4 == 1:  # ask size
            init_Ask.append(init_LOB[i])
        elif i % 4 == 2:  # bid price
            init_Bid.append(init_LOB[i])
        else:
            init_Bid.append(init_LOB[i])
    return init_Ask, init_Bid

init_LOB = data_LOB[0, :].tolist()
init_Ask, init_Bid = lobsterLOB_to_listLOB(init_LOB)
OMS = OrderManagementSystem(init_AskBook_list=init_Ask, init_BidBook_list=init_Bid, init_len=10_000)
LOB_should_be = init_LOB

print(f"Start testing")
starttime = datetime.datetime.now()
for i in range(1, len(data_OF)):
    if i % 10000 == 0:
        print(f"i={i}")
    init_LOB = LOB_should_be
    init_Ask, init_Bid = lobsterLOB_to_listLOB(init_LOB)
    OMS.reset_LOB(init_AskBook_list=init_Ask, init_BidBook_list=init_Bid, init_len=10_000)
    LOB_before = copy.deepcopy(OMS.LOB)
    data_OF_i = data_OF[i, :]

    OMS.receive_order(orderFlow=data_OF[i, :])
    LOB_no_zero = OMS.LOB[OMS.LOB[:, 1] > 0]

    LOB_should_be = data_LOB[i, :].tolist()

    for j in range(LOB_no_zero.shape[0]):
        if round(LOB_no_zero[j, 0]) not in LOB_should_be:
            continue
        idx = LOB_should_be.index(round(LOB_no_zero[j, 0]))
        if LOB_no_zero[j, 1] != LOB_should_be[idx + 1]:
            print(f"qty not match")

    if OMS.askPrice != LOB_should_be[0]:
        print(f"ap1 not match")
    if OMS.bidPrice != LOB_should_be[2]:
        print(f"bp1 not match")

endtime = datetime.datetime.now()
print(f"running time = {(endtime - starttime).seconds}")

# running time = 1610 sec
# no error
