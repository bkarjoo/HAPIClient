from observer import Observable


class Quote:

    def __init__(self, symbol):
        self.changeNotifier = Quote.ChangeNotifier(self)
        self.symbol = symbol
        self.last = ''
        self.lastNotifier = Quote.LastNotifier(self)
        self.last_size = ''
        self.lastSizeNotifier = Quote.LastSizeNotifier(self)
        self.bid = ''
        self.bidNotifier = Quote.BidNotifier(self)
        self.ask = ''
        self.askNotifier = Quote.AskNotifier(self)
        self.bid_size = ''
        self.bidSizeNotifier = Quote.BidSizeNotifier(self)
        self.ask_size = ''
        self.askSizeNotifier = Quote.AskSizeNotifier(self)
        self.high = ''
        self.highNotifier = Quote.HighNotifier(self)
        self.low = ''
        self.lowNotifier = Quote.LowNotifier(self)
        self.volume = ''
        self.volumeNotifier = Quote.VolumeNotifier(self)
        self.open = ''
        self.openNotifier = Quote.OpenNotifier(self)
        self.previous_close = ''
        self.previousCloseNotifier = Quote.PreviousCloseNotifier(self)
        self.unofficial_close = ''
        self.unofficialCloseNotifier = Quote.UnofficialCloseNotifier(self)
        self.tick_val = ''
        self.tickValNotifier = Quote.TickValNotifier(self)
        self.news = ''
        self.newNotifier = Quote.NewsNotifier(self)
        self.vwap = ''
        self.vwapNotifier = Quote.VWAPNotifier(self)
        self.vwap_10 = ''
        self.vwap_exchange = ''

    def __str__(self):
        return 'symbol: {0}\nbid: {1}\nask: {2}\nbid size: {3}\nask size: {4}\nprevious close: {5}\nopen: {6}\nhigh: {7}\nlow: {8}\nlast: {9}\ntick val: {10}\nlast size: {11}\nunofficial close: {12}\nvolume: {13}\nnews: {14}\nvwap from open: {15}\nvwap 10 minute: {16}\nvwap exchange: {17}'.format(
            self.symbol,
            self.bid,
            self.ask,
            self.bid_size,
            self.ask_size,
            self.previous_close,
            self.open,
            self.high,
            self.low,
            self.last,
            self.tick_val,
            self.last_size,
            self.unofficial_close,
            self.volume,
            self.news,
            self.vwap,
            self.vwap_10,
            self.vwap_exchange
        )

    def change(self):  # this is how to notify change
        self.changeNotifier.notifyObservers()

    def set_last(self, value):
        self.last = value
        self.lastNotifier.notifyObservers(value)

    def set_last_size(self, value):
        self.last_size = value
        self.lastSizeNotifier.notifyObservers(value)

    def set_bid(self, value):
        self.bid = value
        self.bidNotifier.notifyObservers(value)

    def set_ask(self, value):
        self.ask = value
        self.askNotifier.notifyObservers(value)

    def set_bid_size(self, value):
        self.bid_size = value
        self.bidSizeNotifier.notifyObservers(value)

    def set_ask_size(self, value):
        self.ask_size = value
        self.askSizeNotifier.notifyObservers(value)

    def set_high(self, value):
        self.high = value
        self.highNotifier.notifyObservers(value)

    def set_low(self, value):
        self.low = value
        self.lowNotifier.notifyObservers(value)

    def set_volume(self, value):
        self.volume = value
        self.volumeNotifier.notifyObservers(value)

    def set_open(self, value):
        self.open = value
        self.openNotifier.notifyObservers(value)

    def set_previous_close(self, value):
        self.previous_close = value
        self.previousCloseNotifier.notifyObservers(value)

    def set_unofficial_close(self, value):
        self.unofficial_close = value
        self.unofficialCloseNotifier.notifyObservers(value)

    def set_tick_val(self, value):
        self.tick_val = value
        self.tickValNotifier.notifyObservers(value)

    def set_news(self, value):
        self.news = value
        self.newNotifier.notifyObservers(value)

    def set_vwap(self, value):
        self.vwap = value
        self.vwapNotifier.notifyObservers(value)

    def set_vwap_10(self, value):
        self.vwap_10 = value

    def set_vwap_exchange(self, value):
        self.vwap_exchange = value

    def get_symbol(self):
        return self.symbol

    def get_last_str(self):
        return self.last

    def get_last_size_str(self):
        return self.last_size

    def get_bid_str(self):
        return self.bid

    def get_ask_str(self):
        return self.ask

    def get_bid_size_str(self):
        return self.bid_size

    def get_ask_size_str(self):
        return self.ask_size

    def get_high_str(self):
        return self.high

    def get_low_str(self):
        return self.low

    def get_volume_str(self):
        return self.volume

    def get_open_str(self):
        return self.open

    def get_previous_close_str(self):
        return self.previous_close

    def get_unofficial_close_str(self):
        return self.unofficial_close

    def get_tick_val_str(self):
        return self.tick_val

    def get_news_str(self):
        return self.news

    def get_vwap_str(self):
        return self.vwap

    def get_vwap_10_str(self):
        return self.vwap_10

    def get_vwap_exchange(self):
        return self.vwap_exchange

    def convert_to_int(self, val):
        try:
            return int(val)
        except:
            return None

    def convert_to_float(self, val):
        try:
            return float(val)
        except:
            return None

    def get_last(self):
        return self.convert_to_float(self.last)

    def get_last_size(self):
        return self.convert_to_int(self.last_size)

    def get_bid(self):
        return self.convert_to_float(self.bid)

    def get_ask(self):
        return self.convert_to_float(self.ask)

    def get_bid_size(self):
        return self.convert_to_int(self.bid_size)

    def get_ask_size(self):
        return self.convert_to_int(self.ask_size)

    def get_high(self):
        return self.convert_to_float(self.high)

    def get_low(self):
        return self.convert_to_float(self.low)

    def get_volume(self):
        return self.convert_to_int(self.volume)

    def get_open(self):
        return self.convert_to_float(self.open)

    def get_previous_close(self):
        return self.convert_to_float(self.previous_close)

    def get_unofficial_close(self):
        return self.convert_to_float(self.unofficial_close)

    def get_tick_val(self):
        return self.convert_to_int(self.tick_val)

    def get_news(self):
        return self.convert_to_int(self.news)

    def get_vwap(self):
        return self.convert_to_float(self.vwap)

    def get_vwap_10(self):
        return self.convert_to_float(self.vwap_10)

    class ChangeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class LastNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class LastSizeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class BidNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class AskNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class BidSizeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class AskSizeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class HighNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class LowNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class VolumeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class OpenNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class VolumeNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class OpenNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class PreviousCloseNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class UnofficialCloseNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class TickValNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class NewsNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

    class VWAPNotifier(Observable):

        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, arg=None):
            self.setChanged()
            Observable.notifyObservers(self, arg)

