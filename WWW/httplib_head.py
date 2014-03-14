"""
    Here is an example session that uses the HEAD method:
        python DOC
        section 20.7.3.

    Minor modification by:
    Jay S. Liu
    jay.s.liu@gmail.com
    May 9, 2012

"""

import httplib

conn = httplib.HTTPConnection("www.python.org")
conn.request("HEAD", "/index.html")
r1 = conn.getresponse()
print "Response for: http://www.python.org/index.html"
#
#   print status line
#
print r1.status, r1.reason
#
#   print message body
#
data = r1.read()
print "The length of data is %s." % len(data)
conn.close()
