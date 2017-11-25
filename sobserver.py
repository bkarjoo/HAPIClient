from observer import *
# import your observable class
from qobservable import Flower


class Bee:
    def __init__(self, name):
        self.name = name
        self.openObserver = Bee.OpenObserver(self)
    # An inner class for observing openings:
    def add_flower(self, f):
        f.openNotifier.addObserver(self.openObserver)
    class OpenObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
        def update(self, observable, arg):
            print("Bee " + self.outer.name +  "'s breakfast time!")

f = Flower()
bee = Bee('bebe')
bee2 = Bee('two')
bee.add_flower(f)
bee2.add_flower(f)
f.open()