import socket
import Queue
import threading
from quotes import *
from hydra_message_utility_functions import *

is_sock = 0
is_server_address = ('localhost', 10001)
is_queue = 0
is_msg_store = 0
is_msg_count = 0
is_listener_thread = 0
is_processor_thread = 0

is_quit_program = False


def is_quit():
    global is_quit_program
    is_quit_program = True


def get_quote_object(symbol):
    if symbol in quotes:
        return quotes[symbol]
    q = Quote(symbol)
    quotes[symbol] = q
    return q


def is_msg_handler(msg):
    global is_msg_count
    is_msg_count += 1
    is_msg_store.append(msg)
    tokens = msg.split(':')
    # tokens[2] is message type
    # tokens[4] is symbol
    if tokens[2] == 'A':
        q = get_quote_object(tokens[4])
        q.set_ask(tokens[5])
        q.set_ask_size(tokens[6])
        q.set_tick_val(tokens[7])
    elif tokens[2] == 'B':
        q = get_quote_object(tokens[4])
        q.set_bid(tokens[5])
        q.set_bid_size(tokens[6])
        q.set_tick_val(tokens[7])
    elif tokens[2] == 'J':
        q = get_quote_object(tokens[4])
        q.set_last(tokens[5])
        q.set_last_size(tokens[6])
    elif tokens[2] == 'C':
        q = get_quote_object(tokens[4])
        q.set_bid(tokens[5])
        q.set_bid_size(tokens[6])
        q.set_ask(tokens[7])
        q.set_ask_size(tokens[8])
        q.set_tick_val(tokens[9])
    elif tokens[2] == 'D':
        q = get_quote_object(tokens[4])
        q.set_high(tokens[5])
    elif tokens[2] == 'K':
        q = get_quote_object(tokens[4])
        q.set_low(tokens[5])
    elif tokens[2] == 'F':
        q = get_quote_object(tokens[4])
        q.set_open(tokens[5])
    elif tokens[2] == 'G':
        q = get_quote_object(tokens[4])
        q.set_previous_close(tokens[5])
    elif tokens[2] == 'H':
        q = get_quote_object(tokens[4])
        q.set_volume(tokens[5])
    elif tokens[2] == 'V':
        q = get_quote_object(tokens[4])
        q.set_vwap(tokens[5])
        q.set_vwap_exchange(tokens[6])
        q.set_vwap_10(tokens[7])
    elif tokens[2] == 'N':
        q = get_quote_object(tokens[4])
        q.set_unofficial_close(tokens[5])
    elif tokens[2] == '1':
        # level 1 data
        q = get_quote_object(tokens[4])
        q.set_last(tokens[5])
        q.set_bid(tokens[6])
        q.set_bid_size(tokens[7])
        q.set_ask(tokens[8])
        q.set_ask_size(tokens[9])
        q.set_high(tokens[10])
        q.set_low(tokens[11])
        q.set_volume(tokens[12])
        q.set_open(tokens[13])
        q.set_previous_close(tokens[14])
        q.set_tick_val(tokens[15])
        q.set_news(tokens[16])
        q.set_vwap(tokens[17])
        q.set_vwap_10(tokens[18])


def is_socket_listener():
    while True:
        try:
            is_sock.settimeout(1)
            header = is_sock.recv(13)
            if len(header) > 0:
                toks = header.split(':')
                length = int(toks[3]) - 13
                remainder = is_sock.recv(length)
                whole_message = header + remainder
                global es_queue
                is_queue.put(whole_message)
        except socket.timeout:
            if is_quit_program:
                is_sock.close()
                break
        except:
            if is_quit_program:
                is_sock.close()
                break
        finally:
            if is_quit_program:
                is_sock.close()
                break


def is_queue_processor():
    while True:
        try:
            msg = is_queue.get(block=True, timeout=1)
            is_msg_handler(msg)
            is_queue.task_done()
            if is_quit_program:
                break
        except Queue.Empty:
            if is_quit_program:
                break


def send_is_quit_message():
    # sends quit message to IS server
    msg = '#:00000:0:018:QUIT'
    is_sock.sendall(msg)


def is_initialize():
    global is_queue
    is_queue = Queue.Queue()
    global is_sock
    is_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_sock.connect(is_server_address)
    global is_msg_store
    is_msg_store = list()
    initialize_quotes()
    global is_listener_thread
    is_listener_thread = threading.Thread(target=is_socket_listener)
    is_listener_thread.start()
    global is_processor_thread
    is_processor_thread = threading.Thread(target=is_queue_processor)
    is_processor_thread.start()


def close_is_socket():
    is_sock.close()
    is_listener_thread.join()
    is_processor_thread.join()


def is_submit_dialogue():
    message_to_submit = raw_input('message to submit: ')
    message_to_submit = add_length(message_to_submit)
    is_sock.sendall(message_to_submit)


def start_quote(command):
    # sends a request to start a quote subscription
    # kill command will then kill a quote if it exists
    # e.g. quote SPY
    tokens = command.split(' ')
    symbol = tokens[2].strip()
    message = '#:00000:1:000:{0}:A:*'.format(symbol)
    message = add_length(message)
    is_sock.sendall(message)


def stop_quote(command):
    tokens = command.split(' ')
    symbol = tokens[2].strip()
    message = '#:00000:1:000:{0}:R:*'.format(symbol)
    message = add_length(message)
    is_sock.sendall(message)


def print_quote(command):
    tokens = command.split(' ')
    if len(tokens) == 3:
        q = get_quote_object(tokens[2])
        print str(q)

