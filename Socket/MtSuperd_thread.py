#
# TCP super server in socket
#       A variation of superd.c as in Comer & Stevens' text book.
#
#       ALL thread version for concurrent super server
#       A main thread is created for each service, which serves
#           incoming requests accordingly.
#       There are 4(TCP ) + 3(UDP) main threads in this example,
#           compared to 1 main process in MtSuperd_select.py
#           because no "select" is needed here
#
#       Few services are supported:
#           echo        17,     TCP/UDP
#           daytime     13,     TCP/UDP
#           chargen     19,     TCP
#           time        37,     TCP/UDP
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Apr. 19, 2013
#   Version 0.1
#
#
import sys
import socket
import select
import threading
import time

from Server_sock import *

class tcp_d(threading.Thread):
    def __init__(self, host, port, portbase, service_thread):
        threading.Thread.__init__(self)
        self.msock = passiveTCP(host, port, 10, portbase)
        self.service_thread = service_thread

    def run(self):
        global running
        #
        # ^c is not able to kill this thread instantly, because
        #       accept() is a blocking call
        while running:
            response = self.msock.accept()   # new request
            print 'Connection from: ', response[1]
            th = self.service_thread(self.msock, response)      # create a thread
            th.start()  
        self.msock.close()

class udp_d(threading.Thread):
    def __init__(self, host, port, portbase, service_func):
        threading.Thread.__init__(self)
        self.msock = passiveUDP(host, port, 10, portbase)
        self.service_func = service_func

    def run(self):
        global running
        #
        # ^c is not able to kill this thread instantly, because
        #       recvfrom() is a blocking call
        while running:
            response = self.msock.recvfrom(1024)
            self.service_func(self.msock, response)
        self.msock.close()

class chargend_thread(threading.Thread):
    def __init__(self, msock, response):
        threading.Thread.__init__(self)
        self.msock = msock
        self.ssock = response[0]
        self.ch = 32

    def run(self):
        global running
        while (running):
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
        global running
        while (running):
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
    global running
    running = True

    if (len(sys.argv) > 1):
        portbase = int(sys.argv[1])

    conf = [['echo', 'tcp', '', echod_thread], \
      ['daytime', 'tcp', '', daytimed_thread], \
      ['chargen', 'tcp', '', chargend_thread], \
      ['time', 'tcp', '', timed_thread], \
      ['echo', 'udp', '', echod_udp], \
      ['daytime', 'udp', '', daytimed_udp], \
      ['time', 'udp', '', timed_udp] ]
    #
    # create and start each service in a seperate main thread
    for service in conf:
        if service[1] == 'tcp':
            service[2] = tcp_d(host, service[0], portbase, service[3])
            service[2].start()
        elif service[1] == 'udp':
            service[2] = udp_d(host, service[0], portbase, service[3])
            service[2].start()
        else:
            sys.stderr.write("Something wrong in conf. file!\n")
            sys.exit()
    #
    # main loop: wait input
    try:
        while running: pass     # wait for any sign of stop,
                                 # cannot use join() for wait,
                                 # if wait on join(), we won't be able to catch Ctrl-c
                                 # Ctrl-c is delivered to the main thread only, not to other thread
    except KeyboardInterrupt:
        print "\nCtrl-c received! Sending kill to threads...\n"
        running = False

    #
    # close all main threads
    for service in conf:
        service[2].join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e

