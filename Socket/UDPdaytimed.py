#! /usr/bin/env python

#
# UDP daytime server
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 13, 2013
#   Version 0.2
#
#
import socket
import sys
import time

from Server_sock import passiveUDP

def udp_daytimed(host, port):
    sock = passiveUDP(host, port, 0)
    while 1:
        data, addr = sock.recvfrom(1024)
        print 'request from: ', addr
        data = time.ctime()
        sock.sendto(data, addr)

def main():
    host = ''
    port = 13
    if (len(sys.argv) > 1):
        port = sys.argv[1]
    udp_daytimed(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e

