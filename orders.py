import threading

class Orders(object):

    def __init__(self):
        self.orders_by_id = dict()
        self.orders_by_parent = dict()
        self.by_id_lock = threading.Lock()
        self.by_parent_lock = threading.Lock()

    def add_order_by_id(self, order_id, o):
        with self.by_id_lock:
            self.orders_by_id[str(order_id)] = o

    def add_order_by_parent(self, order_id, o):
        with self.by_parent_lock:
            self.orders_by_parent[str(order_id)] = o

    def get_order_by_id(self, order_id):
        if order_id in self.orders_by_id:
            return self.orders_by_id[order_id]
        else:
            return None

    def get_order_by_parent(self, order_id):
        if order_id in self.orders_by_parent.keys():
            return self.orders_by_parent[order_id]
        else:
            return None

    def print_orders(self):
        with self.by_parent_lock:
            print self.orders_by_parent
        with self.by_id_lock:
            print self.orders_by_id


