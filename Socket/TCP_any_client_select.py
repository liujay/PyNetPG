#! /usr/bin/env python
#
# A minimal TCP client program:
#       using select.select() to monitor both sock and sys.stdin,
#           where sock is a socket connected to remote host
#       input from sock are displayed on sys.stdout, and
#       input from sys.stdin are sent to remote host thru sock
#
#
# Modified from telnet.py in Python Examples
#
#       Jay S. Liu, Feb. 14, 2013
#       Version 0.2
#       Mar. 12, 2012, Version 0.1
#       jay.s.liu@gmail.com
#
#       HELP wanted:
#           select.select() does not work on sys.stdin for M$ systems
#           let me know if you have a clean solution for this.
#
#
#-------------------------------------------------------------
#
# Modified from telnet.py in Python Examples
#
#
# Usage: TCP_any_client_select host [port]
#
# The port may be a service name or a decimal port number;
# it defaults to 'echo'.
#

import socket
import select
import sys
from Client_connect import connectTCP

BUFSIZE = 1024

def any_client_select(host, port):
    try:
        sock = connectTCP(host, port)
    except socket.error, msg:
        sys.stderr.write('connect failed: ' + repr(msg) + '\n')
        sys.exit(1)
    input = [sock, sys.stdin]
    running = 1
    while (running):
        inputready, outputready, exceptready = select.select(input, [], [])
        for s in inputready:
            if s == sock:
                data = sock.recv(1024)
                if data:
                    sys.stdout.write(data)
                    sys.stdout.flush()
                else:
                    sys.stderr.write('(Closed by remote host)\n')
                    sock.close()
                    sys.exit(1)
            elif s == sys.stdin:
                # handle standard input
                data = sys.stdin.readline()
                if data:
                    sock.sendall(data)

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
            port = socket.getservbyname(service, 'tcp')
        except socket.error:
            sys.stderr.write(service + ': bad tcp service name\n')
            sys.exit(2)
    any_client_select(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e  
