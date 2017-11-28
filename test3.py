"""
connect to IS server and the disconnect
use HAPIInformationServer
make sure it will exit gracefully in case of error
means it sends a disconnect message
"""
import time
from hydra_quote_manager import HydraQuoteManager

print 'call IS constructor'
qm = HydraQuoteManager(False)
qm.open_socket()
print qm
q = qm.start_quote_stream('SPY')
q2 = qm.start_quote_stream('AAPL')
time.sleep(3)
print q
print q2
qm.stop_quote_stream('SPY')
qm.stop_quote_stream('AAPL')
time.sleep(1)
print 'close socket'
qm.close_socket()
print 'done'
