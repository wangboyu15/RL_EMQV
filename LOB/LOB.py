import collections

isASK = 1
isBID = -1

class Book:
    
    def __init__(self, bidORask, initBook_list):
        #---------- fixed ----------#
        self.bidORask = isASK if bidORask == 'ask' else isBID
        self.prc_qty = collections.namedtuple('prc_qty', ['price', 'qty'])
        self.orderLevel = round(len(initBook_list)/2)  # LOBSTER: level=50
        #---------------------------#
        
        #---------- Update ----------#
        self.nearPrice = initBook_list[0]
        self.Book_public = collections.deque(
            self.prc_qty(price=initBook_list[2 * i], qty=initBook_list[2 * i + 1]) for i in range(self.orderLevel)
        )
        #---------------------------#


    def reset(self, initBook_list):
        self.Book_public.clear()
        self.Book_public.extend(
            self.prc_qty(price=initBook_list[2 * i], qty=initBook_list[2 * i + 1]) for i in
            range(round(len(initBook_list) / 2))
        )
    
    
    def isEmpty(self):
        '''Judge: whether the book is empty'''
        return [self.Book_public[i].qty for i in range(len(self.Book_public))] == [0 for i in
                                                                                   range(len(self.Book_public))]
    
    
    def insert(self, limitPrice, quantity):
        # Make sure book is never empty
        
        if self.bidORask * (limitPrice - self.nearPrice) < 0: # limit price is in the spread
            self.Book_public.appendleft(self.prc_qty(price = limitPrice, qty = quantity))
            self.nearPrice = limitPrice
            
        elif self.bidORask * (limitPrice - self.Book_public[-1].price) > 0: # beyond the book 
            self.Book_public.append( self.prc_qty(price = limitPrice, qty = quantity) )
            
        elif limitPrice == self.Book_public[-1].price:  # limit price is the farthest price
            self.Book_public[-1] = self.Book_public[-1]._replace( qty=self.Book_public[-1].qty + quantity ) 
        
        else: # normally insert
            for i in range(len(self.Book_public)-1):
                if self.bidORask * (self.Book_public[i].price - limitPrice) <= 0 and self.bidORask * (
                        limitPrice - self.Book_public[i + 1].price) < 0:
                    if self.Book_public[i].price == limitPrice:
                        self.Book_public[i] = self.Book_public[i]._replace( qty=self.Book_public[i].qty + quantity ) 
                    else:
                        self.Book_public.insert( i+1, self.prc_qty(price = limitPrice, qty = quantity) )
                    break


    def cancel(self, limitPrice, quantity):
        # Before passing in parameters, make sure (by OMS)
        # (1) price range is legal, i.e. not beyond the book
        # (2) the qty to cancel <= all qty this ID has inserted before
        
        if self.prc_qty( price=limitPrice, qty=quantity ) in self.Book_public:  # A level is cancelled out perfectly
            self.Book_public.remove( self.prc_qty( price=limitPrice, qty=quantity ) )
            if limitPrice == self.nearPrice:
                self.nearPrice = self.Book_public[0].price
            
        else:
            exist = False
            for i in range(len(self.Book_public)):
                if self.Book_public[i].price == limitPrice: # Find which level to cancel
                    # Maximum qty-to-cancel = remainig qty at this level
                    if self.Book_public[i].qty > quantity:
                        self.Book_public[i] = self.Book_public[i]._replace( qty=self.Book_public[i].qty - quantity ) 
                    else:
                        self.Book_public.remove( self.prc_qty( price=limitPrice, qty=self.Book_public[i].qty ) )
                        if limitPrice == self.nearPrice:
                            self.nearPrice = self.Book_public[0].price
                    exist = True
                    break
            # if exist == False: # does not exists such price
            #     print(f"No such price level to cancel.")


    def cross(self, quantity):
        ## need to rely on OMS to make sure :
        ## size to cross <= existing size at bid1/ask1
        
        if quantity == self.Book_public[0].qty: ## nearest level is eaten up
            self.Book_public.remove( self.prc_qty( price=self.Book_public[0].price, qty=quantity ) )
            self.nearPrice = self.Book_public[0].price
        
        else:
            self.Book_public[0] = self.Book_public[0]._replace( qty=self.Book_public[0].qty - quantity ) 




#######################################################################################################
#######################################################################################################
#######################################################################################################





class AskBook(Book):
    
    def __init__(self, init_AskBook_list):
        Book.__init__(self, bidORask='ask', initBook_list=init_AskBook_list)


class BidBook(Book):
    
    def __init__(self, init_BidBook_list):
        Book.__init__(self, bidORask='bid', initBook_list=init_BidBook_list)



#######################################################################################################
#######################################################################################################
#######################################################################################################




class LimitOrderBook:
    
    def __init__(self, init_AskBook_list, init_BidBook_list):
        '''Initialize the limit order book'''
        self.askBook = AskBook(init_AskBook_list)
        self.bidBook = BidBook(init_BidBook_list)
        
    def reset(self, init_AskBook_list, init_BidBook_list):
        '''Reset the limit order book'''
        self.askBook.reset(init_AskBook_list)
        self.bidBook.reset(init_BidBook_list)
    
    def update(self, orderType, orderSide, quantity, limitPrice=0):
        '''Update the limit order book'''
        if orderType == 'insert':
            if orderSide == 'buy':
                self.bidBook.insert(limitPrice, quantity)  
            elif orderSide == 'sell':
                self.askBook.insert(limitPrice, quantity)
        
        elif orderType == 'cancel':
            if orderSide == 'buy':
                self.bidBook.cancel(limitPrice, quantity)
                    
            elif orderSide == 'sell':
                self.askBook.cancel(limitPrice, quantity)
            
        elif orderType == 'cross':
            if orderSide == 'buy':
                ## market buy order (need to cross it in the askBook)
                self.askBook.cross(quantity)

            elif orderSide == 'sell':
                ## market sell order(need to cross it in the bidBook)
                self.bidBook.cross(quantity)
        else:
            print(f"No such order type as {orderType}!")
        
   
