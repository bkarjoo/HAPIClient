from quote import Quote

class Quotes(dict):
    """
    a dictionary collection of quotes
    """

    def __init__(self):
        pass

    def get_quote(self, symbol):

        if symbol in self:
            return self[symbol]

        q = Quote(symbol)
        self[symbol] = q
        return q


q = Quotes()
q.get_quote('IBM')
IBM = q.get_quote('IBM')
IBM.set_last(123)
print IBM