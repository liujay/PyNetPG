#
# TCP chargen client in socket
#
#   Jay S Liu
#   jay.s.liu@gmail.com
#   Feb 14, 2013
#   Version 0.2
#
#
import socket
import sys
from Client_connect import connectTCP

def tcp_chargen(host, port):
    try:
        sock = connectTCP(host, port)
    except:
        sys.exit('Error in connecting to the Server!')

    #
    # endless loop until we hit a ctrl C
    #
    while (True):
        data = sock.recv(1024)
        if data:
            sys.stdout.write(data)
            sys.stdout.flush()
        else:
            break
    sock.close()

def main():
    host = 'localhost'
    service = 'chargen'
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
    tcp_chargen(host, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e: 
        print e
