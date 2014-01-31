#
#   Create and bind a TCP/UDP server socket
#
#   This is a port of passiveTCP()/passiveUDP() from Comer and Stevens,
#       with some minor modifications on parameters
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb 13, 2013
#
#
import socket

def passiveTCP(host, service, qlen=5, portbase=0):
    '''
    create and bind a TCP server socket
        parametrs:
            host: network interface the service to be bound
            service: name (string) or port number (short) of service
            qlen: queue length
            portbase: a workaround for some privilege services, eg, echo,
                a portbase of 7000 will shift echo service to port 7007 (7000+7)
        (host, service) defines the server address
        each call reuses the specified port number
    '''
    serv_name = str(service)
    if '0' <= serv_name[:1] <= '9':         # port # in integer
        port = int(serv_name)
    else:                                   # resolve by service name
        try:
            port = socket.getservbyname(serv_name, 'tcp')
        except:                             # something wrong with port #
            sys.exit('Format error in port number!\n')
        port += portbase
    msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    msock.bind((host, port))
    msock.listen(qlen)
    return msock

def passiveUDP(host, service, qlen=0, portbase=0):
    '''
    create and bind a UDP server socket
        parametrs:
            host: network interface the service to be bound
            service: name (string) or port number (short) of service
            qlen: queue length
            portbase: a workaround for some privilege services, eg, echo,
                a portbase of 7000 will shift echo service to port 7007 (7000+7)
        (host, service) defines the server address
        each call reuses the specified port number
    '''
    serv_name = str(service)
    if '0' <= serv_name[:1] <= '9':        # port # in integer
        port = int(serv_name)
    else:                # resolve by service name
        try:
            port = socket.getservbyname(serv_name, 'udp')
        except:                # something wrong with port #
            sys.exit('Format error in port number!\n')
        port += portbase
    msock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    msock.bind((host, port))
    return msock

