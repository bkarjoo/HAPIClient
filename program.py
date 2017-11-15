import socket
import threading
import Queue
import time
from order import *
from google_api import *

quit_program = False
es_sock = 0
is_sock = 0
es_server_address = ('localhost', 10000)
is_server_address = ('localhost', 10001)
es_queue = 0
is_queue = 0
es_msg_store = 0
is_msg_store = 0
es_msg_count = 0
is_msg_count = 0


def es_msg_handler(msg):
    global es_msg_count
    es_msg_count += 1
    es_msg_store.append(msg)


def is_msg_handler(msg):
    global is_msg_count
    is_msg_count += 1
    is_msg_store.append(msg)


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
            if quit_program:
                es_sock.close()
                break
        except:
            if quit_program:
                es_sock.close()
                break
        finally:
            if quit_program:
                es_sock.close()
                break


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
            if quit_program:
                is_sock.close()
                break
        except:
            if quit_program:
                is_sock.close()
                break
        finally:
            if quit_program:
                is_sock.close()
                break


def es_queue_processor():
    while True:
        try:
            msg = es_queue.get(block=True, timeout=1)
            es_msg_handler(msg)
            es_queue.task_done()
            if quit_program:
                break
        except Queue.Empty:
            if quit_program:
                break


def is_queue_processor():
    while True:
        try:
            msg = is_queue.get(block=True, timeout=1)
            is_msg_handler(msg)
            is_queue.task_done()
            if quit_program:
                break
        except Queue.Empty:
            if quit_program:
                break


def get_len_str(msg):
    l = len(msg)
    if l < 10:
        return '00' + str(l)
    elif l < 100:
        return '0' + str(l)
    else:
        return str(l)


def add_length(msg):
    return msg[:10] + get_len_str(msg) + msg[13:]


def send_es_quit_message():
    # sends quit message to ES server
    msg = '#:00000:0:018:QUIT'
    es_sock.sendall(msg)


def send_is_quit_message():
    # sends quit message to IS server
    msg = '#:00000:0:018:QUIT'
    is_sock.sendall(msg)


def quit():
    send_es_quit_message()
    send_is_quit_message()
    global quit_program
    quit_program = True
    time.sleep(1)


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
        o = order()
        acct = 'ALGOGROUP'
        if values[3].upper() == 'MOO':
            if len(values) == 5:
                acct = values[4]
            o = generate_opg_market_order(qty, value[2], acct)
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
                o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', price, acct)
            else:
                if len(values) == 7:
                    acct = values[6]
                o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', values[4], acct)
        elif values[4].upper() == 'LOO':
            if len(values) == 6:
                acct = values[5]
            o = generate_opg_limit_order(qty, value[2], value[3], acct)
        elif values[4].upper() == 'LOC':
            if len(values) == 6:
                acct = values[5]
            o = generate_loc_limit_order(values[1], values[2], values[3], acct)
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
    except:
        print 'error encountered in sell function'


def buy(command):
    try:
        """buy 100 XYZ 23.50 day (ALGOPAI)"""
        """buy 100 XYZ 23.50 loo (ALGOSYND)"""
        """buy 100 XYZ moo (ALGOGROUP)"""
        """buy 100 XYZ 23.5 stop 23.75 limit (ALGOGROUP)"""
        """buy 100 XYZ VWAP 23.5 stop (ALGOGROUP)"""
        """buy 100 XYZ VWAP 23.5 * 1.01 stop (ALGOGROUP)"""
        values = command.split(' ')

        o = order()
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

        hydra_order_message = o.craft_message()
        hydra_order_message = add_length(hydra_order_message)
        es_sock.sendall(hydra_order_message)
        # print hydra_order_message
    except:
        print 'error encountered in buy function'


def submit():
    message_to_submit = raw_input('message to submit: ')
    message_to_submit = add_length(message_to_submit)
    es_sock.sendall(message_to_submit)


def process_row(row):
    if (len(row) > 0):
        strategy = str(row[0])
        symbol = ''
        if (len(row)) > 1:
            symbol = str(row[1]).split(' ')[0]
        side = ''
        if (len(row)) > 2:
            side = str(row[2])
        bp_share = ''
        if (len(row)) > 3:
            bp_share = str(row[3])
        note = ''
        if (len(row)) > 4:
            note = str(row[4])
        account = ''
        if (len(row)) > 5:
            account = str(row[5]).upper()

        if strategy == 'Sentiment':
            qty = int(bp_share)
            action = 'buy'
            if side == 'Short':
                qty *= -1
                action = 'short'
            price = note[1:]
            price = float(price)
            o = generate_opg_limit_order(qty,symbol,price,'ALGOGROUP')
            prompt = 'Should I {0} {1} {2} {3} LOO (y/n)?'.format(action,abs(qty),symbol, price)
            user_input = raw_input(prompt)
            if user_input == 'y':
                hydra_order_message = o.craft_message()
                hydra_order_message = add_length(hydra_order_message)
                es_sock.sendall(hydra_order_message)
                # print hydra_order_message
            else:
                pass
        elif strategy == 'Secondary':
            if note.strip() == 'Exit (MOC)':
                prompt = 'How many shares of {0} do you have in {1}?'.format(
                    symbol, account
                )
                qty = raw_input(prompt)
                qty = int(qty)*-1
                o = generate_moc_market_order(qty,symbol,account)
                prompt = 'Should I {0} {1} {2} moc (y/n)?'.format('sell', abs(qty), symbol)
                user_input = raw_input(prompt)
                if user_input == 'y':
                    hydra_order_message = o.craft_message()
                    hydra_order_message = add_length(hydra_order_message)
                    es_sock.sendall(hydra_order_message)
                    # print hydra_order_message
                else:
                    pass
        else:
            print('strategy: {0}, {1}, {2}, {3}, {4}, {5}'.format(strategy, symbol, side, bp_share, note, account))


def process_sheet():
    sheet = get_sheet()
    for row in sheet:
        process_row(row)


def interactive():
        while True:
            try:
                command = raw_input('')

                if command == 'q':
                    quit()
                    return

                if command[:4] == 'sell':
                    sell(command)

                if command[:3] == 'buy':
                    buy(command)

                if command == 'submit':
                    submit()

                if command == 'sheet':
                    process_sheet()

                if command == 'pem':
                    for m in es_msg_store:
                        print m

                if command == 'pim':
                    for m in is_msg_store:
                        print m

                if command == 'pemc':
                    print es_msg_count

                if command == 'pimc':
                    print is_msg_count

            except:
                print 'error in interactive'





if __name__ == "__main__":
    es_queue = Queue.Queue()
    is_queue = Queue.Queue()
    es_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    es_sock.connect(es_server_address)
    is_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_sock.connect(is_server_address)
    is_msg_store = list()
    es_msg_store = list()

    t1 = threading.Thread(target=es_socket_listener)
    t1.start()
    t2 = threading.Thread(target=es_queue_processor)
    t2.start()
    t3 = threading.Thread(target=is_socket_listener)
    t3.start()
    t4 = threading.Thread(target=is_queue_processor)
    t4.start()

    interactive()

    time.sleep(1)
    es_sock.close()
    is_sock.close()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
