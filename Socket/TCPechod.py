#! /usr/bin/env python
#
# TCP echo server
#       this is an iterative server, which means that it serves one client
#           at a time
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 14, 2013
#   Version 0.2
#   May 23, 2011, Version 0.1
#
#
import socket
import sys
from Server_sock import passiveTCP

def tcp_echod(host, port):
    msock = passiveTCP(host, port, 10)
    while 1:
        ssock, ssock_address = msock.accept()
        print 'Connection from: ', ssock_address
        while 1:
            data = ssock.recv(1024)
            if not data: break
            ssock.sendall(data)
        ssock.close()

def main():
    host = ''
    port = 7
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    tcp_echod(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e
