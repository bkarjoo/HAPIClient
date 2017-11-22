from quote import *
from order import *

class SentimentStrategy(object):
    def __init__(self, quote, order_submiter):
        self.entry_order = 0
        self.stop_order = 0
        self.vwap_order = 0
        self.sender = order_submiter
        self.strategy_timer()

    def place_entry_order(self, arg_list):
        # args are sent from excel sheet
        pass

    def place_stop_order(self):
        # called by entry order status listener
        # canceled by timer at 9:44:50 if still open
        pass

    def place_vwap_order(self):
        # called when stop order's status changes to canceled
        # not canceled
        pass

    def entry_order_status_change(self):
        # if completely executed place the stop order based on execution
        pass

    def stop_order_status_change(self):
        # if canceled send VWAP order
        pass

    def strategy_timer(self):
        # run every second
        # cancel stop at 9:44:50
        # stop running after this
        pass