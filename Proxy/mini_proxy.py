#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Miniproxy
This code is based on microproxy, and munchy.

Only HTTP with methonds GET, HEAD, and POST are supported.

This program comes with ABSOLUTELY NO WARRANTY.

This program is for educational purpose only, use it at your own risk.

    Jay S. Liu
    jay.s.liu@gmail.com
    May. 16, 2012

#####################################################################
Microproxy
This code is based on code based on microproxy.py written by ubershmekel in 2006.

Microproxy is the simplest possible http proxy. It simply relays all bytes from the client to the server at a socket send and recv level. The way it recognises the remote server to connect to is by a simple regex, which extracts the URL of the origin server from the byte stream. (This probably doesn't work in all cases).


#####################################################################
# $ProjectHeader: munchy 0.7.1 Tue, 25 Apr 2000 21:15:56 -0600 nas $
# Neil's Ad Munching HTTP Proxy Server
#
# Usage: proxy.py [port]
#
# This code has been placed in the public domain.
# Neil Schemenauer <nascheme@enme.ucalgary.ca>
#####################################################################

"""

import sys
import socket
import threading
import urlparse
import time

PORT = 8080

class ServiceThread(threading.Thread):
    def __init__(self, (sock,addr)):
        threading.Thread.__init__(self)
        self.clnt_sock = sock
        self.clnt_addr = addr
        self.clnt_rfile = self.clnt_sock.makefile('rb')
        self.clnt_wfile = self.clnt_sock.makefile('wb')
        self.serv_rfile = None
        self.serv_wfile = None

    def run(self):
        """main service thread
            1. precossing request message
            2. processing response message
        """
        self.handle_request()
        self.handle_response()

    def handle_request(self):
        """handle request
            1. process request line
            2. read and forward headers
            3. [read and forward message body]
        """
        #
        # read, process and forward request
        server, port, method, request = self.read_request()
        self.connect(server,port)
        self.send_request(request)
        #
        # read and forward headers
        contentLength = 0
        while 1:
            line = self.clnt_rfile.readline()
            if not line:
                break                                   # something wrong
            if line.lower().startswith('proxy-connection:'):
                continue
            if line.lower().startswith('content-length:'):  # message with content-length
                _, length = line.split(':')
                contentLength = int(length)             # content-length
            self.serv_wfile.write(line)                 # forward to server
            self.serv_wfile.flush()
            if line == '\r\n' or line == '\n':          # end of message header
                break
        #
        # read and forward message body, if any
        #   only method supported is POST
        if method == "POST":
            if contentLength != 0:
                data = self.clnt_rfile.read(contentLength)
            else:
                data = self.clnt_rfile.readline()

            self.serv_wfile.write(data)
            self.serv_wfile.flush()
        sys.stdout.write(" --- Done sending. Response: \n")



    def read_request(self):
        """read request to find out host and port, where
        request is the first line in the request message
        """
        request = self.clnt_rfile.readline()
        sys.stdout.write('%s - %s - %s' % (
                                self.clnt_addr,
                                time.ctime(time.time()),
                                request))
        try:
            method, url, protocol = request.split()
        except:
            self.error(400, "Can't parse request")
        if not url:
            self.error(400, "Empty URL")
        if method not in ['GET', 'HEAD', 'POST']:
            self.error(501, "Unknown request method (%s)" % method)
        #
        # split url into site and path
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
        if scheme.lower() != 'http':
            self.error(501, "Unknown request scheme (%s)" % scheme)
        # find port number
        if ':' in netloc:
            host, port = netloc.split(':')
            port = int(port)
        else:
            host = netloc
            port = 80
        print '---- request for %s %s ----' % (host, port)
        return host, port, method, request

    def connect(self, host, port):
        """connect to the server with end-point address: (host, port)
        connected socket is makefiled and recorded in
        self.serv_rfile and self.serv_wfile
        """
        try:
            addr = socket.gethostbyname(host)
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((addr, port))
        except socket.error, err:
            self.error(200, 'Error connecting to "%s" (%s)' % (host, err))
        print '---- connect to server ok ----'
        self.serv_rfile = server.makefile('rb')
        self.serv_wfile = server.makefile('wb')

    def send_request(self, request):
        """sending the request line
        to the server
        """
        try:
            self.serv_wfile.write(request)
            self.serv_wfile.flush()
            print '---- send request ok ----'
        except socket.error, err:
            self.error(500, 'Error sending data to "%s" (%s)' % (host, err))

    def handle_response(self):
        """handle reponse
            1. process status line
            2. process message headers,
            3. process message body
        """
        #
        # read and forward status line
        sys.stdout.write('reading server response\n')
        response = self.serv_rfile.readline()
        sys.stdout.write('response = %s\n' % response)
        fields = response.split()
        version = fields[0]
        status = fields[1]
        comment = ' '.join(fields[2:])
        self.clnt_wfile.write('HTTP/1.0 %s %s\r\n' % (status, comment))
        #
        # read and forward headers ---- work needs to be done
        sys.stdout.write('reading response headers\n')
        contentLength = -1
        while 1:
            line = self.serv_rfile.readline()
            self.clnt_wfile.write(line)
            line = line.strip()
            print line
            if line.lower().startswith('content-length:'):
                _, length = line.split(':')
                contentLength = int(length)
            if not line:                        # end of headers: \r\n
                break
        self.clnt_wfile.flush()
        print '---- End of reponse Headers ----'
        #
        # read and forward body
        sys.stdout.write('transfering raw data\n')
        print '---- Content-Length: ',  contentLength

        if contentLength >= 0:              # loop based on content-length
            data = ''
            while (len(data)<contentLength):
                print '---- Raw data length: ', len(data), ' ----'
                data += self.serv_rfile.read(contentLength)
            if len(data):
                self.clnt_wfile.write(data)
                self.clnt_wfile.flush()
        else:                               # no info on content-length, loop until null
            while 1:
                data = self.serv_rfile.read(1024)
                if not data:
                    break
                self.clnt_wfile.write(data)
                self.clnt_wfile.flush()
        print '---- End of Raw Data ---'
        """
        self.clnt_rfile.close()
        self.clnt_wfile.close()
        self.serv_rfile.close()
        self.serv_wfile.close()
        """

    def error(self, code, body):
#        import BaseHTTPServer
#        response = BaseHTTPServer.BaseHTTPRequestHandler.responses[code][0]
#
#       We don't want to import BaseHTTPServer in order to make miniproxy lighter.
#       you may hand-coded response message here to make error much more readable
#
        self.clnt_wfile.write("HTTP/1.0 %s \r\n" % code)
        self.clnt_wfile.write("Server: Mini Proxy\r\n")
        self.clnt_wfile.write("Content-type: text/html\r\n")
        self.clnt_wfile.write("\r\n")
        self.clnt_wfile.write('<html><head>\n<title>%d </title>\n</head>\n'
                '<body>\n%s\n</body>\n</html>' % (code, body))
        self.clnt_wfile.flush()
        self.clnt_wfile.close()
        self.clnt_rfile.close()
        raise SystemExit

class ProxyThread(threading.Thread):
    """Main proxy threading
        1. prepare proxy server socket
        2. loop forever
                serve each cleint request
    """
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))


    def run(self):
        self.sock.listen(10)
        while 1:
            sv = ServiceThread(self.sock.accept())    # one service thread on each connection
            sv.daemon = True
            sv.start()

def main():
    if len(sys.argv) >= 2:
        PORT = int(sys.argv[1])
    try:
        proxy = ProxyThread(PORT)
    except:
        print "Fail to start proxy server!"
        sys.exit(1)
    proxy.daemon = True
    proxy.start()
    print "Started a proxy on port", PORT
    try:
        while True: pass
    except KeyboardInterrupt:
        print "\nCtrl-c received! Exiting now...\n"
    sys.exit(2)

if __name__ == "__main__":
    main()
