"""
test using Execution Manager
"""
import time
from hydra_execution_manager import HydraExecutionManager
from order_factory import OrderFactory

def call_back(arg):
    print arg

em = HydraExecutionManager(False)
em.open_socket()
OF = OrderFactory()
o = OF.buy('buy 100 NOK 4.8 day DEMOX1')
em.send_order(o)
time.sleep(1)
em.cancel_all_orders()
o = OF.buy('buy 100 NOK 4.8 day DEMOX1')
em.send_order(o)
time.sleep(1)
em.cancel_order(o)
em.close_socket()
print 'done'
