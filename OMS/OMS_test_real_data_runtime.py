from OMS import OrderManagementSystem
import os
import pandas as pd
import time

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

    OF_type = data_OF.iloc[:, 1].values.tolist()
    OF_size = data_OF.iloc[:, 3].values.tolist()
    OF_price = data_OF.iloc[:, 4].values.tolist()
    OF_direction = data_OF.iloc[:, 5].values.tolist()

    for i in range(len(data_OF)):
        OMS.receive_order(orderType=OF_type[i],
                          orderSize=OF_size[i],
                          orderPrice=OF_price[i],
                          orderDirection=OF_direction[i])
    running_time = time.perf_counter() - RunningStartTime
    print(f"running_time = {running_time}")
    running_time_all += running_time

print(f"average running time = {running_time_all/len(files_for_training)}")

'''
average running time = 5.9102531029680065
{'file_OF': 'AAPL_2016-10-03_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-03_34200000_57600000_orderbook_50.csv'}
running_time = 5.179822147001687
{'file_OF': 'AAPL_2016-10-04_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-04_34200000_57600000_orderbook_50.csv'}
running_time = 8.69598967499769
{'file_OF': 'AAPL_2016-10-05_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-05_34200000_57600000_orderbook_50.csv'}
running_time = 4.630009685999539
{'file_OF': 'AAPL_2016-10-06_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-06_34200000_57600000_orderbook_50.csv'}
running_time = 5.737776287001907
{'file_OF': 'AAPL_2016-10-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-07_34200000_57600000_orderbook_50.csv'}
running_time = 6.019543071997759
{'file_OF': 'AAPL_2016-10-10_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-10_34200000_57600000_orderbook_50.csv'}
running_time = 5.598227800001041
{'file_OF': 'AAPL_2016-10-11_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-11_34200000_57600000_orderbook_50.csv'}
running_time = 9.757515221001086
{'file_OF': 'AAPL_2016-10-12_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-12_34200000_57600000_orderbook_50.csv'}
running_time = 7.308437183000933
{'file_OF': 'AAPL_2016-10-13_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-13_34200000_57600000_orderbook_50.csv'}
running_time = 8.509345147998829
{'file_OF': 'AAPL_2016-10-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-14_34200000_57600000_orderbook_50.csv'}
running_time = 8.12789637899914
{'file_OF': 'AAPL_2016-10-17_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-17_34200000_57600000_orderbook_50.csv'}
running_time = 5.658803263999289
{'file_OF': 'AAPL_2016-10-18_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-18_34200000_57600000_orderbook_50.csv'}
running_time = 5.014028290999704
{'file_OF': 'AAPL_2016-10-19_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-19_34200000_57600000_orderbook_50.csv'}
running_time = 3.9346335900008853
{'file_OF': 'AAPL_2016-10-20_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-20_34200000_57600000_orderbook_50.csv'}
running_time = 5.927096586998232
{'file_OF': 'AAPL_2016-10-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-21_34200000_57600000_orderbook_50.csv'}
running_time = 4.483902621999732
{'file_OF': 'AAPL_2016-10-24_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-24_34200000_57600000_orderbook_50.csv'}
running_time = 3.446339745001751
{'file_OF': 'AAPL_2016-10-25_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-25_34200000_57600000_orderbook_50.csv'}
running_time = 5.172127578000072
{'file_OF': 'AAPL_2016-10-26_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-26_34200000_57600000_orderbook_50.csv'}
running_time = 8.055333381998935
{'file_OF': 'AAPL_2016-10-27_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-27_34200000_57600000_orderbook_50.csv'}
running_time = 6.225659947998793
{'file_OF': 'AAPL_2016-10-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-28_34200000_57600000_orderbook_50.csv'}
running_time = 8.147011552999174
{'file_OF': 'AAPL_2016-10-31_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-10-31_34200000_57600000_orderbook_50.csv'}
running_time = 4.745774512997741
{'file_OF': 'AAPL_2016-11-01_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-01_34200000_57600000_orderbook_50.csv'}
running_time = 8.626331867999397
{'file_OF': 'AAPL_2016-11-02_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-02_34200000_57600000_orderbook_50.csv'}
running_time = 7.5439887559987255
{'file_OF': 'AAPL_2016-11-03_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-03_34200000_57600000_orderbook_50.csv'}
running_time = 7.338078507997125
{'file_OF': 'AAPL_2016-11-04_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-04_34200000_57600000_orderbook_50.csv'}
running_time = 7.877373298000748
{'file_OF': 'AAPL_2016-11-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-07_34200000_57600000_orderbook_50.csv'}
running_time = 4.929546660998312
{'file_OF': 'AAPL_2016-11-08_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-08_34200000_57600000_orderbook_50.csv'}
running_time = 6.568842093998683
{'file_OF': 'AAPL_2016-11-09_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-09_34200000_57600000_orderbook_50.csv'}
running_time = 13.882784490000631
{'file_OF': 'AAPL_2016-11-10_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-10_34200000_57600000_orderbook_50.csv'}
running_time = 15.980585152999993
{'file_OF': 'AAPL_2016-11-11_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-11_34200000_57600000_orderbook_50.csv'}
running_time = 9.7809911559998
{'file_OF': 'AAPL_2016-11-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-14_34200000_57600000_orderbook_50.csv'}
running_time = 10.97782387299958
{'file_OF': 'AAPL_2016-11-15_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-15_34200000_57600000_orderbook_50.csv'}
running_time = 6.931394655999611
{'file_OF': 'AAPL_2016-11-16_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-16_34200000_57600000_orderbook_50.csv'}
running_time = 6.766590454000834
{'file_OF': 'AAPL_2016-11-17_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-17_34200000_57600000_orderbook_50.csv'}
running_time = 6.458815493002476
{'file_OF': 'AAPL_2016-11-18_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-18_34200000_57600000_orderbook_50.csv'}
running_time = 4.147275640996668
{'file_OF': 'AAPL_2016-11-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-21_34200000_57600000_orderbook_50.csv'}
running_time = 4.446310537001409
{'file_OF': 'AAPL_2016-11-22_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-22_34200000_57600000_orderbook_50.csv'}
running_time = 4.8855679299995245
{'file_OF': 'AAPL_2016-11-23_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-23_34200000_57600000_orderbook_50.csv'}
running_time = 4.312008840999624
{'file_OF': 'AAPL_2016-11-25_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-25_34200000_57600000_orderbook_50.csv'}
running_time = 2.0479597080011445
{'file_OF': 'AAPL_2016-11-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-28_34200000_57600000_orderbook_50.csv'}
running_time = 4.1190054250000685
{'file_OF': 'AAPL_2016-11-29_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-29_34200000_57600000_orderbook_50.csv'}
running_time = 4.3646058829981484
{'file_OF': 'AAPL_2016-11-30_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-11-30_34200000_57600000_orderbook_50.csv'}
running_time = 5.101866007000353
{'file_OF': 'AAPL_2016-12-01_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-01_34200000_57600000_orderbook_50.csv'}
running_time = 6.047875879001367
{'file_OF': 'AAPL_2016-12-02_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-02_34200000_57600000_orderbook_50.csv'}
running_time = 4.304366290998587
{'file_OF': 'AAPL_2016-12-05_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-05_34200000_57600000_orderbook_50.csv'}
running_time = 5.4236289729997225
{'file_OF': 'AAPL_2016-12-06_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-06_34200000_57600000_orderbook_50.csv'}
running_time = 4.285789183999441
{'file_OF': 'AAPL_2016-12-07_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-07_34200000_57600000_orderbook_50.csv'}
running_time = 5.960996079000324
{'file_OF': 'AAPL_2016-12-08_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-08_34200000_57600000_orderbook_50.csv'}
running_time = 5.06885108699862
{'file_OF': 'AAPL_2016-12-09_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-09_34200000_57600000_orderbook_50.csv'}
running_time = 4.807825970001431
{'file_OF': 'AAPL_2016-12-12_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-12_34200000_57600000_orderbook_50.csv'}
running_time = 4.392588488000911
{'file_OF': 'AAPL_2016-12-13_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-13_34200000_57600000_orderbook_50.csv'}
running_time = 5.713241596000444
{'file_OF': 'AAPL_2016-12-14_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-14_34200000_57600000_orderbook_50.csv'}
running_time = 7.28566542200133
{'file_OF': 'AAPL_2016-12-15_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-15_34200000_57600000_orderbook_50.csv'}
running_time = 5.823053744999925
{'file_OF': 'AAPL_2016-12-16_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-16_34200000_57600000_orderbook_50.csv'}
running_time = 6.22471838400088
{'file_OF': 'AAPL_2016-12-19_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-19_34200000_57600000_orderbook_50.csv'}
running_time = 4.144463172000542
{'file_OF': 'AAPL_2016-12-20_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-20_34200000_57600000_orderbook_50.csv'}
running_time = 3.0462598189988057
{'file_OF': 'AAPL_2016-12-21_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-21_34200000_57600000_orderbook_50.csv'}
running_time = 3.0711527669991483
{'file_OF': 'AAPL_2016-12-22_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-22_34200000_57600000_orderbook_50.csv'}
running_time = 3.580078243998287
{'file_OF': 'AAPL_2016-12-23_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-23_34200000_57600000_orderbook_50.csv'}
running_time = 2.1483450809973874
{'file_OF': 'AAPL_2016-12-27_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-27_34200000_57600000_orderbook_50.csv'}
running_time = 2.182130794000841
{'file_OF': 'AAPL_2016-12-28_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-28_34200000_57600000_orderbook_50.csv'}
running_time = 3.2925471179987653
{'file_OF': 'AAPL_2016-12-29_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-29_34200000_57600000_orderbook_50.csv'}
running_time = 3.726282636001997
{'file_OF': 'AAPL_2016-12-30_34200000_57600000_message_50.csv', 'file_LOB': 'AAPL_2016-12-30_34200000_57600000_orderbook_50.csv'}
running_time = 4.353064654998889
'''
