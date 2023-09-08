from OMS_beta import OrderManagementSystem
import numpy  as np
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

init_len = 10_000

class TestOMS:

    # def test_OMS_submit_normal(self):
    #
    #     OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook, init_len=init_len)
    #     assert OMS.bidPrice == init_BidBook[0]
    #     assert OMS.askPrice == init_AskBook[0]
    #     assert OMS.bidPrice < OMS.askPrice
    #
    #     order_buy = {'orderType': 1,
    #                  'orderSize': 500,
    #                  'orderPrice': OMS.bidPrice,
    #                  'orderDirection': 1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     assert qty_after - qty_before == order_buy['orderSize']
    #
    #     order_buy = {'orderType': 1,
    #                  'orderSize': 500,
    #                  'orderPrice': OMS.bidPrice - 100,
    #                  'orderDirection': 1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     assert qty_after - qty_before == order_buy['orderSize']
    #
    #
    #     order_sell = {'orderType': 1,
    #                   'orderSize': 500,
    #                   'orderPrice': OMS.askPrice,
    #                   'orderDirection': -1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1]
    #     assert qty_after - qty_before == order_sell['orderSize']
    #
    #     order_sell = {'orderType': 1,
    #                   'orderSize': 500,
    #                   'orderPrice': 1159700,
    #                   'orderDirection': -1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1]
    #     assert qty_after - qty_before == order_sell['orderSize']
    #
    # def test_OMS_submit_in_spread(self):
    #     OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook, init_len=init_len)
    #
    #     delta_p = 100
    #     order_buy = {'orderType': 1,
    #                  'orderSize': 500,
    #                  'orderPrice': OMS.bidPrice + delta_p,
    #                  'orderDirection': 1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.bidPrice == order_buy['orderPrice']
    #     assert OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1] == order_buy['orderSize']
    #
    #
    #     order_sell = {'orderType': 1,
    #                   'orderSize': 500,
    #                   'orderPrice': OMS.askPrice - delta_p,
    #                   'orderDirection': -1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.askPrice == order_sell['orderPrice']
    #     assert OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1] == order_sell['orderSize']
    #
    #
    # def test_OMS_submit_mktable_order(self):
    #     """
    #     1. 这个limit order从askPrice开始吃，在orderPrice以下的某一个档位的时候，orderSize全部fulfil
    #     """
    #     OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
    #
    #     bid_before = OMS.bidPrice
    #     order_buy = {'orderType': 1,
    #                  'orderSize': 925,
    #                  'orderPrice': 1159900,
    #                  'orderDirection': 1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.bidPrice == bid_before
    #     assert OMS.askPrice == 1159500
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.askPrice][0][1] == 350
    #
    #
    #     ask_before = OMS.askPrice
    #     order_sell = {'orderType': 1,
    #                   'orderSize': 1770,
    #                   'orderPrice': 1156400,
    #                   'orderDirection': -1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.askPrice == ask_before
    #     assert OMS.bidPrice == 1156500
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.bidPrice][0][1] == 200
    #
    #     """
    #     2. 正好在orderPrice处把orderSize全部fulfil
    #     """
    #     OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
    #
    #     bid_before = OMS.bidPrice
    #     order_buy = {'orderType': 1,
    #                  'orderSize': 1305,
    #                  'orderPrice': 1159900,
    #                  'orderDirection': 1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.bidPrice == bid_before
    #     assert OMS.askPrice == 1159900
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.askPrice][0][1] == 200
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159300][0][1] == 0
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159400][0][1] == 0
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159500][0][1] == 0
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159600][0][1] == 0
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159700][0][1] == 0
    #     assert OMS.LOB[OMS.LOB[:, 0] == 1159800][0][1] == 0
    #
    #
    #     ask_before = OMS.askPrice
    #     order_sell = {'orderType': 1,
    #                   'orderSize': 1570,
    #                   'orderPrice': 1156400,
    #                   'orderDirection': -1}
    #
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.askPrice == ask_before
    #     assert OMS.bidPrice == 1156500
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.bidPrice][0][1] == 400
    #     for i in range(10):
    #         assert OMS.LOB[OMS.LOB[:, 0] == 1156600 + i * 100][0][1] == 0
    #
    #
    # def test_OMS_cancel_normal(self):
    #
    #     OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
    #
    #     #
    #     qty_to_left = 1
    #     #
    #
    #     '''Cancel at bid1 with qty_to_left share(s) left'''
    #     order_buy = {'orderType': 2,
    #                  'orderSize': OMS.LOB[OMS.LOB[:, 0] == OMS.bidPrice][0][1] - qty_to_left,
    #                  'orderPrice': OMS.bidPrice,
    #                  'orderDirection': 1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.bidPrice == order_buy['orderPrice']
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.bidPrice][0][1] == qty_to_left
    #
    #     '''Cancel at the price level that does not exist'''
    #     order_buy = {'orderType': 2,
    #                  'orderSize': 10,
    #                  'orderPrice': 1156600,
    #                  'orderDirection': 1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     assert qty_before == 0
    #     assert qty_after == 0
    #
    #     '''Cancel the remaining qty_to_left share(s) at bid1'''
    #     bid_before = OMS.bidPrice
    #     order_buy = {'orderType': 2,
    #                  'orderSize': qty_to_left,
    #                  'orderPrice': OMS.bidPrice,
    #                  'orderDirection': 1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_buy['orderType'],
    #                 0,
    #                 order_buy['orderSize'],
    #                 order_buy['orderPrice'],
    #                 order_buy['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.LOB[OMS.LOB[:, 0] == bid_before][0][1] == 0
    #     assert OMS.bidPrice == 1156700
    #
    #
    #     '''Cancel at ask1 with qty_to_left share(s) left'''
    #     order_sell = {'orderType': 2,
    #                   'orderSize': OMS.LOB[OMS.LOB[:, 0] == OMS.askPrice][0][1] - qty_to_left,
    #                   'orderPrice': OMS.askPrice,
    #                   'orderDirection': -1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.askPrice == order_sell['orderPrice']
    #     assert OMS.LOB[OMS.LOB[:, 0] == OMS.askPrice][0][1] == qty_to_left
    #
    #     '''Cancel at the price level that does not exist'''
    #     order_sell = {'orderType': 2,
    #                   'orderSize': 10,
    #                   'orderPrice': 1159700,
    #                   'orderDirection': -1}
    #     qty_before = OMS.LOB[OMS.LOB[:, 0] == order_buy['orderPrice']][0][1]
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     qty_after = OMS.LOB[OMS.LOB[:, 0] == order_sell['orderPrice']][0][1]
    #     assert qty_before == 0
    #     assert qty_after == 0
    #
    #     '''Cancel the remaining qty_to_left share(s) at ask1'''
    #     ask_before = OMS.askPrice
    #     order_sell = {'orderType': 2,
    #                   'orderSize': qty_to_left,
    #                   'orderPrice': OMS.askPrice,
    #                   'orderDirection': -1}
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 order_sell['orderSize'],
    #                 order_sell['orderPrice'],
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.LOB[OMS.LOB[:, 0] == ask_before][0][1] == 0
    #     assert OMS.askPrice == ask_before + 100
    #
    #     '''Cancel 之后需要找到新的ask1'''
    #     ## order : time, type, ID, size, price, direction
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 100,
    #                 1159400,
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 950,
    #                 1159500,
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     OMS.receive_order(
    #         orderFlow=np.array(
    #             [
    #                 0,
    #                 order_sell['orderType'],
    #                 0,
    #                 30,
    #                 1159600,
    #                 order_sell['orderDirection']
    #             ]
    #         )
    #     )
    #     assert OMS.askPrice == 1159900


    def test_OMS_exec_normal(self):

        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)

        order_buy = {'orderType': 4,
                     'orderSize': 225,
                     'orderPrice': 0,
                     'orderDirection': -1}
        ask_before = OMS.askPrice
        ask1_to_be = 1159400
        PnL = OMS.receive_order(
            orderFlow=np.array(
                [
                    0,
                    order_buy['orderType'],
                    0,
                    order_buy['orderSize'],
                    order_buy['orderPrice'],
                    order_buy['orderDirection']
                ]
            )
        )
        assert ask1_to_be == OMS.askPrice
        assert OMS.LOB[OMS.LOB[:, 0] == ask_before][0][1] == 0
        assert PnL == order_buy['orderSize'] * ask_before

        ask_before = OMS.askPrice
        order_buy = {'orderType': 4,
                     'orderSize': 50,
                     'orderPrice': 0,
                     'orderDirection': -1}
        PnL = OMS.receive_order(
            orderFlow=np.array(
                [
                    0,
                    order_buy['orderType'],
                    0,
                    order_buy['orderSize'],
                    order_buy['orderPrice'],
                    order_buy['orderDirection']
                ]
            )
        )
        assert ask_before == OMS.askPrice
        assert OMS.LOB[OMS.LOB[:, 0] == ask_before][0][1] == 50
        assert PnL == order_buy['orderSize'] * ask_before


    def test_OMS_exec_eat_book(self):

        OMS = OrderManagementSystem(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)

        order_buy = {'orderType': 4,
                     'orderSize': 1305,
                     'orderPrice': 0,
                     'orderDirection': -1}
        PnL = OMS.receive_order(
            orderFlow=np.array(
                [
                    0,
                    order_buy['orderType'],
                    0,
                    order_buy['orderSize'],
                    order_buy['orderPrice'],
                    order_buy['orderDirection']
                ]
            )
        )
        assert OMS.askPrice == 1159900
        assert PnL == 1159300 * 225 + 1159400 * 100 + 1159500 * 950 + 1159600 * 30

        bid_before = OMS.bidPrice
        order_sell = {'orderType': 4,
                      'orderSize': 70,
                      'orderPrice': 0,
                      'orderDirection': 1}
        PnL = OMS.receive_order(
            orderFlow=np.array(
                [
                    0,
                    order_sell['orderType'],
                    0,
                    order_sell['orderSize'],
                    order_sell['orderPrice'],
                    order_sell['orderDirection']
                ]
            )
        )
        assert OMS.bidPrice == 1156700
        assert PnL == order_sell['orderSize'] * bid_before

        order_sell = {'orderType': 4,
                      'orderSize': 1900,
                      'orderPrice': 0,
                      'orderDirection': 1}
        PnL = OMS.receive_order(
            orderFlow=np.array(
                [
                    0,
                    order_sell['orderType'],
                    0,
                    order_sell['orderSize'],
                    order_sell['orderPrice'],
                    order_sell['orderDirection']
                ]
            )
        )
        assert OMS.bidPrice == 1156100
        assert PnL == 1156700 * 1500 + 1156500 * 400

if __name__ == "__main__":
    pytest.main()






