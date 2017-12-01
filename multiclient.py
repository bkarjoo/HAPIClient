# Python TCP Client A
import socket
import threading

exit = False
host = socket.gethostname()
port = 52000
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

def send_thread():
    while 1:
        message = raw_input('')
        if message == 'exit':
            exit = True
            break

        tcpClientA.send(message)

t = threading.Thread(target=send_thread)
t.start()


while 1:
    #tcpClientA.send(MESSAGE)
    data = tcpClientA.recv(BUFFER_SIZE)
    print " Client2 received data:", data
    #MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")
    if exit:
        break


t.join()
tcpClientA.close()