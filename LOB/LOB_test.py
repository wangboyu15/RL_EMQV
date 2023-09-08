from LOB import LimitOrderBook
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

class TestLOB:  
        
    '''Test: Insert orders'''
    # Insert limit buy orders
    def test_LOB_insert_in_spread(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        delta_p = 1000
        ##
        best_bid_before = LOB.bidBook.nearPrice
        LOB.update('insert', 'buy', qty_to_insert, best_bid_before + delta_p )
        best_bid_after = LOB.bidBook.nearPrice
        assert best_bid_after - best_bid_before == delta_p
        assert LOB.bidBook.Book_public[0].qty == qty_to_insert
        
        best_ask_before = LOB.askBook.nearPrice
        LOB.update('insert', 'sell', qty_to_insert, best_ask_before - delta_p )
        best_ask_after = LOB.askBook.nearPrice
        assert best_ask_before - best_ask_after == delta_p
        assert LOB.askBook.Book_public[0].qty == qty_to_insert
    
    
    def test_LOB_insert_beyond_book(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        delta_p = 1000
        ##
        worst_bid_before = LOB.bidBook.Book_public[-1].price
        len_before = len(LOB.bidBook.Book_public)
        LOB.update('insert', 'buy', qty_to_insert, worst_bid_before - delta_p )
        worst_bid_after = LOB.bidBook.Book_public[-1].price
        len_after = len(LOB.bidBook.Book_public)
        assert worst_bid_before - worst_bid_after == delta_p
        assert LOB.bidBook.Book_public[-1].qty == qty_to_insert
        assert len_after - len_before == 1
        
        
        worst_ask_before = LOB.askBook.Book_public[-1].price
        len_before = len(LOB.askBook.Book_public)
        LOB.update('insert', 'sell', qty_to_insert, worst_ask_before + delta_p )
        worst_ask_after = LOB.askBook.Book_public[-1].price
        len_after = len(LOB.askBook.Book_public)
        assert worst_ask_after - worst_ask_before == delta_p
        assert LOB.askBook.Book_public[-1].qty == qty_to_insert
        assert len_after - len_before == 1
        
    
    def test_LOB_insert_in_book_at_best(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        ##
        bid_qty_before = LOB.bidBook.Book_public[0].qty
        LOB.update('insert', 'buy', qty_to_insert, LOB.bidBook.nearPrice )
        bid_qty_after = LOB.bidBook.Book_public[0].qty
        assert bid_qty_after - bid_qty_before == qty_to_insert
        
        ask_qty_before = LOB.askBook.Book_public[0].qty
        LOB.update('insert', 'sell', qty_to_insert, LOB.askBook.nearPrice )
        ask_qty_after = LOB.askBook.Book_public[0].qty
        assert ask_qty_after - ask_qty_before == qty_to_insert
    
    
    def test_LOB_insert_in_book_at_farthest(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        ##
        bid_qty_before = LOB.bidBook.Book_public[-1].qty
        LOB.update('insert', 'buy', qty_to_insert, LOB.bidBook.Book_public[-1].price )
        bid_qty_after = LOB.bidBook.Book_public[-1].qty
        assert bid_qty_after - bid_qty_before == qty_to_insert
        
        ask_qty_before = LOB.askBook.Book_public[-1].qty
        LOB.update('insert', 'sell', qty_to_insert, LOB.askBook.Book_public[-1].price )
        ask_qty_after = LOB.askBook.Book_public[-1].qty
        assert ask_qty_after - ask_qty_before == qty_to_insert
        
        
    def test_LOB_insert_in_book_existing_level(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        level_to_insert = -5
        ##
        bid_qty_before = LOB.bidBook.Book_public[level_to_insert].qty
        LOB.update('insert', 'buy', qty_to_insert, LOB.bidBook.Book_public[level_to_insert].price )
        bid_qty_after = LOB.bidBook.Book_public[level_to_insert].qty
        assert bid_qty_after - bid_qty_before == qty_to_insert
        
        ask_qty_before = LOB.askBook.Book_public[level_to_insert].qty
        LOB.update('insert', 'sell', qty_to_insert, LOB.askBook.Book_public[level_to_insert].price )
        ask_qty_after = LOB.askBook.Book_public[level_to_insert].qty
        assert ask_qty_after - ask_qty_before == qty_to_insert
        
        
    def test_LOB_insert_in_book_new_level(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_insert = 500
        level_to_insert_1 = -5
        level_to_insert_2 = -4
        ##
        bid_prc_to_insert = int((LOB.bidBook.Book_public[level_to_insert_1].price+LOB.bidBook.Book_public[level_to_insert_2].price)/2)  
        LOB.update('insert', 'buy', qty_to_insert, bid_prc_to_insert )
        assert LOB.bidBook.Book_public[level_to_insert_1].price == bid_prc_to_insert
        assert LOB.bidBook.Book_public[level_to_insert_1].qty == qty_to_insert
        
        ask_prc_to_insert = int((LOB.askBook.Book_public[level_to_insert_1].price+LOB.askBook.Book_public[level_to_insert_2].price)/2)  
        LOB.update('insert', 'sell', qty_to_insert, ask_prc_to_insert )
        assert LOB.askBook.Book_public[level_to_insert_1].price == ask_prc_to_insert
        assert LOB.askBook.Book_public[level_to_insert_1].qty == qty_to_insert

    
    

    
    '''Test: Cancel orders'''
    def test_LOB_cancel_out_perfectly(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        len_before = len(LOB.bidBook.Book_public)
        LOB.update('cancel', 'buy', LOB.bidBook.Book_public[0].qty, LOB.bidBook.nearPrice )
        len_after = len(LOB.bidBook.Book_public)
        assert len_before - len_after == 1
        assert LOB.bidBook.nearPrice == LOB.bidBook.Book_public[0].price
        
        len_before = len(LOB.askBook.Book_public)
        LOB.update('cancel', 'sell', LOB.askBook.Book_public[0].qty, LOB.askBook.nearPrice )
        len_after = len(LOB.askBook.Book_public)
        assert len_before - len_after == 1
        assert LOB.askBook.nearPrice == LOB.askBook.Book_public[0].price

        
    def test_LOB_cancel_leftover(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        level_to_cancel = -5
        qty_to_cancel = 1
        ##
        qty_before = LOB.bidBook.Book_public[level_to_cancel].qty
        LOB.update('cancel', 'buy', qty_to_cancel, LOB.bidBook.Book_public[level_to_cancel].price )
        qty_after = LOB.bidBook.Book_public[level_to_cancel].qty
        assert qty_before - qty_after == qty_to_cancel
        
        qty_before = LOB.askBook.Book_public[level_to_cancel].qty
        LOB.update('cancel', 'sell', qty_to_cancel, LOB.askBook.Book_public[level_to_cancel].price )
        qty_after = LOB.askBook.Book_public[level_to_cancel].qty
        assert qty_before - qty_after == qty_to_cancel
        
        
    def test_LOB_cancel_leq_existing_qty(self):
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        ##
        level_to_cancel = 0
        qty_to_cancel_bid = LOB.bidBook.Book_public[level_to_cancel].qty + 1
        qty_to_cancel_ask = LOB.askBook.Book_public[level_to_cancel].qty + 1
        ##
        len_before = len(LOB.bidBook.Book_public)
        LOB.update('cancel', 'buy', qty_to_cancel_bid, LOB.bidBook.Book_public[level_to_cancel].price )
        len_after = len(LOB.bidBook.Book_public)
        assert len_before - len_after == 1
        assert LOB.bidBook.nearPrice == LOB.bidBook.Book_public[0].price
        
        len_before = len(LOB.askBook.Book_public)
        LOB.update('cancel', 'sell', qty_to_cancel_ask, LOB.askBook.Book_public[level_to_cancel].price )
        len_after = len(LOB.askBook.Book_public)
        assert len_before - len_after == 1
        assert LOB.askBook.nearPrice == LOB.askBook.Book_public[0].price
        
    
    '''Test: Cross market order'''
    def test_LOB_cross_eaten_up(self):  
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ask_before = LOB.askBook.nearPrice
        len_before = len(LOB.askBook.Book_public)
        LOB.update('cross', 'buy', LOB.askBook.Book_public[0].qty)
        ask_after = LOB.askBook.nearPrice
        len_after = len(LOB.askBook.Book_public)
        assert ask_after != ask_before
        assert ask_after == LOB.askBook.Book_public[0].price
        assert len_before - len_after == 1
        
        
        bid_before = LOB.bidBook.nearPrice
        len_before = len(LOB.bidBook.Book_public)
        LOB.update('cross', 'sell', LOB.bidBook.Book_public[0].qty)
        bid_after = LOB.bidBook.nearPrice
        len_after = len(LOB.bidBook.Book_public)
        assert bid_before != bid_after
        assert bid_after == LOB.bidBook.Book_public[0].price
        assert len_before - len_after == 1
        
    
    def test_LOB_cross_leftover(self): 
        
        LOB = LimitOrderBook(init_AskBook_list=init_AskBook, init_BidBook_list=init_BidBook)
        
        ##
        qty_to_cross = 1
        ##
        ask_before = LOB.askBook.nearPrice
        len_before = len(LOB.askBook.Book_public)
        qty_before = LOB.askBook.Book_public[0].qty
        LOB.update('cross', 'buy', qty_to_cross)
        ask_after = LOB.askBook.nearPrice
        len_after = len(LOB.askBook.Book_public)
        qty_after = LOB.askBook.Book_public[0].qty
        assert ask_after == ask_before
        assert len_before == len_after
        assert qty_before - qty_after == qty_to_cross
        
        bid_before = LOB.bidBook.nearPrice
        len_before = len(LOB.bidBook.Book_public)
        qty_before = LOB.bidBook.Book_public[0].qty
        LOB.update('cross', 'sell', qty_to_cross)
        bid_after = LOB.bidBook.nearPrice
        len_after = len(LOB.bidBook.Book_public)
        qty_after = LOB.bidBook.Book_public[0].qty
        assert bid_after == bid_before
        assert len_before == len_after
        assert qty_before - qty_after == qty_to_cross
    
    
    '''Test: whether the book is empty'''
    def test_LOB_isEmpty(self):
        
        LOB = LimitOrderBook(init_AskBook_list=[10,0,11,0], init_BidBook_list=[9,0,8,0])
        assert LOB.askBook.isEmpty()
        assert LOB.bidBook.isEmpty()
        
        
        
if __name__ == "__main__":
    pytest.main()
        
        
        
        
        
        