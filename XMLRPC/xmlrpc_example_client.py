"""
http://docs.python.org/library/simplexmlrpcserver.html

20.24.1.1. SimpleXMLRPCServer Example
Client code:

Modified by JSL
            jay.s.liu@gmail.com

        1. port number at users' choice: sys.argv[1]
        2. two methods in class MyFuncs: sub, mul
"""

import xmlrpclib
import sys
### JSL
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = '8000'
uri = 'http://127.0.0.1:' + port
s = xmlrpclib.ServerProxy(uri)
### JSL --
print s.pow(2,3)  # Returns 2**3 = 8
print s.add(2,3)  # Returns 5
print s.div(5,2)  # Returns 5//2 = 2
# JSL
print s.sub(2,3)  # Returns 2-3 = -1
print s.mul(2,3)  # Returns 2*3 = 6
# JSL ----
# Print list of available methods
print s.system.listMethods()