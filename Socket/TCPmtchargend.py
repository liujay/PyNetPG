#
# TCP chargen server in socket
#       Thread version for concurrent server
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 14, 2013
#   Version 0.2
#   Jan. 5, 2012, Version 0.1
#
#
import socket
import sys
import threading

from Server_sock import passiveTCP

class chargend_thread(threading.Thread):
    '''
        define server thread to serve each client
    '''
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.ssock = sock
        self.ch = 32

    def run(self):
        while (True):
            from cStringIO import StringIO
            f_str = StringIO()
            for num in xrange(80):
                f_str.write(chr(self.ch))
                if self.ch >= 126:
                    self.ch = 32
                else:
                    self.ch += 1
            data = f_str.getvalue()
            try:
                self.ssock.sendall(data)
            except:
                break
        self.ssock.close()

def tcp_mtchargend(host, port):
    msock = passiveTCP(host, port, 10)          # create and bind server socket
    while 1:
        try:
            ssock, ssock_address = msock.accept()   # new request
            print 'Connection from: ', ssock_address
            th = chargend_thread(ssock)             # create a thread
            th.start()                          #   to serve this client
        except:
            break

def main():
    host = ''
    port = 19
    if (len(sys.argv) == 2):
        port = int(sys.argv[1])
    tcp_mtchargend(host, port)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e
