#
# TCP super server in socket
#       A python version of superd.c as in Comer & Stevens' text book.
#
#       Thread version for concurrent server
#       There is one master process (defined in main loop) reponsible for
#           processing each request from msocks or stdin:
#           each (defined) TCP request is handled by creating a thread,
#           each UDP request is handled by the master process by calling a function, and
#           terminate on secret code entered from stdin
#
#       The name select is used because the master process depends on the
#           system call "select" to multiplexing different requests.
#
#       Few services are supported:
#           echo        17,     TCP/UDP
#           daytime     13,     TCP/UDP
#           chargen     19,     TCP
#           time        37,     TCP/UDP
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Jan. 31, 2014
#   Version 0.2.1
#
#
import sys
import socket
import select
import threading
import time

from Server_sock import *

class chargend_thread(threading.Thread):
    def __init__(self, msock, response):
        threading.Thread.__init__(self)
        self.msock = msock
        self.ssock = response[0]
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

class echod_thread(threading.Thread):
    def __init__(self, msock, response):
        threading.Thread.__init__(self)
        self.msock = msock
        self.ssock = response[0]

    def run(self):
        while (True):
            data = self.ssock.recv(1024)
            if not data: break
            self.ssock.sendall(data)
        self.ssock.close()

class timed_thread(threading.Thread):
    def __init__(self, msock, response):
        threading.Thread.__init__(self)
        self.msock = msock
        self.ssock = response[0]

    def run(self):
        data = time.strftime('%10s')
        self.ssock.sendall(data)
        self.ssock.close()

class daytimed_thread(threading.Thread):
    def __init__(self, msock, response):
        threading.Thread.__init__(self)
        self.msock = msock
        self.ssock = response[0]

    def run(self):
        data = time.ctime()
        self.ssock.sendall(data)
        self.ssock.close()

def echod_udp(sock, response):
    data, addr = response
    sock.sendto(data, addr)

def timed_udp(sock, response,):
    dontcare, addr = response
    data = time.strftime('%10s')
    sock.sendto(data, addr)

def daytimed_udp(sock, response):
    dontcare, addr = response
    data = time.ctime()
    sock.sendto(data, addr)

#
# main
#
def main():
    host = ''
    portbase = 0

    if (len(sys.argv) > 1):
        portbase = int(sys.argv[1])

    conf = [['echo','tcp', '',echod_thread], \
      ['daytime','tcp', '',daytimed_thread], \
      ['chargen','tcp', '',chargend_thread], \
      ['time','tcp', '',timed_thread], \
      ['echo','udp', '', echod_udp], \
      ['daytime','udp', '', daytimed_udp], \
      ['time','udp', '', timed_udp] ]
    sock_2_serv_TCP = dict()
    sock_2_serv_UDP = dict()
    input = [sys.stdin]

    #
    # create and bind one msock for each service
    #     we need a dictionary to store msock for service mapping
    #
    for service in conf:
        if service[1] == 'tcp':
            tsock = passiveTCP(host, service[0], 5, portbase)
            sock_2_serv_TCP[tsock] = service[3]
            service[2] = tsock
            input.append(tsock)
        elif service[1] == 'udp':       # we have not consider UPD at this time
            usock = passiveUDP(host, service[0], 0, portbase)
            sock_2_serv_UDP[usock] = service[3]
            service[2] = usock
            input.append(usock)

    #
    # main loop: wait input and process each request from msocks or stdin
    #
    running = 1
    while (running):
        try:
            inputready, outputready, exceptready = select.select(input, [], [])
            for sock in inputready:
                if sock_2_serv_TCP.has_key(sock):           # TCP only
                    serv = sock_2_serv_TCP[sock]
                    response = sock.accept()                # mimic ServerSocket
                    print 'Incoming TCP connection from %s, for service on port %s'\
                        % (repr(response[1]), sock.getsockname()[1])
                    th = serv(sock, response)               # one thread for each client request
                    th.start()                              #   pass response to thread
                elif sock_2_serv_UDP.has_key(sock):         # UDP only
                    serv = sock_2_serv_UDP[sock]
                    response = sock.recvfrom(1024)          # mimic ServerSocket
                    print 'Incoming UDP request from %s, for service on port %s'\
                        % (repr(response[1]), sock.getsockname()[1])
                    serv(sock, response)
                elif sock == sys.stdin:
                    data = sys.stdin.readline()
                    if data[:9] == '!!!END!!!': running = 0
                    else: sys.stderr.write(
                    "Server running --- enter secret code or ... to stop\n")
        except:
            running = 0

    #
    # close all msocks
    #
    for service in conf:
        service[2].close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e

