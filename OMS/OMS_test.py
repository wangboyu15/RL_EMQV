from OMS import OrderManagementSystem
import os
import pandas as pd
import pytest

# AAPL_2017-01-04
init_AskBook = [1159300, 225,
                1159400, 100,
                1159500, 950,
                1159600, 30,
                1159900, 200,
                1160000, 507,
                1160900, 100,
                1161000, 412,
                1161300, 100,
                1161400, 350,
                1161500, 130,
                1162000, 500,
                1162500, 30,
                1162600, 86,
                1163600, 43,
                1163700, 100,
                1164000, 800,
                1164200, 43,
                1164700, 100,
                1165000, 10,
                1165300, 100,
                1165900, 400,
                1167500, 249,
                1169800, 40,
                1170000, 68,
                1170800, 900,
                1172000, 75,
                1174600, 150,
                1175000, 18,
                1175500, 75,
                1175800, 1400,
                1178000, 80,
                1178900, 1190,
                1180000, 532,
                1180100, 50,
                1180600, 50,
                1181900, 100,
                1182000, 50,
                1182400, 98,
                1182900, 900,
                1183000, 40,
                1183500, 10,
                1184200, 40,
                1185000, 50,
                1185300, 300,
                1186000, 14,
                1187800, 150,
                1188800, 30,
                1189600, 1400,
                1189900, 50]

init_BidBook = [1157500, 70,
                1156700, 1500,
                1156500, 400,
                1156100, 500,
                1155400, 500,
                1155100, 500,
                1155000, 470,
                1154200, 100,
                1154000, 150,
                1153000, 200,
                1152800, 100,
                1152500, 300,
                1152100, 43,
                1151200, 172,
                1151100, 43,
                1151000, 1043,
                1150800, 43,
                1150600, 86,
                1150000, 56,
                1148100, 200,
                1147600, 30,
                1146500, 900,
                1145000, 75,
                1144400, 200,
                1141600, 2400,
                1140900, 26,
                1140000, 1336,
                1135100, 900,
                1135000, 22,
                1132700, 200,
                1130000, 32,
                1127900, 2400,
                1127500, 1,
                1126800, 50,
                1125000, 8,
                1122500, 250,
                1122000, 90,
                1120000, 35,
                1118500, 30,
                1115100, 5,
                1113500, 900,
                1113400, 300,
                1112000, 100,
                1111100, 25,
                1110000, 28,
                1109600, 30,
                1105500, 100,
                1104900, 900,
                1100200, 5,
                1100000, 181]


class TestOMS:
    
    def test_OMS_submit_normal(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        order_buy = {'orderType': 1,
                     'orderSize': 500,
                     'orderPrice': OMS.LOB.bidBook.Book_public[0].price,
                     'orderDirection': 1}
        qty_before = OMS.LOB.bidBook.Book_public[0].qty
        len_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_after = len(OMS.LOB.bidBook.Book_public)
        qty_after = OMS.LOB.bidBook.Book_public[0].qty
        assert qty_after - qty_before == order_buy['orderSize']
        assert len_after == len_before
        
        
        order_sell = {'orderType': 1,
                      'orderSize': 500,
                      'orderPrice': OMS.LOB.askBook.Book_public[0].price,
                      'orderDirection': -1}
        qty_before = OMS.LOB.askBook.Book_public[0].qty
        len_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_after = len(OMS.LOB.askBook.Book_public)
        qty_after = OMS.LOB.askBook.Book_public[0].qty
        assert qty_after - qty_before == order_sell['orderSize']
        assert len_after == len_before
        
    
    def test_OMS_submit_mktable_order_die(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        #
        qty_to_left = 1
        #
        
        order_buy = {'orderType': 1,
                     'orderSize': OMS.LOB.askBook.Book_public[0].qty + OMS.LOB.askBook.Book_public[1].qty - qty_to_left,
                     'orderPrice': OMS.LOB.askBook.Book_public[1].price,
                     'orderDirection': 1}
        len_opposite_before = len(OMS.LOB.askBook.Book_public)
        len_sameSide_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_opposite_after = len(OMS.LOB.askBook.Book_public)
        len_sameSide_after = len(OMS.LOB.bidBook.Book_public)
        assert len_opposite_before - len_opposite_after == 1
        assert len_sameSide_after == len_sameSide_before
        assert OMS.LOB.askBook.Book_public[0].qty == qty_to_left
        
        
        order_sell = {'orderType': 1,
                      'orderSize': OMS.LOB.bidBook.Book_public[0].qty + OMS.LOB.bidBook.Book_public[1].qty - qty_to_left,
                      'orderPrice': OMS.LOB.bidBook.Book_public[1].price,
                      'orderDirection': -1}
        len_opposite_before = len(OMS.LOB.bidBook.Book_public)
        len_sameSide_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_opposite_after = len(OMS.LOB.bidBook.Book_public)
        len_sameSide_after = len(OMS.LOB.askBook.Book_public)
        assert len_opposite_before - len_opposite_after == 1
        assert len_sameSide_after == len_sameSide_before
        assert OMS.LOB.bidBook.Book_public[0].qty == qty_to_left
        
        
    def test_OMS_submit_mktable_order_left(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        #
        qty_to_left = 1
        #
        
        order_buy = {'orderType': 1,
                     'orderSize': OMS.LOB.askBook.Book_public[0].qty + OMS.LOB.askBook.Book_public[1].qty + qty_to_left,
                     'orderPrice': OMS.LOB.askBook.Book_public[1].price,
                     'orderDirection': 1}
        len_opposite_before = len(OMS.LOB.askBook.Book_public)
        len_sameSide_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_opposite_after = len(OMS.LOB.askBook.Book_public)
        len_sameSide_after = len(OMS.LOB.bidBook.Book_public)
        assert len_opposite_before - len_opposite_after == 2
        assert len_sameSide_after - len_sameSide_before == 1
        assert OMS.LOB.bidBook.Book_public[0].qty == qty_to_left
        
        
        order_sell = {'orderType': 1,
                      'orderSize': OMS.LOB.bidBook.Book_public[0].qty + OMS.LOB.bidBook.Book_public[1].qty + qty_to_left,
                      'orderPrice': OMS.LOB.bidBook.Book_public[1].price,
                      'orderDirection': -1}
        len_opposite_before = len(OMS.LOB.bidBook.Book_public)
        len_sameSide_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_opposite_after = len(OMS.LOB.bidBook.Book_public)
        len_sameSide_after = len(OMS.LOB.askBook.Book_public)
        assert len_opposite_before - len_opposite_after == 2
        assert len_sameSide_after - len_sameSide_before == 1
        assert OMS.LOB.askBook.Book_public[0].qty == qty_to_left
        
        
    def test_OMS_submit_mktable_book_left1(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        buy_size = 0
        for i in range(len(OMS.LOB.askBook.Book_public)):
            buy_size += OMS.LOB.askBook.Book_public[i].qty
        order_buy = {'orderType': 1,
                     'orderSize': buy_size,
                     'orderPrice': OMS.LOB.askBook.Book_public[-1].price,
                     'orderDirection': 1}
        len_sameSide_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_opposite_after = len(OMS.LOB.askBook.Book_public)
        len_sameSide_after = len(OMS.LOB.bidBook.Book_public)
        assert len_opposite_after == 1
        assert len_sameSide_after - len_sameSide_before == 0
        
        
        sell_size = 0
        for i in range(len(OMS.LOB.bidBook.Book_public)):
            sell_size += OMS.LOB.bidBook.Book_public[i].qty
        order_sell = {'orderType': 1,
                      'orderSize': sell_size,
                      'orderPrice': OMS.LOB.bidBook.Book_public[-1].price,
                      'orderDirection': -1}
        len_sameSide_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_opposite_after = len(OMS.LOB.bidBook.Book_public)
        len_sameSide_after = len(OMS.LOB.askBook.Book_public)
        assert len_opposite_after == 1
        assert len_sameSide_after - len_sameSide_before == 0
    
    
    def test_OMS_cancel_normal(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        #
        qty_to_left = 1
        #
        
        '''Cancel at bid1 with qty_to_left share(s) left'''
        order_buy = {'orderType': 2,
                     'orderSize': OMS.LOB.bidBook.Book_public[0].qty - qty_to_left,
                     'orderPrice': OMS.LOB.bidBook.Book_public[0].price,
                     'orderDirection': 1}
        len_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_after = len(OMS.LOB.bidBook.Book_public)
        assert len_after - len_before == 0
        assert OMS.LOB.bidBook.Book_public[0].qty == qty_to_left
        
        '''Cancel at the price level that does not exist'''
        order_buy = {'orderType': 2,
                     'orderSize': OMS.LOB.bidBook.Book_public[0].qty - qty_to_left,
                     'orderPrice': (OMS.LOB.bidBook.Book_public[0].price + OMS.LOB.bidBook.Book_public[1].price)/2,
                     'orderDirection': 1}
        len_before = len(OMS.LOB.bidBook.Book_public)
        qty_before = OMS.LOB.bidBook.Book_public[0].qty
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_after = len(OMS.LOB.bidBook.Book_public)
        qty_after = OMS.LOB.bidBook.Book_public[0].qty
        assert len_after - len_before == 0
        assert qty_after- qty_before == 0
        
        '''Cancel the remaining qty_to_left share(s) at bid1'''
        order_buy = {'orderType': 2,
                     'orderSize': qty_to_left,
                     'orderPrice': OMS.LOB.bidBook.Book_public[0].price,
                     'orderDirection': 1}
        len_before = len(OMS.LOB.bidBook.Book_public)
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_after = len(OMS.LOB.bidBook.Book_public)
        assert len_before - len_after == 1
        
        
        
        '''Cancel at ask1 with qty_to_left share(s) left'''
        order_sell = {'orderType': 2,
                      'orderSize': OMS.LOB.askBook.Book_public[0].qty - qty_to_left,
                      'orderPrice': OMS.LOB.askBook.Book_public[0].price,
                      'orderDirection': -1}
        len_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_after = len(OMS.LOB.askBook.Book_public)
        assert len_after - len_before == 0
        assert OMS.LOB.askBook.Book_public[0].qty == qty_to_left
        
        '''Cancel at the price level that does not exist'''
        order_sell = {'orderType': 2,
                      'orderSize': OMS.LOB.askBook.Book_public[0].qty - qty_to_left,
                      'orderPrice': (OMS.LOB.askBook.Book_public[0].price + OMS.LOB.askBook.Book_public[1].price)/2,
                      'orderDirection': -1}
        len_before = len(OMS.LOB.askBook.Book_public)
        qty_before = OMS.LOB.askBook.Book_public[0].qty
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_after = len(OMS.LOB.askBook.Book_public)
        qty_after = OMS.LOB.askBook.Book_public[0].qty
        assert len_after - len_before == 0
        assert qty_after- qty_before == 0
        
        '''Cancel the remaining qty_to_left share(s) at bid1'''
        order_sell = {'orderType': 2,
                      'orderSize': qty_to_left,
                      'orderPrice': OMS.LOB.askBook.Book_public[0].price,
                      'orderDirection': -1}
        len_before = len(OMS.LOB.askBook.Book_public)
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_after = len(OMS.LOB.askBook.Book_public)
        assert len_before - len_after == 1
        
        
    def test_OMS_exec_normal(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        #
        level_to_exec = 3
        #
        buy_size = 0
        for i in range(level_to_exec):
            buy_size += OMS.LOB.askBook.Book_public[i].qty
        order_buy = {'orderType': 4,
                     'orderSize': buy_size,
                     'orderPrice': OMS.LOB.askBook.Book_public[-1].price,
                     'orderDirection': -1}
        len_before = len(OMS.LOB.askBook.Book_public)
        ask1_to_be = OMS.LOB.askBook.Book_public[level_to_exec].price
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        len_after = len(OMS.LOB.askBook.Book_public)
        assert len_before - len_after == level_to_exec
        assert ask1_to_be == OMS.LOB.askBook.Book_public[0].price
        
        
        sell_size = 0
        for i in range(level_to_exec):
            sell_size += OMS.LOB.bidBook.Book_public[i].qty
        order_sell = {'orderType': 4,
                      'orderSize': sell_size,
                      'orderPrice': OMS.LOB.bidBook.Book_public[-1].price,
                      'orderDirection': 1}
        len_before = len(OMS.LOB.bidBook.Book_public)
        bid1_to_be = OMS.LOB.bidBook.Book_public[level_to_exec].price
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        len_after = len(OMS.LOB.bidBook.Book_public)
        assert len_before - len_after == level_to_exec
        assert bid1_to_be == OMS.LOB.bidBook.Book_public[0].price
        
        
    def test_OMS_exec_eat_book(self):
        
        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        buy_size = 0
        for i in range(len(OMS.LOB.askBook.Book_public)):
            buy_size += OMS.LOB.askBook.Book_public[i].qty
        order_buy = {'orderType': 4,
                     'orderSize': buy_size,
                     'orderPrice': OMS.LOB.askBook.Book_public[-1].price,
                     'orderDirection': -1}
        ask1_to_be = OMS.LOB.askBook.Book_public[-1].price
        OMS.receive_order(orderType = order_buy['orderType'], 
                          orderSize = order_buy['orderSize'], 
                          orderPrice = order_buy['orderPrice'], 
                          orderDirection = order_buy['orderDirection'])
        assert len(OMS.LOB.askBook.Book_public) == 1
        assert ask1_to_be == OMS.LOB.askBook.Book_public[0].price
        
        
        sell_size = 0
        for i in range(len(OMS.LOB.bidBook.Book_public)):
            sell_size += OMS.LOB.bidBook.Book_public[i].qty
        order_sell = {'orderType': 4,
                      'orderSize': sell_size,
                      'orderPrice': OMS.LOB.bidBook.Book_public[-1].price,
                      'orderDirection': 1}
        bid1_to_be = OMS.LOB.bidBook.Book_public[-1].price
        OMS.receive_order(orderType = order_sell['orderType'], 
                          orderSize = order_sell['orderSize'], 
                          orderPrice = order_sell['orderPrice'], 
                          orderDirection = order_sell['orderDirection'])
        assert len(OMS.LOB.bidBook.Book_public) == 1
        assert bid1_to_be == OMS.LOB.bidBook.Book_public[0].price
    
    # def test_OMS_real_data(self):
        
    #     current_path = os.path.dirname(__file__)
    #     backtest_path = os.path.dirname(current_path)
    #     data_path = os.path.dirname(backtest_path)
    #     file_dir = data_path+'/17Q1/-data-dwn-22-143--AAPL_2017-01-01_2017-03-31_50/'
        
    #     file_name_OF = 'AAPL_2017-01-03_34200000_57600000_message_50.csv'
    #     file_name_LOB = file_name_OF.replace('message', 'orderbook')
        
    #     read_OF_from = file_dir+file_name_OF
    #     read_LOB_from = file_dir+file_name_LOB
        
    #     data_OF = pd.read_csv(read_OF_from, header=None)
    #     data_LOB = pd.read_csv(read_LOB_from, header=None)
        
    #     assert len(data_OF) == len(data_LOB)
        
    #     init_LOB = data_LOB.iloc[0,:].values.tolist()
    #     init_Ask = []
    #     init_Bid = []
    #     for i in range(len(init_LOB)):
    #         if i%4 == 0: #ask price
    #             init_Ask.append(init_LOB[i])
    #         elif i%4 == 1: #ask size
    #             init_Ask.append(init_LOB[i])
    #         elif i%4 == 2: #bid price
    #             init_Bid.append(init_LOB[i])
    #         else:
    #             init_Bid.append(init_LOB[i])
        
    #     OMS = OrderManagementSystem(init_AskBook_list=init_Ask, init_BidBook_list=init_Bid)
    #     OF_type = data_OF.iloc[:, 1].values.tolist()
    #     OF_size = data_OF.iloc[:, 3].values.tolist()
    #     OF_price = data_OF.iloc[:, 4].values.tolist()
    #     OF_direction = data_OF.iloc[:, 5].values.tolist()
        
    #     for i in range(1, len(data_OF)):
    #         # print(i)
    #         OMS.receive_order(orderType = OF_type[i], 
    #                           orderSize = OF_size[i], 
    #                           orderPrice = OF_price[i], 
    #                           orderDirection = OF_direction[i])
            
    #         LOB_should_be = data_LOB.iloc[i,:].values.tolist()
            
    #         for j in range(0, min(len(LOB_should_be), len(OMS.LOB.askBook.Book_public), len(OMS.LOB.bidBook.Book_public)), 2): #0,2,4,....
    #             level_idx = j//4
                
    #             if j%4 == 0: #ask price
    #                 my_LOB_at_this_level = OMS.LOB.askBook.Book_public[level_idx]
    #             else: #bid price
    #                 my_LOB_at_this_level = OMS.LOB.bidBook.Book_public[level_idx]
                    
    #             if LOB_should_be[j] != my_LOB_at_this_level.price or LOB_should_be[j+1] != my_LOB_at_this_level.qty:
    #                 print(f"i={i}, j={j}, LOB_should_be[j]={LOB_should_be[j]}, my_LOB_at_this_level.price={my_LOB_at_this_level.price}, LOB_should_be[j+1]={LOB_should_be[j+1]}, my_LOB_at_this_level.qty={my_LOB_at_this_level.qty}")
    #             assert LOB_should_be[j] == my_LOB_at_this_level.price # test price
    #             assert LOB_should_be[j+1] == my_LOB_at_this_level.qty # test qty



if __name__ == "__main__":
    pytest.main()






