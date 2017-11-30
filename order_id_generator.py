import datetime

class OrderIdGenerator(object):

    def __init__(self):
        self.order_number = 100

    def generate_order_id(self):
        """
        :return:order id string
        """

        self.order_number += 1
        if self.order_number == 999:
            self.order_number = 100
        return int('{:%H%M%S}{}'.format(datetime.datetime.now(), self.order_number))