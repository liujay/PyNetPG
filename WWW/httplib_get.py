"""
    Here is an example session that uses the GET method:
        python DOC
        section 20.7.3.

    Minor modification by:
    Jay S. Liu
    jay.s.liu@gmail.com
    May 9, 2012

"""

import httplib
import sys

conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print "Response for: http://www.python.org/index.html"
#
#   print status line
#
print r1.status, r1.reason
print
#
#   print message body
#       only the first 5 and the last 10 lines are shown
#
data = r1.read()                        # read reponse
datalines = data.splitlines(True)       # split into lines (keep line breaks)
sys.stdout.writelines(datalines[:5])    # print the first 5 lines
print "......"
sys.stdout.writelines(datalines[-10:])  # print the last 10 lines
print

#
#   2nd request
#
conn.request("GET", "/parrot.spam")
r2 = conn.getresponse()
print "Response for: http://www.python.org/parrot.spam"
print r2.status, r2.reason
print
data2 = r2.read()                       # read reponse
datalines = data.splitlines(True)       # split into lines (keep line breaks)
sys.stdout.writelines(datalines[:5])    # print the first 5 lines
print "......"
sys.stdout.writelines(datalines[-10:])  # print the last 10 lines
print
conn.close()
