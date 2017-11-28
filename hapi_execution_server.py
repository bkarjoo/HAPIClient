import socket
import Queue
from orders import *
from hydra_message_utility_functions import *


class HAPIExecutionServer(object):

    def __init__(self):
        es_server_address = ('localhost', 10000)
        self.es_msg_count = 0
        self.es_listener_thread = 0
        self.es_processor_thread = 0
        self.es_quit_program = False
        self.es_queue = Queue.Queue()
        self.es_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.es_sock.connect(es_server_address)
        self.es_msg_store = list()
        initialize_orders()
        self.es_listener_thread = threading.Thread(target=self.es_socket_listener)
        self.es_listener_thread.start()
        self.es_processor_thread = threading.Thread(target=self.es_queue_processor)
        self.es_processor_thread.start()

    def es_quit(self):
        self.es_quit_program = True

    def es_msg_handler(self, msg):
        self.es_msg_count += 1
        self.es_msg_store.append(msg)
        tokens = msg.split(':')
        # if order is not found on the dictionary nothing is done
        # so place your order on the dictionary before sending

        if tokens[2] == 'S':
            if tokens[4] == 'S':
                # find order by Hydra id
                o = get_order_by_id(tokens[8])
                if o is not None:
                    o.update_order(tokens)
                pass
            elif tokens[4] == 'F':
                # find order by parent id
                o = get_order_by_parrent(tokens[6])
                if o is not None:
                    o.order_id = tokens[9]
                    add_order_by_id(tokens[9], o)
                    o.update_order(tokens)
                pass

    def es_socket_listener(self):
        while True:
            try:
                self.es_sock.settimeout(1)
                header = self.es_sock.recv(13)
                if len(header) > 0:
                    tokens = header.split(':')
                    length = int(tokens[3]) - 13
                    remainder = es_sock.recv(length)
                    whole_message = header + remainder
                    es_queue.put(whole_message)
            except socket.timeout:
                if self.es_quit_program:
                    es_sock.close()
                    break
            except:
                if self.es_quit_program:
                    es_sock.close()
                    break
            finally:
                if self.es_quit_program:
                    es_sock.close()
                    break

    def es_queue_processor(self):
        while True:
            try:
                msg = es_queue.get(block=True, timeout=1)
                self.es_msg_handler(msg)
                es_queue.task_done()
                if self.es_quit_program:
                    break
            except Queue.Empty:
                if self.es_quit_program:
                    break

    def send_message_to_es(self, msg):
        self.es_sock.sendall(msg)

    def send_es_quit_message(self):
        # sends quit message to ES server
        msg = '#:00000:0:018:QUIT'
        self.es_sock.sendall(msg)

    def close_es_socket(self):
        self.es_sock.close()
        self.es_listener_thread.join()
        self.es_processor_thread.join()

    def es_submit_dialogue(self):
        message_to_submit = raw_input('message to submit: ')
        message_to_submit = add_length(message_to_submit)
        self.es_sock.sendall(message_to_submit)

    def sell(self, command):
        try:
            """sell 100 XYZ 23.50 day ALGOPAIR"""
            """sell 100 XYZ 23.50 loo ALGOSYND"""
            """sell 100 XYZ moo ALGOGROUP"""
            """sell 100 XYZ vwap 23.5 stop ALGOSYND"""
            """sell 100 XYZ vwap 23.5 * 0.99 stop ALGOGROUP"""
            values = command.split(' ')
            qty = int(values[1])
            # -qty means sell
            qty = qty * -1
            o = Order()
            acct = 'ALGOGROUP'
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = generate_opg_market_order(qty, values[2], acct)
            elif values[3].upper() == 'MOC':
                if len(values) == 5:
                    acct = values[4]
                o = generate_moc_market_order(qty, values[2], acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier, 2)
                    if len(values) == 9:
                        acct = values[8]
                    o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', values[4], acct)
            elif values[4].upper() == 'LOO':
                if len(values) == 6:
                    acct = values[5]
                o = generate_opg_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'LOC':
                if len(values) == 6:
                    acct = values[5]
                o = generate_loc_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = generate_stop_limit_order(qty, values[2], values[3], values[5], acct)

            hydra_order_message = o.craft_message()
            hydra_order_message = add_length(hydra_order_message)
            self.es_sock.sendall(hydra_order_message)
            # print hydra_order_message
        except Exception as e:
            print e

    def buy(self, command):
        try:
            """buy 100 XYZ 23.50 day (ALGOPAI)"""
            """buy 100 XYZ 23.50 loo (ALGOSYND)"""
            """buy 100 XYZ moo (ALGOGROUP)"""
            """buy 100 XYZ 23.5 stop 23.75 limit (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 stop (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 * 1.01 stop (ALGOGROUP)"""
            values = command.split(' ')

            o = Order()
            acct = 'ALGOGROUP'
            if len(values) == 4: values.append(acct)
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = generate_opg_market_order(values[1], values[2], acct)
            elif values[3].upper() == 'MOC':
                if len(values) == 5:
                    acct = values[4]
                o = generate_moc_market_order(values[1], values[2], acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier, 2)
                    if len(values) == 9:
                        acct = values[8]
                    o = generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', values[4], acct)
            elif values[4].upper() == 'LOO':
                if len(values) == 6:
                    acct = values[5]
                o = generate_opg_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'LOC':
                if len(values) == 6:
                    acct = values[5]
                o = generate_loc_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = generate_stop_limit_order(values[1], values[2], values[3], values[5], acct)

            add_order_by_parent(o.parent_id, o)

            hydra_order_message = o.craft_message()
            hydra_order_message = add_length(hydra_order_message)

            self.es_sock.sendall(hydra_order_message)
            print hydra_order_message
        except Exception as e:
            print 'error encountered in buy function:\n{}'.format(e)

    def print_order_status(self):
        for key, value in orders_by_id.iteritems():
            print value.status

    def cancel_all_orders(self):
        for key, value in orders_by_id.iteritems():
            if value.status == order_status_type.open or value.status == order_status_type.partial_open:
                cancel_msg = value.craft_cancel_message()
                cancel_msg = add_length(cancel_msg)
                print cancel_msg
                self.es_sock.sendall(cancel_msg)

