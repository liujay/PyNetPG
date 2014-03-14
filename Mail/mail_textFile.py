"""
how to create and send a simple text message
Adapted from
    18.1.11. email: Examples

    Jay S Liu
    jay.s.liu@gmail.com
    Mar. 14, 2014

"""

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

import sys

#
#   check if we have required parameters
#
if len(sys.argv) < 4:
    print "usage: %s server textfile from_addr to_addr [to_addr]" % sys.argv[0]
    sys.exit(2)

#
#   rename sy.argv[] to local variables
#
server, textfile, me, you = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

msg['Subject'] = 'The contents of %s, sent by %s' % (textfile, sys.argv[0])
msg['From'] = me

s = smtplib.SMTP(server)

#
#   if you do not intend to disclose recipients
#       do these:
for rcpt in you:
    s.sendmail(me, rcpt, msg.as_string())

#
#   if you intend to disclose all recipients' address
#       do these:
"""
msg['To'] = you
s.sendmail(me, [you], msg.as_string())
"""
s.quit()