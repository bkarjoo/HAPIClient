from order import *

orders_by_id = 0
orders_by_parent = 0

def initialize_orders():
    global orders_by_id
    orders_by_id = dict()
    global orders_by_parent
    orders_by_parent = dict()


def add_order_by_id(id, o):
    orders_by_id[id] = o


def add_order_by_parent(id, o):
    orders_by_parent[id] = o


def get_order_by_id(id):
    if id in orders_by_id:
        return orders_by_id[id]
    else:
        return None


def get_order_by_parrent(id):
    if id in orders_by_parent:
        return orders_by_parent[id]
    else:
        return None


def print_orders():
    print orders_by_id
    print orders_by_parent
