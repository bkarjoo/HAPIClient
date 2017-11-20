class Quote(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.last = ''
        self.last_size = ''
        self.bid = ''
        self.ask = ''
        self.bid_size = ''
        self.ask_size = ''
        self.high = ''
        self.low = ''
        self.volume = ''
        self.open = ''
        self.previous_close = ''
        self.unofficial_close = ''
        self.tick_val = ''
        self.news = ''
        self.vwap = ''
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

    def set_last(self, value):
        self.last = value

    def set_last_size(self, value):
        self.last_size = value

    def set_bid(self, value):
        self.bid = value
        
    def set_ask(self, value):
        self.ask = value
        
    def set_bid_size(self, value):
        self.bid_size = value
        
    def set_ask_size(self, value):
        self.ask_size = value
        
    def set_high(self, value):
        self.high = value
        
    def set_low(self, value):
        self.low = value
        
    def set_volume(self, value):
        self.volume = value
        
    def set_open(self, value):
        self.open = value
        
    def set_previous_close(self, value):
        self.previous_close = value

    def set_unofficial_close(self, value):
        self.unofficial_close = value
        
    def set_tick_val(self, value):
        self.tick_val = value
        
    def set_news(self, value):
        self.news = value
        
    def set_vwap(self, value):
        self.vwap = value
        
    def set_vwap_10(self, value):
        self.vwap_10 = value

    def set_vwap_exchange(self, value):
        self.vwap_exchange = value

    def get_last(self):
        return self.last

    def get_last_size(self):
        return self.last_size

    def get_bid(self):
        return self.bid

    def get_ask(self):
        return self.ask

    def get_bid_size(self):
        return self.bid_size

    def get_ask_size(self):
        return self.ask_size

    def get_high(self):
        return self.high

    def get_low(self):
        return self.low

    def get_volume(self):
        return self.volume

    def get_open(self):
        return self.open

    def get_previous_close(self):
        return self.previous_close

    def get_unofficial_close(self):
        return self.unofficial_close

    def get_tick_val(self):
        return self.tick_val

    def get_news(self):
        return self.news

    def get_vwap(self):
        return self.vwap

    def get_vwap_10(self):
        return self.vwap_10

    def get_vwap_exchange(self):
        return self.vwap_exchange