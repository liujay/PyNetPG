#! /usr/bin/env python
#
# UDP echo client
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   May 3, 2013
#   Version 0.2.1
#
#
import socket
import sys

from Client_connect import connectUDP

def udp_echo(host, port):
    sock = connectUDP(host, port)
    #
    # loop ends with a blank input line, or ...
    #
    data = raw_input('------> ')
    while (data):
        sock.send(data)
        data, addr = sock.recvfrom(1024)
        print 'Echoed: %s' % data
        data = raw_input('------> ')

def main():
    host = 'localhost'
    service = 'echo'
    if (len(sys.argv) > 1):
        try:
            host = socket.gethostbyname(sys.argv[1])
        except socket.error:
            sys.stderr.write(sys.argv[1] + ': bad host name\n')
            sys.exit(2)
    if len(sys.argv) > 2:
        service = sys.argv[2]
    if '0' <= service[:1] <= '9':      # port in number form
        port = int(service)
    else:                               # port in service name form
        try:
            port = socket.getservbyname(service, 'udp')
        except socket.error:
            sys.stderr.write(service + ': bad udp service name\n')
            sys.exit(2)
    udp_echo(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e
