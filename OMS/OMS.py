import os
import sys
sys.path.append(os.path.pardir)
from LOB.LOB import LimitOrderBook


class OrderManagementSystem:
    def __init__(self, init_AskBook_list, init_BidBook_list):
        
        self.LOB = LimitOrderBook(init_AskBook_list, init_BidBook_list)
        # self.ask = self.LOB.askBook.nearPrice
        # self.bid = self.LOB.bidBook.nearPrice
        # self.ask_book = self.LOB.askBook.Book_public
        # self.bid_book = self.LOB.bidBook.Book_public
        
    def receive_order(self, orderType, orderSize, orderPrice, orderDirection):
        
        if orderType == 1: 
            '''1: Submission of a new limit order'''
            if orderDirection == 1: 
                '''Buy limit order'''
                if orderPrice >= self.LOB.askBook.nearPrice: 
                    '''A marketable limit buy order'''
                    qty_to_insert = orderSize
                    while orderPrice >= self.LOB.askBook.nearPrice \
                        and qty_to_insert > 0 \
                        and len(self.LOB.askBook.Book_public) > 1:
                        qty_to_exec_this_time = min( qty_to_insert, self.LOB.askBook.Book_public[0].qty )
                        self.LOB.update(orderType='cross', orderSide='buy', quantity=qty_to_exec_this_time)
                        qty_to_insert -= qty_to_exec_this_time
                    if qty_to_insert > 0 and len(self.LOB.askBook.Book_public) > 1:
                        self.LOB.update(orderType='insert', orderSide='buy', quantity=qty_to_insert, limitPrice=orderPrice)
                else:
                    '''Normal submission'''
                    self.LOB.update(orderType='insert', orderSide='buy', quantity=orderSize, limitPrice=orderPrice)
            else:                   
                '''Sell limit order, -1'''
                if orderPrice <= self.LOB.bidBook.nearPrice: 
                    '''A marketable limit sell order'''
                    qty_to_insert = orderSize
                    while orderPrice <= self.LOB.bidBook.nearPrice \
                        and qty_to_insert > 0 \
                        and len(self.LOB.bidBook.Book_public) > 1:
                        qty_to_exec_this_time = min( qty_to_insert, self.LOB.bidBook.Book_public[0].qty )
                        self.LOB.update(orderType='cross', orderSide='sell', quantity=qty_to_exec_this_time)
                        qty_to_insert -= qty_to_exec_this_time
                    if qty_to_insert > 0 and len(self.LOB.bidBook.Book_public) > 1:
                        self.LOB.update(orderType='insert', orderSide='sell', quantity=qty_to_insert, limitPrice=orderPrice)
                else:
                    '''Normal submission'''
                    self.LOB.update(orderType='insert', orderSide='sell', quantity=orderSize, limitPrice=orderPrice)
            return True
        
        elif orderType == 2 or orderType == 3:
            '''
            2: Cancellation (Partial deletion of a limit order)
            3: Deletion (Total deletion of a limit order)
            '''
            if orderDirection == 1 and len(self.LOB.bidBook.Book_public) > 1:
                self.LOB.update(orderType='cancel', orderSide='buy', quantity=orderSize, limitPrice=orderPrice)
            elif orderDirection == -1 and len(self.LOB.askBook.Book_public) > 1:
                self.LOB.update(orderType='cancel', orderSide='sell', quantity=orderSize, limitPrice=orderPrice)
            return True
                
        elif orderType == 4:
            '''4: Execution of a visible order'''
            qty_to_exec = orderSize
            PnL_single_trade = 0
            if orderDirection == 1: 
                '''Execution price is bp1'''
                while qty_to_exec > 0 and len(self.LOB.bidBook.Book_public) > 1:
                    qty_to_exec_this_time = min( qty_to_exec, self.LOB.bidBook.Book_public[0].qty )
                    PnL_single_trade += qty_to_exec_this_time * self.LOB.bidBook.nearPrice # remember to divide 1e4 in the final result   
                    self.LOB.update(orderType='cross', orderSide='sell', quantity=qty_to_exec_this_time)
                    qty_to_exec -= qty_to_exec_this_time
            else:                   
                '''Execution price is ap1'''
                while qty_to_exec > 0 and len(self.LOB.askBook.Book_public) > 1:
                    qty_to_exec_this_time = min( qty_to_exec, self.LOB.askBook.Book_public[0].qty )
                    PnL_single_trade += qty_to_exec_this_time * self.LOB.askBook.nearPrice # remember to divide 1e4 in the final result
                    self.LOB.update(orderType='cross', orderSide='buy', quantity=qty_to_exec_this_time)
                    qty_to_exec -= qty_to_exec_this_time
            return PnL_single_trade
        
        else: 
            '''
            5: Execution of a hidden limit order. We do not deal with dark pool orders in OMS.
            7: Trading halt indicator
            '''
            return True

    def reset_LOB(self, init_AskBook_list, init_BidBook_list):
        self.LOB.reset(init_AskBook_list, init_BidBook_list)
