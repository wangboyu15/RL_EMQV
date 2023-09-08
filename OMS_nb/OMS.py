import numpy as np
import numba as nb

# Indexing in LOB array
prcIdx = 0
qtyIdx = 1

@nb.jit(nopython=True)
def cal_LOBidx(orderPrice, highest_prc):
    return round((highest_prc - orderPrice)/100)

@nb.jit(nopython=True)
def receive_order_single(LOB, askPrice, bidPrice, orderFlow):
    """
    Parameters:
        LOB: array
        askPrice, bidPrice: int, not divided by 1e4
        orderFlow: array (6,)
    """
    orderType = orderFlow[1]
    orderSize = orderFlow[3]
    orderPrice = orderFlow[4]
    orderDirection = orderFlow[5]

    order_LOBidx = cal_LOBidx(orderPrice=orderPrice, highest_prc=LOB[0, prcIdx])
    if orderType == 1:
        '''1: Submission of a new limit order'''
        if orderDirection == 1:
            '''Buy limit order'''
            if orderPrice >= askPrice:
                '''A marketable limit buy order'''
                ask_LOBidx = cal_LOBidx(orderPrice=askPrice, highest_prc=LOB[0, prcIdx])  # order_LOBidx <= ask_LOBidx
                qty_to_insert = orderSize
                for idx in range(ask_LOBidx, order_LOBidx-1, -1):
                    if LOB[idx, qtyIdx] == 0:
                        continue
                    qty_to_exec_this_time = min(qty_to_insert, LOB[idx, qtyIdx])
                    LOB[idx, qtyIdx] -= qty_to_exec_this_time
                    qty_to_insert -= qty_to_exec_this_time
                    if qty_to_insert == 0:
                        '''
                        Two cases:
                        1. 这个limit order从askPrice开始吃，在orderPrice以下的某一个档位的时候，orderSize全部fulfil
                        2. 正好在orderPrice处把orderSize全部fulfil
                        '''
                        if LOB[idx, qtyIdx] > 0:
                            askPrice = LOB[idx, prcIdx]
                        else:
                            LOB_slice = LOB[(LOB[:, prcIdx] > LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                            askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
                        break
                if qty_to_insert > 0:
                    '''
                    把orderPrice以下的liquidity全吃完还没有fulfil orderSize，此时orderPrice变成新的bidPrice，
                    qty_to_insert变成对应的size
                    '''
                    bidPrice = orderPrice
                    LOB[order_LOBidx, qtyIdx] = qty_to_insert

            elif orderPrice > bidPrice:
                '''Submission in the bid-ask spread and this one becomes the new bid1'''
                LOB[order_LOBidx, qtyIdx] += orderSize
                bidPrice = orderPrice

            else:
                '''Normal submission in the bid book'''
                LOB[order_LOBidx, qtyIdx] += orderSize
        else:
            '''Sell limit order, -1'''
            if orderPrice <= bidPrice:
                '''A marketable limit sell order'''
                bid_LOBidx = cal_LOBidx(orderPrice=bidPrice, highest_prc=LOB[0, prcIdx])  # order_LOBidx >= bid_LOBidx
                qty_to_insert = orderSize
                for idx in range(bid_LOBidx, order_LOBidx + 1):
                    if LOB[idx, qtyIdx] == 0:
                        continue
                    qty_to_exec_this_time = min(qty_to_insert, LOB[idx, qtyIdx])
                    LOB[idx, qtyIdx] -= qty_to_exec_this_time
                    qty_to_insert -= qty_to_exec_this_time
                    if qty_to_insert == 0:
                        '''
                        Two cases:
                        1. 这个limit order从bidPrice开始吃，在orderPrice以上的某一个档位的时候，orderSize全部fulfil
                        2. 正好在orderPrice处把orderSize全部fulfil
                        '''
                        if LOB[idx, qtyIdx] > 0:
                            bidPrice = LOB[idx, prcIdx]
                        else:
                            LOB_slice = LOB[(LOB[:, prcIdx] < LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                            bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
                        break
                if qty_to_insert > 0:
                    '''
                    把orderPrice以上的liquidity全吃完还没有fulfil orderSize，此时orderPrice变成新的askPrice，
                    qty_to_insert变成对应的size
                    '''
                    askPrice = orderPrice
                    LOB[order_LOBidx, qtyIdx] = qty_to_insert

            elif orderPrice < askPrice:
                '''Submission in the bid-ask spread and this one becomes the new ask1'''
                LOB[order_LOBidx, qtyIdx] += orderSize
                askPrice = orderPrice

            else:
                '''Normal submission in the ask book'''
                LOB[order_LOBidx, qtyIdx] += orderSize
        OF_res = True

    elif orderType == 2 or orderType == 3:
        '''
        2: Cancellation (Partial deletion of a limit order)
        3: Deletion (Total deletion of a limit order)
        '''
        if orderDirection == 1 and bidPrice != LOB[-1, prcIdx]:
            # cancel a limit buy order in the bid book
            if orderSize < LOB[order_LOBidx, qtyIdx]:
                LOB[order_LOBidx, qtyIdx] -= orderSize
            else:
                LOB[order_LOBidx, qtyIdx] = 0
                if orderPrice == bidPrice:
                    # need to determine the new bid price
                    LOB_slice = LOB[(LOB[:, prcIdx] < orderPrice) & (LOB[:, qtyIdx] > 0)]
                    bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
        elif orderDirection == -1 and askPrice != LOB[0, prcIdx]:
            # cancel a limit buy order in the bid book
            if orderSize < LOB[order_LOBidx, qtyIdx]:
                LOB[order_LOBidx, qtyIdx] -= orderSize
            else:
                LOB[order_LOBidx, qtyIdx] = 0
                if orderPrice == askPrice:
                    # need to determine the new ask price
                    LOB_slice = LOB[(LOB[:, prcIdx] > orderPrice) & (LOB[:, qtyIdx] > 0)]
                    askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
        OF_res = True

    elif orderType == 4:
        '''4: Execution of a visible order'''
        qty_to_exec = orderSize
        PnL_single_trade = 0
        if orderDirection == 1:
            '''Execution in bid book'''
            bid_LOBidx = cal_LOBidx(orderPrice=bidPrice, highest_prc=LOB[0, prcIdx])
            for idx in range(bid_LOBidx, LOB.shape[0]):
                if LOB[idx, qtyIdx] == 0:
                    continue
                qty_to_exec_this_time = min(qty_to_exec, LOB[idx, qtyIdx])
                LOB[idx, qtyIdx] -= qty_to_exec_this_time
                # print("exec:", qty_to_exec_this_time, LOB[idx, prcIdx])
                PnL_single_trade += qty_to_exec_this_time * LOB[idx, prcIdx]  # haven't divided by 1e4
                qty_to_exec -= qty_to_exec_this_time

                if qty_to_exec == 0:
                    if LOB[idx, qtyIdx] > 0:
                        bidPrice = LOB[idx, prcIdx]
                    else:
                        LOB_slice = LOB[(LOB[:, prcIdx] < LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                        bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
                    break
        else:
            '''Execution in ask book'''
            ask_LOBidx = cal_LOBidx(orderPrice=askPrice, highest_prc=LOB[0, prcIdx])
            for idx in range(ask_LOBidx, -1, -1):
                if LOB[idx, qtyIdx] == 0:
                    continue
                qty_to_exec_this_time = min(qty_to_exec, LOB[idx, qtyIdx])
                LOB[idx, qtyIdx] -= qty_to_exec_this_time
                PnL_single_trade += qty_to_exec_this_time * LOB[idx, prcIdx]  # haven't divided by 1e4
                qty_to_exec -= qty_to_exec_this_time

                if qty_to_exec == 0:
                    if LOB[idx, qtyIdx] > 0:
                        askPrice = LOB[idx, prcIdx]
                    else:
                        LOB_slice = LOB[(LOB[:, prcIdx] > LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                        askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
                    break
        OF_res = PnL_single_trade

    else:
        '''
        5: Execution of a hidden limit order. We do not deal with dark pool orders in OMS.
        7: Trading halt indicator
        '''
        OF_res = True

    return askPrice, bidPrice, OF_res


@nb.jit(nopython=True)
def receive_order_array(LOB, askPrice, bidPrice, orderFlow):
    """
    Parameters:
        LOB: array
        askPrice, bidPrice: int, not divided by 1e4
        orderType, orderSize, orderPrice, orderDirection: array
    """
    for i in range(orderFlow.shape[0]):
        orderType = orderFlow[i, 1]
        orderSize = orderFlow[i, 3]
        orderPrice = orderFlow[i, 4]
        orderDirection = orderFlow[i, 5]

        order_LOBidx = cal_LOBidx(orderPrice=orderPrice, highest_prc=LOB[0, prcIdx])
        if orderType == 1:
            '''1: Submission of a new limit order'''
            if orderDirection == 1:
                '''Buy limit order'''
                if orderPrice >= askPrice:
                    '''A marketable limit buy order'''
                    ask_LOBidx = cal_LOBidx(orderPrice=askPrice, highest_prc=LOB[0, prcIdx])  # order_LOBidx <= ask_LOBidx
                    qty_to_insert = orderSize
                    for idx in range(ask_LOBidx, order_LOBidx - 1, -1):
                        if LOB[idx, qtyIdx] == 0:
                            continue
                        qty_to_exec_this_time = min(qty_to_insert, LOB[idx, qtyIdx])
                        LOB[idx, qtyIdx] -= qty_to_exec_this_time
                        qty_to_insert -= qty_to_exec_this_time
                        if qty_to_insert == 0:
                            '''
                            Two cases:
                            1. 这个limit order从askPrice开始吃，在orderPrice以下的某一个档位的时候，orderSize全部fulfil
                            2. 正好在orderPrice处把orderSize全部fulfil
                            '''
                            if LOB[idx, qtyIdx] > 0:
                                askPrice = LOB[idx, prcIdx]
                            else:
                                LOB_slice = LOB[(LOB[:, prcIdx] > LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                                askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
                            break
                    if qty_to_insert > 0:
                        '''
                        把orderPrice以下的liquidity全吃完还没有fulfil orderSize，此时orderPrice变成新的bidPrice，
                        qty_to_insert变成对应的size
                        '''
                        bidPrice = orderPrice
                        LOB[order_LOBidx, qtyIdx] = qty_to_insert

                elif orderPrice > bidPrice:
                    '''Submission in the bid-ask spread and this one becomes the new bid1'''
                    LOB[order_LOBidx, qtyIdx] += orderSize
                    bidPrice = orderPrice

                else:
                    '''Normal submission'''
                    LOB[order_LOBidx, qtyIdx] += orderSize
            else:
                '''Sell limit order, -1'''
                if orderPrice <= bidPrice:
                    '''A marketable limit sell order'''
                    bid_LOBidx = cal_LOBidx(orderPrice=bidPrice, highest_prc=LOB[0, prcIdx])  # order_LOBidx >= bid_LOBidx
                    qty_to_insert = orderSize
                    for idx in range(bid_LOBidx, order_LOBidx + 1):
                        if LOB[idx, qtyIdx] == 0:
                            continue
                        qty_to_exec_this_time = min(qty_to_insert, LOB[idx, qtyIdx])
                        LOB[idx, qtyIdx] -= qty_to_exec_this_time
                        qty_to_insert -= qty_to_exec_this_time
                        if qty_to_insert == 0:
                            '''
                            Two cases:
                            1. 这个limit order从bidPrice开始吃，在orderPrice以上的某一个档位的时候，orderSize全部fulfil
                            2. 正好在orderPrice处把orderSize全部fulfil
                            '''
                            if LOB[idx, qtyIdx] > 0:
                                bidPrice = LOB[idx, prcIdx]
                            else:
                                LOB_slice = LOB[(LOB[:, prcIdx] < LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                                bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
                            break
                    if qty_to_insert > 0:
                        '''
                        把orderPrice以上的liquidity全吃完还没有fulfil orderSize，此时orderPrice变成新的askPrice，
                        qty_to_insert变成对应的size
                        '''
                        askPrice = orderPrice
                        LOB[order_LOBidx, qtyIdx] = qty_to_insert

                elif orderPrice < askPrice:
                    '''Submission in the bid-ask spread and this one becomes the new ask1'''
                    LOB[order_LOBidx, qtyIdx] += orderSize
                    askPrice = orderPrice

                else:
                    '''Normal submission'''
                    LOB[order_LOBidx, qtyIdx] += orderSize
            OF_res = True

        elif orderType == 2 or orderType == 3:
            '''
            2: Cancellation (Partial deletion of a limit order)
            3: Deletion (Total deletion of a limit order)
            '''
            if orderDirection == 1 and bidPrice != LOB[-1, prcIdx]:
                # cancel a limit buy order in the bid book
                if orderSize < LOB[order_LOBidx, qtyIdx]:
                    LOB[order_LOBidx, qtyIdx] -= orderSize
                else:
                    LOB[order_LOBidx, qtyIdx] = 0
                    if orderPrice == bidPrice:
                        # need to determine the new bid price
                        LOB_slice = LOB[(LOB[:, prcIdx] < orderPrice) & (LOB[:, qtyIdx] > 0)]
                        bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
            elif orderDirection == -1 and askPrice != LOB[0, prcIdx]:
                # cancel a limit sell order in the ask book
                if orderSize < LOB[order_LOBidx, qtyIdx]:
                    LOB[order_LOBidx, qtyIdx] -= orderSize
                else:
                    LOB[order_LOBidx, qtyIdx] = 0
                    if orderPrice == askPrice:
                        # need to determine the new ask price
                        LOB_slice = LOB[(LOB[:, prcIdx] > orderPrice) & (LOB[:, qtyIdx] > 0)]
                        askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
            OF_res = True

        elif orderType == 4:
            '''4: Execution of a visible order'''
            qty_to_exec = orderSize
            PnL_single_trade = 0
            if orderDirection == 1:
                '''Execution in bid book'''
                bid_LOBidx = cal_LOBidx(orderPrice=bidPrice, highest_prc=LOB[0, prcIdx])
                for idx in range(bid_LOBidx, LOB.shape[0]):
                    if LOB[idx, qtyIdx] == 0:
                        continue
                    qty_to_exec_this_time = min(qty_to_exec, LOB[idx, qtyIdx])
                    LOB[idx, qtyIdx] -= qty_to_exec_this_time
                    PnL_single_trade += qty_to_exec_this_time * LOB[idx, prcIdx]  # haven't divided by 1e4
                    qty_to_exec -= qty_to_exec_this_time

                    if (qty_to_exec == 0) or (idx == LOB.shape[0] - 1):
                        if LOB[idx, qtyIdx] > 0:
                            bidPrice = LOB[idx, prcIdx]
                        else:
                            LOB_slice = LOB[(LOB[:, prcIdx] < LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                            bidPrice = LOB_slice[0, prcIdx] if LOB_slice.shape[0] > 0 else LOB[-1, prcIdx]
                        break
            else:
                '''Execution in ask book'''
                ask_LOBidx = cal_LOBidx(orderPrice=askPrice, highest_prc=LOB[0, prcIdx])
                for idx in range(ask_LOBidx, -1, -1):
                    if LOB[idx, qtyIdx] == 0:
                        continue
                    qty_to_exec_this_time = min(qty_to_exec, LOB[idx, qtyIdx])
                    LOB[idx, qtyIdx] -= qty_to_exec_this_time
                    PnL_single_trade += qty_to_exec_this_time * LOB[idx, prcIdx]  # haven't divided by 1e4
                    qty_to_exec -= qty_to_exec_this_time

                    if (qty_to_exec == 0) or (idx == 0):
                        if LOB[idx, qtyIdx] > 0:
                            askPrice = LOB[idx, prcIdx]
                        else:
                            LOB_slice = LOB[(LOB[:, prcIdx] > LOB[idx, prcIdx]) & (LOB[:, qtyIdx] > 0)]
                            askPrice = LOB_slice[-1, prcIdx] if LOB_slice.shape[0] > 0 else LOB[0, prcIdx]
                        break
            OF_res = PnL_single_trade

        else:
            '''
            5: Execution of a hidden limit order. We do not deal with dark pool orders in OMS.
            7: Trading halt indicator
            '''
            OF_res = True

    return askPrice, bidPrice, OF_res


@nb.jit(nopython=True)
def reset_LOB(LOB, init_LOB_flatten):
    LOB[:, prcIdx] = init_LOB_flatten[::2]
    LOB[:, qtyIdx] = init_LOB_flatten[1::2]

class OrderManagementSystem:
    def __init__(self, init_AskBook_list, init_BidBook_list, init_len=10_000):
        """
        An example of LOB:
        index    price   qty  b/s
        0        150.00  200
        1        149.99  100
        ...
        5002     100.02  500
        5001     100.01  0
        5000     100.00  100  ask1
        4999     99.99   0
        4998     99.98   200  bid1
        4997     99.97   100
        ...
        9998     50.02   300
        9999     50.01   200
        """

        ## tick size = $0.01 = 100 in the LOBSTER data
        self.askPrice = init_AskBook_list[0]  # not divided by 1e4
        self.bidPrice = init_BidBook_list[0]  # not divided by 1e4
        self.LOB = np.zeros(shape=(init_len, 2))

        ## Initialize prc in LOB
        highest_prc = round(self.askPrice + round(init_len/2) * 100)
        self.LOB[:, prcIdx] = [highest_prc - i * 100 for i in range(init_len)]

        ## Initialize qty in LOB
        # prc_idx = (
        #     np.round((highest_prc - np.array(init_AskBook_list[::2][::-1] + init_BidBook_list[::2])) / 100).astype(
        #         int)).tolist()
        # qty_list = init_AskBook_list[1::2][::-1] + init_BidBook_list[1::2]
        # self.LOB[prc_idx, qtyIdx] = qty_list
        '''
        BLK is not applicable, it has very high ask prices (99999999..)
        [-99960644, -99960644, -99960644, -49532, -10502, -5102, -2644, -1144, -165, -144, 535, 579, 856, 1156, 1356, 1380, 1506, 1579, 1761, 1856, 2056, 2212, 2356, 2498, 2553, 2556, 2602, 2668, 2704, 2823, 2856, 2886, 2956, 3156, 3244, 3290, 3356, 3521, 3548, 3564, 4001, 4256, 4459, 4498, 4589, 4917, 4948, 4951, 4985, 5000, 5072, 5088, 5089, 5090, 5125, 5137, 5197, 5470, 5869, 6048, 6056, 6087, 6098, 6283, 6546, 6739, 6741, 6984, 7237, 7249, 7369, 7429, 7628, 7677, 7771, 7856, 8121, 8356, 8556, 8856, 9023, 9133, 9282, 9283, 9356, 9440, 9556, 9616, 10356, 10384, 10585, 10656, 10983, 11045, 11856, 12032, 12356, 12750, 13800, 14856]
        '''

        prc_idx = np.round((highest_prc - np.array(init_AskBook_list[::2][::-1] + init_BidBook_list[::2])) / 100).astype(int)
        qty_list = init_AskBook_list[1::2][::-1] + init_BidBook_list[1::2]
        valid_idx = np.where((prc_idx >= 0) & (prc_idx < init_len))[0].tolist()
        self.LOB[prc_idx[valid_idx], qtyIdx] = [qty_list[i] for i in valid_idx]

        
    # def receive_order(self, orderType, orderSize, orderPrice, orderDirection):
    def receive_order(self, orderFlow):
        '''
        Parameters: either a single number or a list
        '''
        if len(orderFlow.shape) == 1:
            self.askPrice, self.bidPrice, OF_res = receive_order_single(
                LOB=self.LOB,
                askPrice=self.askPrice,
                bidPrice=self.bidPrice,
                orderFlow=orderFlow
            )
        else:
            self.askPrice, self.bidPrice, OF_res = receive_order_array(
                LOB=self.LOB,
                askPrice=self.askPrice,
                bidPrice=self.bidPrice,
                orderFlow=orderFlow
            )
        return OF_res

    def reset_LOB(self, init_LOB_flatten, askPrice, bidPrice):
        reset_LOB(LOB=self.LOB, init_LOB_flatten=init_LOB_flatten)
        self.askPrice = askPrice
        self.bidPrice = bidPrice
