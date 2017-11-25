from observer import *
from quote import *

class Strategy(object):

    def __init__(self, name):
        self.name = name
        self.quote_observer = Strategy.QuoteObserver(self)

    def set_quote(self, q):
        q.changeNotifier.addObserver(self.quote_observer)


    def on_quote_update(self, q):
        print 'quote_updated: ' + q.get_symbol()

    class QuoteObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            self.outer.on_quote_update(observable)


s = Strategy()
SPY = Quote('SPY')
print s
s.set_quote(SPY)
SPY.set_last(228.5)
