import time
from hapi_information_server import HAPIInformationServer
from hapi_execution_server import HAPIExecutionServer
from hydra_execution_manager import HydraExecutionManager
from order_factory import OrderFactory
from google_sheet_dtp import *
from hydra_quote_manager import HydraQuoteManager


em = 0
of = 0
info_serve = 0

def quit():
    em.close_socket()
    info_serve.close_is_socket()
    time.sleep(1)


def interactive():
        while True:
            try:
                command = raw_input('')

                if command == 'q':
                    quit()
                    return
                elif command[:4] == 'sell':
                    o = of.sell(command)
                    em.send_order(o)
                elif command[:3] == 'buy':
                    o = of.buy(command)
                    em.send_order(o)
                elif command == 'submit':
                    ES.es_submit_dialogue()
                elif command == 'sheet':
                    ggg = GoogleSheetDailyTradingProcedure(of,em)
                    ggg.process_sheet()
                elif command == 'pem':
                    for m in ES.es_msg_store:
                        print m
                elif command == 'pim':
                    for m in IS.is_msg_store:
                        print m
                elif command == 'pemc':
                    print ES.es_msg_count
                elif command == 'pimc':
                    print IS.is_msg_count
                elif command[:11] == 'start quote':
                    info_serve.start_quote(command.split(' ')[2])
                elif command[:10] == 'stop quote':
                    info_serve.stop_quote(command.split(' ')[2])
                # elif command == 'closing bracket orders':
                #     closing_bracket_orders()
                elif command[:11] == 'print quote':
                    IS.print_quote(command)
                elif command == 'print orders':
                    ES.print_orders()
                elif command == 'print status':
                    ES.print_order_status()
                elif command == 'cancel all orders':
                    ES.cancel_all_orders()
                elif command[:9] == 'print row':
                    tokens = command.split()
                    print_row(int(tokens[2]))
                elif command[:11] == 'process row':
                    tokens = command.split()
                    i = int(tokens[2])
                    process_row(get_row(i),i)
                elif command == 'tech':
                    pass
            except Exception as e:
                print 'error in interactive', e


if __name__ == "__main__":
    em = HydraExecutionManager()
    of = OrderFactory()
    info_serve = HAPIInformationServer()
    interactive()







