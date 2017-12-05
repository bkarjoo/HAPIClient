from quote_manager import *
from quote import Quote
import time
from hapi_information_server import HAPIInformationServer


class HydraQuoteManager(QuoteManager):
    """
    adaptor class to connect to hydra
    """
    def __init__(self, auto_start = True):
        super(HydraQuoteManager, self).__init__()
        self.iserver = 0
        if auto_start:
            self.open_socket()

    def start_quote_stream(self, symbol):
        """
        :param symbol:
        :return: the quote object
        """
        q = self.iserver.start_quote(symbol)
        return q

    def stop_quote_stream(self, symbol):
        self.iserver.stop_quote(symbol)

    def open_socket(self):
        self.iserver = HAPIInformationServer()

    def close_socket(self):
        self.iserver.close_is_socket()
        self.iserver = 0 
