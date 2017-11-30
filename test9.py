"""
sentiment strategy test
"""

"""
buy something and print execution price
"""
import time
import datetime
from observer import *
from hydra_quote_manager import HydraQuoteManager
from hydra_execution_manager import HydraExecutionManager
from order_factory import OrderFactory


class SentimentStrategy(object):
    def __init__(self, executionManager, orderFactory, symbol, quantity, price, account = 'ALGOGROUP'):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.account = account
        self.orderStatusObserver = SentimentStrategy.OrderStatusObserver(self)
        self.executionManager = executionManager
        self.loo_order = 0
        self.stop_order = 0
        self.vwap_order = 0
        self.orderFactory = orderFactory
        self.timer_thread = threading.Thread(target=self.timer_loop)
        self.timer_thread.run()


    def timer_loop(self):
        # start this on its own thread
        current_time = datetime.datetime.now()
        time94455 = current_time.replace(hour=9, minute=44, second=55, microsecond=0)
        while True:
            current_time = datetime.datetime.now()
            if current_time > time94455:
                # the stop is no longer necessary, the vwap has a stop
                if self.stop_order:
                    self.executionManager.cancel_order(self.stop_order)
                break
            if self.vwap_order.status == order_status_type.canceled:
                # the order stopped out and canceled vwap, done with the strategy
                break
            time.sleep(1)

    def add_order(self, order):
        order.statusChangeNotifier.addObserver(self.orderStatusObserver)

    def placeLOOOrder(self):
        self.loo_order = self.orderFactory.generate_opg_limit_order(self.quantity, self.symbol, self.price, self.account)
        self.add_order(self.loo_order)
        self.executionManager.send_order(self.loo_order)

    def on_status_change(self, order, arg):
        if order == self.loo_order:
            if arg == order_status_type.executed or arg == order_status_type.partial_canceled:
                if self.stop_order == 0 and self.vwap_order == 0:
                    # place stop order
                    qty = self.loo_order.executed_quantity
                    fill_price = self.loo_order.get_average_execution_price()
                    stop_price = 0
                    stop_limit_price = 0
                    if self.loo_order.side == side_type.buy:
                        stop_price = round(fill_price * .99,2)
                        stop_limit_price = round(fill_price * .98,2)
                        qty = qty * - 1
                    else:
                        stop_price = round(fill_price * 1.01,2)
                        stop_limit_price = round(fill_price * 1.02,2)

                    self.stop_order = self.orderFactory.generate_stop_limit_order(qty, self.symbol, stop_price, stop_limit_price, self.account)
                    self.vwap_order = self.orderFactory.generate_nite_vwap_order(qty, self.symbol, '09-45-00', '13-00-00', stop_price, self.account)
                    self.executionManager.send_order(self.stop_order)
                    self.executionManager.send_order(self.vwap_order)
        elif order == self.stop_order:
            if arg == order_status_type.executed or arg == order_status_type.partial_canceled:
                if self.vwap_order:
                    self.executionManager.cancel_order(self.vwap_order)

    class OrderStatusObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            self.outer.on_status_change(observable, arg)


print datetime.datetime.now()
# you should have one quote manager which manages connection to IS server
qm = HydraQuoteManager()
em = HydraExecutionManager()
try:
    of = OrderFactory()
    ss = SentimentStrategy(em,of,'NOK',1,4.8,'DEMOX1')
    ss.placeLOOOrder()
    time.sleep(10)
except Exception as e:
    print e
finally:
    em.close_socket()
    qm.close_socket()

# this is an example of a strategy using the quote manager
# note that the quote manager must be initialized before entry
# there should be only one quote manager per program
# multiple strategies can use the same quote manager