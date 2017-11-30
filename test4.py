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
time.sleep(1)
o = OF.buy('buy 100 NOK 4.8 day DEMOX1')
em.send_order(o)
time.sleep(1)
em.cancel_order(o)
time.sleep(1)
# 10 orders
for i in range(0,9):
    o = OF.buy('sell 100 NOK 5.03 day DEMOX1')
    em.send_order(o)
    time.sleep(.1)
time.sleep(1)
#em.cancel_all_orders()
print 'done canceling'
time.sleep(1)
em.close_socket()
print 'done'

# note open send cancel cancel_all , finally close
# all open and close crucial in using the execution manager