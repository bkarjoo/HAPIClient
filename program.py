import socket
import threading
import Queue
import time

quit_program = False
es_sock = 0
is_sock = 0
es_server_address = ('localhost', 10000)
is_server_address = ('localhost', 10001)
es_queue = 0
is_queue = 0


def es_msg_handler(msg):
    print 'es: ', msg


def is_msg_handler(msg):
    print 'is: ', msg


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


def interactive():
    while True:
        command = raw_input('')

        if command == 'q':
            quit()
            return






if __name__ == "__main__":
    es_queue = Queue.Queue()
    is_queue = Queue.Queue()
    es_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    es_sock.connect(es_server_address)
    is_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_sock.connect(is_server_address)

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
