import threading
import time
from order import *

from excel_quotes import *

from execution_server import *
from information_server import *
from google_sheet_dtp import *

def quit():
    send_es_quit_message()
    send_is_quit_message()
    es_quit()
    is_quit()
    close_es_socket()
    close_is_socket()
    time.sleep(1)


def interactive():
        while True:
            try:
                command = raw_input('')

                if command == 'q':
                    quit()
                    return
                elif command[:4] == 'sell':
                    sell(command)
                elif command[:3] == 'buy':
                    buy(command)
                elif command == 'submit':
                    es_submit_dialogue()
                elif command == 'sheet':
                    process_sheet()
                elif command == 'pem':
                    for m in es_msg_store:
                        print m
                elif command == 'pim':
                    for m in is_msg_store:
                        print m
                elif command == 'pemc':
                    print es_msg_count
                elif command == 'pimc':
                    print is_msg_count
                elif command[:11] == 'start quote':
                    start_quote(command)
                elif command[:10] == 'stop quote':
                    stop_quote(command)
                elif command == 'closing bracket orders':
                    closing_bracket_orders()
                elif command[:11] == 'print quote':
                    print_quote(command)
                elif command == 'print orders':
                    print_orders()
                elif command == 'print status':
                    print_order_status()
                elif command == 'cancel all orders':
                    cancel_all_orders()
                elif command[:9] == 'print row':
                    tokens = command.split()
                    print_row(int(tokens[2]))
                elif command[:11] == 'process row':
                    tokens = command.split()
                    i = int(tokens[2])
                    process_row(get_row(i),i)
            except:
                print 'error in interactive'


if __name__ == "__main__":
    is_initialize()
    es_initialize()
    interactive()






