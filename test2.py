"""
connect to es server and disconnect
enter an order to buy NOK
"""
import time
from hapi_execution_server import HAPIExecutionServer
from order_factory import OrderFactory

def call_back(arg):
    print arg

ES = HAPIExecutionServer()
print ES
OF = OrderFactory()
o = OF.buy('buy 100 NOK 4.8 day DEMOX1')
ES.submit_order(o)
time.sleep(1)
ES.cancel_all_orders()
ES.close_es_socket()
print 'done'

# all these details are hidden by the execution manager
