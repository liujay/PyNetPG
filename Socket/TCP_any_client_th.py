#! /usr/bin/env python
#
# TCP any client in socket
#       thread is used for reading/writing to/from socket
#
#       Usage: python TCP_any_client_th.py host port
#
#           use Ctrl-c (or, some secret code)to terminate the program
#           unresolved issue: select.select() was used to mimic non-blocking keyboard input,
#                       which was not supported in M$ systems,
#                       therefore, this program does not work under M$ systems.
#
#                       however, you may comment out two line:
#                           select.select() and if inputready in the to_sevr_thread
#                       to get this program runs on M$;
#                       it runs smoothly on M$, except that Ctrl-c won't be delivered
#                       until you hit the RETRUN (readln() was used).
#                       btw, Ctrl-c is not the only way to terminate program,
#                       seek thou should find a secret code to terminate threads.
#
#                       let me know if you have a better solution for M$.
#
#                       THIS IS A CRAZY SOLUTION!
#                       BOTH ANY_CLIENT AND ANY_CLIENT_SELECT WORKS FINE, BUT NEITHER ON M$
#                       EITHER ONE WILL BE A NEAT SOLUTION COMPARED TO THIS, FOR FUN!?
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 14, 2013
#   Version 0.2
#
#   Mar. 17, 2012, Version 0.1
#
#
import socket
import sys
import threading
import select

from Client_connect import connectTCP

class from_sevr_thread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.timeout = 0.05
        self.sock.settimeout(self.timeout)      # timeout used for socket input from server

    def run(self):
        global running
        while running:
            try:
                data = self.sock.recv(1024)     # socket input with timeout
            except socket.timeout:
                continue                        # try to read in next round
            except:
                running = False
                break
            if not data:
                sys.stderr.write('\nSocket closed by remote!\n')
                running = False
                break
            sys.stdout.write(data)              # copy socket input to stdout
            sys.stdout.flush()

class to_sevr_thread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.timeout = 0.05

    def run(self):
        global running
        input = [sys.stdin]
        while running:
            #
            #   CRAZY SOLUTION
            #
            #   select.select with timeout was used to mimic non-blocking,
            #       which enables the while loop to get a refresh on running or not
            #
            #   remove the following two lines if you want to run this program on M$
            #       however, there is one minor side effect as stated before
            #
            inputready, outputready, exceptready = select.select(input, [], [],self.timeout)
            if inputready:
                try:
                    data = sys.stdin.readline()
                except:
                    running = False
                    break
                if data[:9] == '!!!END!!!':     # secret code to end both threads
                    print '\nBingo ---- terminating both threads...\n'
                    running = False
                    break
                self.sock.sendall(data)     # send keyboard input to server in one shot
#        print '--- to server thread ends ---\n'


def any_client_th(host, port):
    try:
        sock = connectTCP(host, port)
    except:
        sys.exit('Error in connecting to the server!\n')
    #
    #
    #
    global running
    running = True
    from_th = from_sevr_thread(sock)
    from_th.start()
    to_th = to_sevr_thread(sock)
    to_th.start()

    try:
        while running: pass     # wait for any sign of stop,
                                 # cannot use join() for wait,
                                 # if wait on join(), we won't be able to catch Ctrl-c
                                 # Ctrl-c is delivered to the main thread only, not to other thread
    except KeyboardInterrupt:
        print "\nCtrl-c received! Sending kill to threads...\n"
        running = False
    from_th.join()
    to_th.join()
    sys.exit(1)

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
    any_client_th(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e

