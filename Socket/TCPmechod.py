#
# TCP echo server in socket
#       Concurrent echo server through select
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb. 19, 2013
#   Version 0.2
#   May 24, 2011, Version 0.1
#
#
import socket
import sys
import select

from Server_sock import passiveTCP

def tcp_mechod(host, port):
    msock = passiveTCP(host, port, 10)          # create and bind server socket
    in_source = [msock, sys.stdin]
    while 1:
        in_ready, out_ready, exp_ready = select.select(in_source, [], [])
        for sock in in_ready:
            if sock == msock:
            #
            #   handle the server socket (msock)
            #
                ssock, ssock_address = msock.accept()
                print 'Connection from: ', ssock_address
                in_source.append(ssock)
            elif sock == sys.stdin:
            #
            #   handle the stdin
            #       we don't actually need this, just for demonstration
            #
                junk = sys.stdin.readln()
            else:
            #
            #   handle all other clients
            #
                data = sock.recv(1024)
                if data:
                    sock.sendall(data)
                else:
                    sock.close()
                    in_source.remove(sock)
    msock.close()

def main():
    host = ''
    port = 7
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    tcp_mechod(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print e
