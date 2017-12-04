import socket
import Queue
import time
import threading
from quotes import *
from quote_updater import *
from hydra_message_utility_functions import *


class HAPIInformationServer(object):
    """
    manages information server communication
    """

    def __init__(self):
        is_server_address = ('localhost', 10001)
        self.is_msg_count = 0
        self.quotes = Quotes()
        self.is_quit_program = False
        self.is_queue = Queue.Queue()
        self.is_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_sock.connect(is_server_address)
        self.is_msg_store = list()
        self.is_listener_thread = threading.Thread(target=self.is_socket_listener)
        self.is_listener_thread.start()
        self.is_processor_thread = threading.Thread(target=self.is_queue_processor)
        self.is_processor_thread.start()

    def is_quit(self):
        self.is_quit_program = True

    def is_msg_handler(self, msg):
        # self.is_msg_count += 1
        # self.is_msg_store.append(msg)
        tokens = msg.split(':')
        quote = self.quotes.get_quote(tokens[4])
        if quote == None:
            quote = self.quotes.add_quote(tokens[4])
        update_quote(quote, tokens)

    def is_socket_listener(self):
        while True:
            try:
                self.is_sock.settimeout(1)
                header = self.is_sock.recv(13)
                if len(header) > 0:
                    toks = header.split(':')
                    length = int(toks[3]) - 13
                    remainder = self.is_sock.recv(length)
                    whole_message = header + remainder
                    self.is_queue.put(whole_message)
            except socket.timeout:
                if self.is_quit_program:
                    self.is_sock.close()
                    break
            except:
                if self.is_quit_program:
                    self.is_sock.close()
                    break
            finally:
                if self.is_quit_program:
                    self.is_sock.close()
                    break

    def is_queue_processor(self):
        while True:
            try:
                msg = self.is_queue.get(block=True, timeout=1)
                self.is_msg_handler(msg)
                self.is_queue.task_done()
                if self.is_quit_program:
                    break
            except Queue.Empty:
                if self.is_quit_program:
                    break

    def send_is_quit_message(self):
        # sends quit message to IS server
        msg = 'QUIT'
        self.is_sock.sendall(msg)

    def close_is_socket(self):
        self.send_is_quit_message()
        time.sleep(1)
        self.is_sock.close()
        self.is_quit_program = True
        self.is_listener_thread.join()
        self.is_processor_thread.join()

    def is_submit_dialogue(self):
        message_to_submit = raw_input('message to submit: ')
        message_to_submit = add_length(message_to_submit)
        self.is_sock.sendall(message_to_submit)

    def start_quote(self, symbol):
        # sends a request to start a quote subscription
        # e.g. quote SPY
        q = self.quotes.get_quote(symbol)
        if q == None:
            q = self.quotes.add_quote(symbol)
        if q.is_live:
            return
        q.is_live = True
        message = '#:00000:1:000:{0}:A:*'.format(symbol)
        message = add_length(message)
        self.is_sock.sendall(message)
        return q

    def stop_quote(self, symbol):
        q = self.quotes.get_quote(symbol)
        if not q.is_live:
            return
        if not q.has_observers():
            q.is_live = False
            message = '#:00000:1:000:{0}:R:*'.format(symbol)
            message = add_length(message)
            self.is_sock.sendall(message)
            self.quotes.delete_quote(symbol)

    def print_quote(self, command):
        tokens = command.split(' ')
        if len(tokens) == 3:
            q = self.quotes.get_quote(tokens[2])
            print str(q)

