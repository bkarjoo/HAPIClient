import socket
import Queue
from orders import *
from hydra_message_utility_functions import *


es_sock = 0
es_server_address = ('localhost', 10000)
es_queue = 0
es_msg_store = 0
es_msg_count = 0
es_listener_thread = 0
es_processor_thread = 0

es_quit_program = False


def es_quit():
    global es_quit_program
    es_quit_program = True


def es_msg_handler(msg):
    global es_msg_count
    es_msg_count += 1
    es_msg_store.append(msg)
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


def es_socket_listener():
    while True:
        try:
            es_sock.settimeout(1)
            header = es_sock.recv(13)
            if len(header) > 0:
                toks = header.split(':')
                length = int(toks[3]) - 13
                remainder = es_sock.recv(length)
                whole_message = header + remainder
                global es_queue
                es_queue.put(whole_message)
        except socket.timeout:
            if es_quit_program:
                es_sock.close()
                break
        except:
            if es_quit_program:
                es_sock.close()
                break
        finally:
            if es_quit_program:
                es_sock.close()
                break


def es_queue_processor():
    while True:
        try:
            msg = es_queue.get(block=True, timeout=1)
            es_msg_handler(msg)
            es_queue.task_done()
            if es_quit_program:
                break
        except Queue.Empty:
            if es_quit_program:
                break


def send_message_to_es(msg):
    es_sock.sendall(msg)


def send_es_quit_message():
    # sends quit message to ES server
    msg = '#:00000:0:018:QUIT'
    es_sock.sendall(msg)


def es_initialize():
    global es_queue
    es_queue = Queue.Queue()
    global es_sock
    es_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    es_sock.connect(es_server_address)
    global es_msg_store
    es_msg_store = list()
    initialize_orders()
    global es_listener_thread
    es_listener_thread = threading.Thread(target=es_socket_listener)
    es_listener_thread.start()
    global es_processor_thread
    es_processor_thread = threading.Thread(target=es_queue_processor)
    es_processor_thread.start()


def close_es_socket():
    es_sock.close()
    es_listener_thread.join()
    es_processor_thread.join()


def es_submit_dialogue():
    message_to_submit = raw_input('message to submit: ')
    message_to_submit = add_length(message_to_submit)
    es_sock.sendall(message_to_submit)


def sell(cmd):
    try:
        """sell 100 XYZ 23.50 day ALGOPAIR"""
        """sell 100 XYZ 23.50 loo ALGOSYND"""
        """sell 100 XYZ moo ALGOGROUP"""
        """sell 100 XYZ vwap 23.5 stop ALGOSYND"""
        """sell 100 XYZ vwap 23.5 * 0.99 stop ALGOGROUP"""
        values = cmd.split(' ')
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
        es_sock.sendall(hydra_order_message)
        # print hydra_order_message
    except Exception as e:
        print e


def buy(command):
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

        es_sock.sendall(hydra_order_message)
        print hydra_order_message
    except Exception as e:
        print 'error encountered in buy function:\n{}'.format(e)


def closing_bracket_orders():
    acct = 'ALGOGROUP'
    dollars_per_trade = 20000
    build_quote_dictionary()
    offset_percentage = .015
    try:
        for key, l in quote_dictionary.iteritems():
            bid = l[0]
            ask = l[1]
            bid_offset = bid * offset_percentage
            ask_offset = ask * offset_percentage
            if .50 > bid_offset: bid_offset = .50
            if .50 > ask_offset: ask_offset = .50
            buy_level = round(bid - bid_offset,2)
            sell_level = round(ask + ask_offset,2)
            buy_shares = int(round(dollars_per_trade / buy_level,0))
            sell_shares = int(round(dollars_per_trade/sell_level,0)) * -1

            buy_order = generate_loc_limit_order(buy_shares,key,buy_level,acct)
            hydra_order_message = buy_order.craft_message()
            hydra_order_message = add_length(hydra_order_message)
            print hydra_order_message
            #es_sock.sendall(hydra_order_message)

            sell_order = generate_loc_limit_order(sell_shares,key,sell_level,acct)
            hydra_order_message = sell_order.craft_message()
            hydra_order_message = add_length(hydra_order_message)
            print hydra_order_message
            #es_sock.sendall(hydra_order_message)
            break
    except Exception as e:
        print e


def print_order_status():
    for key, value in orders_by_id.iteritems():
        print value.status


def cancel_all_orders():
    for key, value in orders_by_id.iteritems():
        if value.status == order_status_type.open or value.status == order_status_type.partial_open:
            cancel_msg = value.craft_cancel_message()
            cancel_msg = add_length(cancel_msg)
            print cancel_msg
            es_sock.sendall(cancel_msg)

