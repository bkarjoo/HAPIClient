import datetime
import time
from observer import *





class tif_type:
    day = 'DAY'
    ioc = 'IOC'
    opg = 'OPG'


class operation_type:
    new_order = 'N'
    htb_new_order = 'M'
    cancel = 'C'
    none = None


class side_type:
    buy = 'B'
    sell = 'S'
    short = 'T'
    buy_to_cover = 'BC'
    none = None


class channel:
    CSFB = 'CSFB'
    NITE = 'NITE'


class order_type:
    limit = 'L'
    market = 'M'
    stop = 'T'
    moc = '5'
    loc = 'B'


class display_mode:
    hidden = 'N'
    lit = 'Y'


class algo_type:
    twap = '5'
    vwap = '6'


class msg_status_type:
    pending = 'P'
    open = 'O'
    canceled = 'C'
    rejected = 'R'
    executed = 'E'


class order_status_type:
    submitting = 0
    acknowledged = 1  # acknowledged by hydra, but not the exchange
    open = 2
    canceled = 3
    rejected = 4
    partial_open = 5
    partial_canceled = 6
    executed = 7


class Order(object):

    def __init__(self):
        self.statusChangeNotifier = Order.StatusChangeNotifier(self)
        self.account = ''
        self.parent_id = ''
        self.order_id = ''
        self.operation = operation_type.none
        self.symbol = ''
        self.side = side_type.none
        self.quantity = 0
        self.order_price = ''
        self.contra = ''
        self.channel_of_execution = channel.CSFB
        self.tif = ''
        self.type = ''
        self.display = display_mode.lit
        self.stop_limit_price = ''
        self.reserve_size = ''
        self.cancel_replace_id = ''
        self.ticket_id = ''
        self.algo_fields = ''
        self.security_type = ''
        self.security_id = ''
        self.is_submitted = False
        self.cancel_submitted = False
        self.executed_quantity = 0
        self.status = order_status_type.submitting
        self.error = ''
        self.leaves_qty = 0

    def __str__(self):
        return self.craft_message()

    def set_nite_vwap(self, start_time, end_time, stop_price):
        self.algo_fields = "4,{0},{1},,,{2},N,N,100,,,N,N,0".format(start_time,end_time,stop_price)

    def craft_message(self):
        return "#:00000:N:000:{0}:{1}:{2}:N:{3}:{4}:{5}:{6}:{7}:{8}:{9}::{10}::{11}:{18}:{13}:{12}:{14}:{15}:{16}:{17}::::*".format(
            self.account, self.parent_id, self.order_id, self.symbol, self.side,
            self.quantity, self.order_price, self.contra, self.channel_of_execution,
            self.tif, self.type, self.display, self.cancel_replace_id,
            self.reserve_size, self.ticket_id, self.algo_fields, self.security_type,
            self.security_id, self.stop_limit_price)

    def craft_cancel_message(self):
        return "#:00000:N:000:{0}::{2}:C:{3}:{4}:{5}:{6}::{8}:{9}::{10}::{11}:*".format(
            self.account, self.parent_id, self.order_id, self.symbol, self.side,
            self.quantity, self.order_price, self.contra, self.channel_of_execution,
            self.tif, self.type, self.display)

    def change_status(self, stat):
        self.status = stat
        self.statusChangeNotifier.notifyObservers(stat)

    def update_order(self, tokens):
        if tokens[2] != 'S':
            raise Exception('invalid message type {0} sent to order.update_order'.format(tokens[2]))
        if tokens[4] == 'S':
            # ignore if status is pending
            if tokens[14] == msg_status_type.pending:
                self.change_status(order_status_type.acknowledged)

            elif tokens[14] == msg_status_type.executed:
                # can be partial or full
                self.executed_quantity += int(tokens[10])
                self.leaves_qty = int(tokens[20])
                if self.leaves_qty == 0:
                    self.change_status(order_status_type.executed)
                else:
                    self.change_status(order_status_type.partial_open)
            elif tokens[14] == msg_status_type.open:
                # can be unfilled order or partial
                self.leaves_qty = int(tokens[20])
                if self.leaves_qty != self.quantity:
                    self.change_status(order_status_type.partial_open)
                else:
                    self.change_status(order_status_type.open)
            elif tokens[14] == msg_status_type.rejected:
                # you want to note the error
                self.change_status(order_status_type.rejected)
                self.error = tokens[15]
            elif tokens[14] == msg_status_type.canceled:
                # this can be a partial order canceled so there's filled portion and canceled
                if self.leaves_qty == self.quantity:
                    self.change_status(order_status_type.canceled)
                else:
                    self.change_status(order_status_type.partial_canceled)
        elif tokens[4] == 'F':
            # this is an acknowledgment order, so can be ignored
            pass
        else:
            raise Exception('message type S {0} not implemented'.format(tokens[4]))

    class StatusChangeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)





# o = Order()
# o.account = 'ALGOGROUP'
# o.parrent_id = '6'
# o.symbol = 'MU'
# o.side = side_type.sell
# o.quantity = 1156
# # automatically set to CSFB, if VWAP set to NITE
# o.channel_of_execution = 'NITE'
# # submiter automatically sets to DAY, can be overriden to be OPG
# o.tif = tif_type.day
# # if price not provided, set to market else limit
# o.type = order_type.market
# # automatically set to Y, if N must be set manually
# o.display = 'Y'
# # reserve size - set automatically to 100 must be set otherwise
# o.reserve_size = '100'
# # need an algo field generator for NITE VWAP, if others needed future iteration
# o.set_nite_vwap('09-45-00','13-00-00',43.14)
# # automatically set
# o.security_type = '8'
# # automatically set equal
# o.security_id = 'MU'
#
#
# print(o)





