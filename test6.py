"""
test a printer strategy object with orders
"""
import time
from observer import *
from hydra_quote_manager import HydraQuoteManager
from hydra_execution_manager import HydraExecutionManager
from order_factory import OrderFactory

class PrinterStrategy(object):
    def __init__(self, name, quoteManager, executionManager, orderFactory):
        self.name = name
        self.askObserver = PrinterStrategy.AskObserver(self)
        self.orderStatusObserver = PrinterStrategy.OrderStatusObserver(self)
        self.quoteManager = quoteManager
        self.quote = 0
        self.executionManager = executionManager
        self.order = 0
        self.orderFactory = orderFactory


    def add_quote(self, symbol):
        self.quote = self.quoteManager.start_quote_stream(symbol)
        self.quote.askNotifier.addObserver(self.askObserver)

    def remove_quote(self, symbol):
        self.quote.askNotifier.deleteObserver(self.askObserver)
        self.quoteManager.stop_quote_stream(self.quote.get_symbol())
        self.quote = 0

    def add_order(self, order):
        order.statusChangeNotifier.addObserver(self.orderStatusObserver)

    def placeATestOrder(self):
        self.order = self.orderFactory.buy('buy 100 NOK 4.8 day ALGOPAIR')
        self.add_order(self.order)
        self.executionManager.send_order(self.order)

    def cancelTestOrder(self):
        self.executionManager.cancel_order(self.order)

    class OrderStatusObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            print 'order status changed {}'.format(arg)

    class QuoteObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            print 'quote updated'

    class AskObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            print arg


# you should have one quote manager which manages connection to IS server
qm = 0
em = HydraExecutionManager()
of = OrderFactory()
p = PrinterStrategy('test', qm, em, of)
print 'entering order'
p.placeATestOrder()
print 'placed order'
time.sleep(2)
print 'cancel order'
p.cancelTestOrder()
print 'order canceled'
# the connection must be closed
time.sleep(2)
em.close_socket()

# this is an example of a strategy using the quote manager
# note that the quote manager must be initialized before entry
# there should be only one quote manager per program
# multiple strategies can use the same quote manager