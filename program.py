import socket
import threading
import Queue
import time
from order import *
from google_api import *
from excel_quotes import *
from quote import Quote

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
orders_by_id = 0
orders_by_parent = 0
quotes = 0


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
            if tokens[8] in orders_by_id:
                o = orders_by_id[tokens[8]]
                o.update_order(tokens)
            pass
        elif tokens[4] == 'F':
            # find order by parent id
            if tokens[6] in orders_by_parent:
                o = orders_by_parent[tokens[6]]
                o.order_id = tokens[9]
                orders_by_id[tokens[9]] = o
                o.update_order(tokens)
            pass


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

        orders_by_parent[o.parrent_id] = o

        hydra_order_message = o.craft_message()
        hydra_order_message = add_length(hydra_order_message)

        es_sock.sendall(hydra_order_message)
        print hydra_order_message
    except:
        print 'error encountered in buy function'


def submit():
    message_to_submit = raw_input('message to submit: ')
    message_to_submit = add_length(message_to_submit)
    es_sock.sendall(message_to_submit)


def process_row(row):
    print row
    return
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
            elif note.strip() == 'Enter (MOO)':
                prompt = 'How many shares of {0} do you have in {1}?'.format(
                    symbol, account
                )
                qty = raw_input(prompt)
                qty = int(qty)
                o = generate_opg_market_order(qty,symbol,account)
                prompt = 'Should I {0} {1} {2} moo (y/n)?'.format('buy', abs(qty), symbol)
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


def print_orders():
    print orders_by_id
    print orders_by_parent


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
                    submit()

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
    orders_by_id = dict()
    orders_by_parent = dict()
    quotes = dict()

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
