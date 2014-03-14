#!/usr/bin/env python

"""
Send the contents of a directory as a zipped and gpg encrypted MIME message.
"""

"""
    Inspired by
    -- send the entire contenets of a directory as an email message --
    appeared in
        18.1.11. email: Examples in Python library

    What I did:
        1. zip all contenets to a zip file
        2. encrypt the zip file using gpg

    Jay S. Liu
    jay.s.liu@gmail.com
    Mar. 14, 2014
    
    Usage: python mail_dir_enc.py -s sender -r recipient -p passphrase
            [-d directory/-o ouputFile]
"""

import os
import sys
import smtplib
# For guessing MIME type based on file name extension
import mimetypes

""" JSL """
import zipfile
import gnupg
""" JSL -- """

from optparse import OptionParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

""" JSL """
def zipdir(dir_name, zfile):
    """
    zip all files in a directory (dir_name), and
    save the zipped file (zfile)
    """
    #
    # specify: zipfile.ZIP_DEFLATED, if zlib is installed
    #           otherwise leave it out for no compression
    #
    zf = zipfile.ZipFile(zfile, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirs, files in os.walk(dir_name):
        for f in files:
            fn = os.path.join(dirpath, f)
            # no recursive on zfile itself
            if (fn == zfile) or (f == zfile) :
                print "skip"
                continue
            else: zf.write(fn)
    zf.close()

def sym_enc(infile, pf):
    """
    symmetric encryption file using gnupg
    """
    gpg = gnupg.GPG()
    outfile = infile + '.gpg'
    with open(infile, 'rb') as f:
        status = gpg.encrypt_file(
            f,
            recipients=[''],
            passphrase = pf,
            symmetric = True,
            output= outfile)

""" JSL -- """

def main():
    parser = OptionParser(usage="""\
Send the contents of a directory as a zipped+encrypted MIME message.

Usage: %prog [options]

Unless the -o option is given, the email is sent by forwarding to your local
SMTP server, which then does the normal delivery process.  Your local machine
must be running an SMTP server.
""")
    parser.add_option('-d', '--directory',
                      type='string', action='store',
                      help="""Mail the contents of the specified directory,
                      otherwise use the current directory.""")
    parser.add_option('-o', '--output',
                      type='string', action='store', metavar='FILE',
                      help="""Print the composed message to FILE instead of
                      sending the message to the SMTP server.""")
    parser.add_option('-s', '--sender',
                      type='string', action='store', metavar='SENDER',
                      help='The value of the From: header (required)')
    parser.add_option('-r', '--recipient',
                      type='string', action='append', metavar='RECIPIENT',
                      default=[], dest='recipients',
                      help='A To: header value (at least one required)')
    parser.add_option('-p', '--passphrase',
                      type='string', action='store', metavar='PASSPHRASE',
                      help='The passphrase for symmetric encryption (required)')
    opts, args = parser.parse_args()
    if not opts.sender or not opts.recipients  or not opts.passphrase:
        parser.print_help()
        sys.exit(1)
    directory = opts.directory
    if not directory:
        directory = '.'
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Contents of directory:  %s' % directory
    outer['To'] = COMMASPACE.join(opts.recipients)
    outer['From'] = opts.sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    #
    # JSL
    #   create the zipfile for specified directory, and 
    #       gpg encrypt it,
    #   both files are saved in the current working directory
    #   !!! they stay there until you remove them !!!
    #
    tfile = directory + ".zip"
    gpgfile = tfile + ".gpg"
    zipdir(directory, tfile)
    sym_enc(tfile, opts.passphrase)
    #
    # JSL --

    # set up mimetype for msg
    ctype, encoding = mimetypes.guess_type(gpgfile)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    # add gpgfile to msg
    fp = open(gpgfile, 'rb')
    msg = MIMEBase(maintype, subtype)
    msg.set_payload(fp.read())
    fp.close()

    # Set the filename parameter
    msg.add_header('Content-Disposition', 'attachment', filename=gpgfile)
    outer.attach(msg)
    # Now send or store the message
    composed = outer.as_string()
    if opts.output:
        fp = open(opts.output, 'w')
        fp.write(composed)
        fp.close()
    else:
        s = smtplib.SMTP('localhost')
        s.sendmail(opts.sender, opts.recipients, composed)
        s.quit()


if __name__ == '__main__':
    main()
