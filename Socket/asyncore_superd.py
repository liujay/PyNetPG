'''
The is an example of TCP multiservices server using asyncore module,
    modified from asyncore echo server in Python Doc
    17.6 asyncore

    Jay S. Liu
    jay.s.liu@gmail.com
    Apr. 7, 2012
'''
import asyncore
import socket
import sys
import time

class UDPServer(asyncore.dispatcher):

    def __init__(self, sv_addr, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind(sv_addr)
        self.sv_addr = sv_addr
        self.handler = handler
        self.handler(self)
        
class UDPEchoHandler(asyncore.dispatcher):        

    def handle_read(self):
        data, addr = self.recvfrom(2048)
        print 'Incoming connection from %s, asking for service on UDP port %s'\
              % (repr(addr), repr(self.sv_addr[1]))
        self.sendto(data,addr)

    # This is called all the time and causes errors if you leave it out.
    def handle_write(self):
        pass

class TCPServer(asyncore.dispatcher):

    def __init__(self, sv_addr, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(sv_addr)
        self.listen(5)
        self.sv_addr = sv_addr
        self.handler = handler

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s, asking for service on TCP port %s'\
              % (repr(addr), repr(self.sv_addr[1]))
            self.handler(sock)
            
class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.sendall(data)

class DaytimeHandler(asyncore.dispatcher_with_send):

    def writable(self):
        return True

    def handle_write(self):
        data = time.ctime()
        self.sendall(data)
        self.close()

class ChargenHandler(asyncore.dispatcher_with_send):

    def writable(self):
        return True

    def handle_write(self):
#
#   no infinite loop is allowed here,
#       since it eats up all resouce and all other sockets suffer starvation
#
        ch = 32
        from cStringIO import StringIO
        f_str = StringIO()
        for num in xrange(95):
            f_str.write(chr(ch))
            ch += 1
        data = f_str.getvalue()
        try:
            self.sendall(data)
        except:
            self.close()


def main():

    conf = [['echo','tcp', '', EchoHandler], \
      ['daytime','tcp', '', DaytimeHandler], \
      ['chargen','tcp', '', ChargenHandler], \
      ['echo', 'udp', '', UDPEchoHandler] ]
    
    if (len(sys.argv) >= 2):
        conf[0][0] = int(sys.argv[1])
    if (len(sys.argv) >= 3):
        conf[1][0] = int(sys.argv[2])
    if (len(sys.argv) >= 4):
        conf[2][0] = int(sys.argv[3])
    if (len(sys.argv) >= 5):
        conf[3][0] = int(sys.argv[4])
    for serv in conf:
        service = serv[3]
        try:      # resolve by service name first
            port = socket.getservbyname(serv[0])
        except:   # if not resolvable by name then assume that it is a port number
            port = int(serv[0])
        if serv[1] == 'tcp':
            TCPServer(('localhost',port),service)
        else:
            UDPServer(('localhost',port),service)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()