'''
The is an example of UDP echo server using asyncore module,
    modified from asyncore echo server in Python Doc
    17.6 asyncore

    Jay S. Liu
    jay.s.liu@gmail.com
    Feb. 16, 2013
    Version 0.1.2
    Apr. 7, 2012, Version 0.1
'''
import asyncore, socket, sys

class AsyncoreServerUDP(asyncore.dispatcher):
   def __init__(self, host, port):
      asyncore.dispatcher.__init__(self)
      self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.bind((host, port))

   # Even though UDP is connectionless this is called when it binds to a port
   def handle_connect(self):
      print "Server Started..."

   # This is called everytime there is something to read
   def handle_read(self):
      data, addr = self.recvfrom(2048)
      print str(addr)+" >> "+data
      self.sendto(data,addr)

   # This is called all the time and causes errors if you leave it out.
   def handle_write(self):
      pass

def main():
    host = 'localhost'
    port = 8080
    if (len(sys.argv) >= 2): port = int(sys.argv[1])
    AsyncoreServerUDP(host, port)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        sys.exit(2)

if __name__ == "__main__":
    main()        
