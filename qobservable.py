from observer import *

class Flower:
    def __init__(self):
        self.openNotifier = Flower.OpenNotifier(self)
    def open(self): # Opens its petals
        self.openNotifier.notifyObservers()
    def closing(self): return self.closeNotifier

    class OpenNotifier(Observable):
        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer
        def notifyObservers(self):
            self.setChanged()
            Observable.notifyObservers(self)