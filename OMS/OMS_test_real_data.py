from OMS import OrderManagementSystem
import os
import pandas as pd
import datetime

current_path = os.path.dirname(__file__)
backtest_path = os.path.dirname(current_path)
data_path = os.path.dirname(backtest_path)
file_dir = data_path + '/17Q1/-data-dwn-22-143--AAPL_2017-01-01_2017-03-31_50/'

file_name_OF = 'AAPL_2017-01-03_34200000_57600000_message_50.csv'
file_name_LOB = file_name_OF.replace('message', 'orderbook')

read_OF_from = file_dir + file_name_OF
read_LOB_from = file_dir + file_name_LOB

data_OF = pd.read_csv(read_OF_from, header=None)
data_LOB = pd.read_csv(read_LOB_from, header=None)

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

init_LOB = data_LOB.iloc[0, :].values.tolist()
init_Ask, init_Bid = lobsterLOB_to_listLOB(init_LOB)
OMS = OrderManagementSystem(init_AskBook_list=init_Ask, init_BidBook_list=init_Bid)
LOB_should_be = init_LOB

OF_type = data_OF.iloc[:, 1].values.tolist()
OF_size = data_OF.iloc[:, 3].values.tolist()
OF_price = data_OF.iloc[:, 4].values.tolist()
OF_direction = data_OF.iloc[:, 5].values.tolist()

starttime = datetime.datetime.now()
for i in range(1, len(data_OF)):
    if i % 5000 == 0:
        print(f"i={i}")
    init_LOB = LOB_should_be
    init_Ask, init_Bid = lobsterLOB_to_listLOB(init_LOB)
    OMS.reset_LOB(init_AskBook_list=init_Ask, init_BidBook_list=init_Bid)

    OMS.receive_order(orderType=OF_type[i],
                      orderSize=OF_size[i],
                      orderPrice=OF_price[i],
                      orderDirection=OF_direction[i])

    LOB_should_be = data_LOB.iloc[i, :].values.tolist()

    for j in range(0, len(LOB_should_be), 2):  # 0,2,4,....
        level_idx = j // 4
        if j % 4 == 0:  # ask price
            if level_idx >= len(OMS.LOB.askBook.Book_public):
                continue
            my_LOB_at_this_level = OMS.LOB.askBook.Book_public[level_idx]
        else:  # bid price
            if level_idx >= len(OMS.LOB.bidBook.Book_public):
                continue
            my_LOB_at_this_level = OMS.LOB.bidBook.Book_public[level_idx]

        if LOB_should_be[j] != my_LOB_at_this_level.price or LOB_should_be[j + 1] != my_LOB_at_this_level.qty:
            print(f"i={i}, j={j}, LOB_should_be[j]={LOB_should_be[j]}, my_LOB_at_this_level.price={my_LOB_at_this_level.price}, LOB_should_be[j+1]={LOB_should_be[j + 1]}, my_LOB_at_this_level.qty={my_LOB_at_this_level.qty}")
        # assert LOB_should_be[j] == my_LOB_at_this_level.price  # test price
        # assert LOB_should_be[j + 1] == my_LOB_at_this_level.qty  # test qty

endtime = datetime.datetime.now()
print(f"running time = {(endtime - starttime).seconds}")

# running time = 215 sec
# no error

# if you only loop through all the OF, running time = 3 sec
