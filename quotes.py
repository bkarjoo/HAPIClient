from quote import Quote


class Quotes(dict):
    """
    quote object collection
    """

    def __init__(self):
        pass

    def get_quote(self, symbol):
        """
        If the quote object is not there it will be created.
        :param symbol:
        :return: a quote object for the symbol
        """
        if symbol in self:
            return self[symbol]

        q = Quote(symbol)
        self[symbol] = q
        return q


# q = Quotes()
# q.get_quote('IBM')
# IBM = q.get_quote('IBM')
# IBM.set_last(123)
# print IBM