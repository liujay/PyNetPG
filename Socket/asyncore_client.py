'''
This is an example from Python Doc:
    17.6 asyncore

    minor modification by
    JSL
    jay.s.liu@fcu.edu.tw
    Mar. 7, 2012
'''
import asyncore, socket

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, path, id):         # JSL add id
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 80) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path
        self.id = id                            # JSL a

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print 'Result from Client %s: ' % self.id       # JSL a
        print self.recv(8192)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        print 'Client %s sent %d bytes' % (self.id, sent)   # JSL a
        self.buffer = self.buffer[sent:]


client1 = HTTPClient('www.google.com', '/', 'c1')           # JSL m
client2 = HTTPClient('www.python.org', '/', 'c2')           # JSL m
asyncore.loop()