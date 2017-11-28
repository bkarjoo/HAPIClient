from execution_manager import *
from hapi_execution_server import HAPIExecutionServer

class HydraExecutionManager(ExecutionManager):

    def __init__(self, autostart = True):
        super(HydraExecutionManager, self).__init__()
        self.es_server = 0
        if autostart:
            self.open_socket()

    def open_socket(self):
        self.es_server = HAPIExecutionServer()

    def close_socket(self):
        self.es_server.close_es_socket()

    def send_order(self, order):
        self.es_server.submit_order(order)

    def cancel_order(self, order):
        self.es_server.cancel_order(order)

    def cancel_all_orders(self):
        self.es_server.cancel_all_orders()