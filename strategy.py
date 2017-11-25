from observer import *
from quote import Quote
from order import Order


class Strategy:
    def __init__(self, name):
        self.name = name
        self.quoteObserver = Strategy.QuoteObserver(self)
        self.askObserver = Strategy.AskObserver(self)
        self.orderStatusObserver = Strategy.OrderStatusObserver(self)

    def add_quote(self, quote):
        quote.changeNotifier.addObserver(self.quoteObserver)
        quote.askNotifier.addObserver(self.askObserver)

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
            print 'ask updated {}'.format(arg)


f = Quote('SPY')
bee = Strategy('bebe')
bee2 = Strategy('two')
bee.add_quote(f)
bee2.add_quote(f)
f.change()
f.set_ask('23.34')
print f.get_ask()

o = Order()
bee.add_order(o)
o.change_status('changed')
