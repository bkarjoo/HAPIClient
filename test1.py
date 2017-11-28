"""
connect to IS server and the disconnect
use HAPIInformationServer
make sure it will exit gracefully in case of error
means it sends a disconnect message
"""
import time
from hapi_information_server import HAPIInformationServer

print 'call IS constructor'
IS = HAPIInformationServer()
print IS
q = IS.start_quote('SPY')
q2 = IS.start_quote('AAPL')
time.sleep(3)
print q
print q2
IS.stop_quote('SPY')
IS.stop_quote('AAPL')
time.sleep(1)
print 'close socket'
IS.close_is_socket()
print 'done'
