"""
test a printer strategy object
"""
import time
from observer import *
from hydra_quote_manager import HydraQuoteManager

class PrinterStrategy(object):
    def __init__(self, name, quote_manager):
        self.name = name
        self.askObserver = PrinterStrategy.AskObserver(self)
        self.orderStatusObserver = PrinterStrategy.OrderStatusObserver(self)
        self.quoteManager = quote_manager
        self.quote = 0

    def add_quote(self, symbol):
        self.quote = self.quoteManager.start_quote_stream(symbol)
        self.quote.askNotifier.addObserver(self.askObserver)

    def remove_quote(self, symbol):
        self.quote.askNotifier.deleteObserver(self.askObserver)
        self.quoteManager.stop_quote_stream(self.quote.get_symbol())
        self.quote = 0

    def add_order(self, order):
        order.statusChangeNotifier.addObserver(self.orderStatusObserver)

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
qm = HydraQuoteManager()
p = PrinterStrategy('test', qm)
print 'adding quote'
p.add_quote('SPY')
print 'added quote'
time.sleep(1)
print 'removing quote'
p.remove_quote('SPY')
print 'removed quote'
# the connection must be closed
qm.close_socket()

# this is an example of a strategy using the quote manager
# note that the quote manager must be initialized before entry
# there should be only one quote manager per program
# multiple strategies can use the same quote manager