#
#   Create a TCP/UDP clinet socket, and connect it to (host, port)
#
#   This is a port of connectTCP()/connectUDP() from Comer and Stevens
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb 13, 2013
#
#
import socket

def connectTCP(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        return sock
    except:
        raise       # pass exception to caller; let it handle this


def connectUDP(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((host, port))
        return sock
    except:
        raise       # pass exception to caller; let it handle this

