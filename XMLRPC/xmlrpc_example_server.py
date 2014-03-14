"""
http://docs.python.org/library/simplexmlrpcserver.html

20.24.1.1. SimpleXMLRPCServer Example
Server code:

Modified by JSL
            jay.s.liu@gmail.com

        1. port number at users' choice: sys.argv[1]
        2. two methods in class MyFuncs: sub, mul
"""

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import sys

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
### JSL
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8000
### JSL --
server = SimpleXMLRPCServer(("localhost", port),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

# Register a function under a different name
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
#       and, 'sub' + 'mul'
class MyFuncs:
    def div(self, x, y):
        return x // y
    #
    # JSL
    #
    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y
    #
    # JSL ----

server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
