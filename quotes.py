import threading
from quote import Quote


class Quotes(dict):
    """
    quote object collection
    """

    def __init__(self):
        self.lock = threading.Lock()

    def get_quote(self, symbol):
        """
        If the quote object is not there it will be created.
        :param symbol:
        :return: a quote object for the symbol
        """
        q = None
        with self.lock:
            if symbol in self:
                q = self[symbol]

        return q

    def add_quote(self, symbol):

        with self.lock:
            if not symbol in self:
                q = Quote(symbol)
                self[symbol] = q

        return q

    def delete_quote(self, symbol):

        with self.lock:
            if symbol in self:
                del self[symbol]

    def count(self):
        return len(self)


