#! /usr/bin/env python
#
# A minimal UPD client program:
#	using (a) a child process to read data from stdin, send data to server
#             (b) a parent process to read data from server, write data to stdout
#
# Modified from telnet.py in Python Examples
#
#       Jay S. Liu, Feb. 13, 2013
#       Version 0.2
#       jay.s.liu@gmail.com
#
#       Mar. 12, 2012, Varsion 0.1
#           replace posix module with os
#           HELP wanted:
#               there is no fork() in M$, so how to make this runs on M$???
#               let me know if you have a clean solution for this.
#
#-------------------------------------------------------------
#
# Usage: UDP_any_client host [port]
#
# The port may be a service name or a decimal port number;
# it defaults to 'echo'.
#
# Terminate the client by pressing ctrl C
#


import sys
import socket
import os

from Client_connect import connectUDP

BUFSIZE = 1024

def udp_any_client(host, port):
    sock = connectUDP(host, port)
    pid = os.fork()
    #
    if pid == 0:
        # child -- read stdin, write socket
        while 1:
            line = sys.stdin.readline()
            #sock.sendto(line,(host,port))
            sock.sendall(line)              # use sendall() instead of sendto(), since
                                            # connected UPD socket is employed
    else:
        # parent -- read socket, write stdout
        while 1:
            data, addr = sock.recvfrom(BUFSIZE)
            if not data:
                # EOF; kill child and exit
                sys.stderr.write('(Closed by remote host)\n')
                os.kill(pid, 9)
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
            port = socket.getservbyname(service, 'udp')
        except socket.error:
            sys.stderr.write(service + ': bad udp service name\n')
            sys.exit(2)
    udp_any_client(host, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e        

