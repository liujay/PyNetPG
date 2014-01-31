#! /usr/bin/env python
#
# A minimal TCP client program:
#       using (a) a child process to read data from stdin, send data to server
#             (b) a parent process to read data from server, write data to stdout
#
# Modified from telnet.py in Python Examples
#
#       Jay S. Liu, Feb. 14, 2013
#       jay.s.liu@gmail.com
#       version 0.2
#
#       Mar. 12, 2012:
#       version 0.1
#           replace posix module with os
#           HELP wanted:
#               there is no fork() in M$, so how to make this runs on M$???
#               let me know if you have a clean solution for this.
#
#
#-------------------------------------------------------------
#
# Usage: TCP_any_client host [port]
#
# The port may be a service name or a decimal port number;
# it defaults to 'echo'.
#

import sys
import socket
#import posix
import os

from Client_connect import connectTCP

BUFSIZE = 1024

def any_client(host, port):
    try:
        sock = connectTCP(host, port)
    except socket.error, msg:
        sys.stderr.write('connect failed: ' + repr(msg) + '\n')
        sys.exit(1)
    #
    pid = os.fork()             # replace posix with os
    #
    if pid == 0:
        # child -- read stdin, write socket
        while 1:
            line = sys.stdin.readline()
            sock.send(line)
    else:
        # parent -- read socket, write stdout
        iac = 0         # Interpret next char as command
        opt = ''        # Interpret next char as option
        while 1:
            data = sock.recv(BUFSIZE)
            if not data:
                # EOF; kill child and exit
                sys.stderr.write('(Closed by remote host)\n')
                os.kill(pid, 9)     # replace posix with os
                sys.exit(1)
            sys.stdout.write(data)
            sys.stdout.flush()


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
    any_client(host, port)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e         
