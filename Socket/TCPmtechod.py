#
# TCP echo server in socket
#       Thread version for concurrent server
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 14, 2013
#   Version 0.2
#   May 24, 2011, Version 0.1
#
#
import socket
import sys
import threading

from Server_sock import passiveTCP

class echod_thread(threading.Thread):
    '''
        define server thread to serve each client
    '''
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.ssock = sock

    def run(self):
        while 1:
            data = self.ssock.recv(1024)
            if not data: break
            self.ssock.sendall(data)
        self.ssock.close()

def tcp_mtechod(host, port):
    msock = passiveTCP(host, port, 10)          # create and bind server socket
    while 1:
        ssock, ssock_address = msock.accept()   # new request
        print 'Connection from: ', ssock_address
        th = echod_thread(ssock)                 # create a thread
        th.start()                              #   to serve this client

def main():
    host = ''
    port = 7
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    tcp_mtechod(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e
