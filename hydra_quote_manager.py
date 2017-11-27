from quote_manager import *
from quote import Quote

class HydraQuoteManager(QuoteManager):
    """
    adaptor class to connect to hydra
    """
    def __init__(self, information_server):
        super(HydraQuoteManager, self).__init__()
        self.iserver = information_server

    def start_quote_stream(self, symbol):
        """
        :param symbol:
        :return: the quote object
        """
        q = self.iserver.get_quote_object(symbol)
        return q


    def stop_quote_stream(self, symbol):
        pass