
class Orders(object):

    def __init__(self):
        self.orders_by_id = dict()
        self.orders_by_parent = dict()

    def add_order_by_id(self, order_id, o):
        self.orders_by_id[order_id] = o

    def add_order_by_parent(self, order_id, o):
        self.orders_by_parent[order_id] = o

    def get_order_by_id(self, order_id):
        if order_id in self.orders_by_id:
            return self.orders_by_id[order_id]
        else:
            return None

    def get_order_by_parent(self, order_id):
        if order_id in self.orders_by_parent:
            return self.orders_by_parent[order_id]
        else:
            return None

    def print_orders(self):
        print self.orders_by_id
        print self.orders_by_parent
