import socket
import Queue
import time
import threading
from order import *
from orders import Orders
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
        self.orders = Orders()
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
                o = self.orders.get_order_by_id(tokens[8])
                if o is not None:
                    o.update_order(tokens)
                pass
            elif tokens[4] == 'F':
                # find order by parent id

                o = self.orders.get_order_by_parent(tokens[6])
                if o is not None:
                    o.order_id = tokens[9]
                    self.orders.add_order_by_id(tokens[9], o)
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
                    remainder = self.es_sock.recv(length)
                    whole_message = header + remainder
                    self.es_queue.put(whole_message)
            except socket.timeout:
                if self.es_quit_program:
                    self.es_sock.close()
                    break
            except:
                if self.es_quit_program:
                    self.es_sock.close()
                    break
            finally:
                if self.es_quit_program:
                    self.es_sock.close()
                    break

    def es_queue_processor(self):
        while True:
            try:
                msg = self.es_queue.get(block=True, timeout=1)
                self.es_msg_handler(msg)
                self.es_queue.task_done()
                if self.es_quit_program:
                    break
            except Queue.Empty:
                if self.es_quit_program:
                    break

    def send_message_to_es(self, msg):
        self.es_sock.sendall(msg)

    def send_es_quit_message(self):
        # sends quit message to ES server
        #msg = '#:00000:0:018:QUIT'
        msg = 'QUIT'
        self.es_sock.sendall(msg)

    def close_es_socket(self):
        self.send_es_quit_message()
        time.sleep(1)
        self.es_quit_program = True
        self.es_sock.close()
        self.es_listener_thread.join()
        self.es_processor_thread.join()

    def es_submit_dialogue(self):
        message_to_submit = raw_input('message to submit: ')
        message_to_submit = add_length(message_to_submit)
        self.es_sock.sendall(message_to_submit)

    def submit_order(self, o):
        self.orders.add_order_by_parent(o.parent_id, o)
        hydra_order_message = o.craft_message()
        hydra_order_message = add_length(hydra_order_message)
        self.es_sock.sendall(hydra_order_message)

    def cancel_order(self, o):
        hydra_cancel_message = o.craft_cancel_message()
        hydra_cancel_message = add_length(hydra_cancel_message)
        self.es_sock.sendall(hydra_cancel_message)

    def print_order_status(self):
        for key, value in self.orders.orders_by_id.iteritems():
            print value.status

    def cancel_all_orders(self):
        print len(self.orders.orders_by_id)
        cancel_msgs = list()
        with self.orders.by_id_lock:

            for key, value in self.orders.orders_by_id.iteritems():
                if value.status == order_status_type.open or value.status == order_status_type.partial_open:
                    cancel_msg = value.craft_cancel_message()
                    cancel_msg = add_length(cancel_msg)
                    cancel_msgs.append(cancel_msg)
        for m in cancel_msgs:
            self.es_sock.sendall(m)
            time.sleep(.15)

