#!/usr/bin/env python

"""Web Crawler/Spider

This module implements a web crawler. This is very _basic_ only
and needs to be extended to do anything usefull with the
traversed pages.
"""

"""Modified Version

The depth defined in the original version is unusual?!
This modified version allows us to follow usual definition in depth:
    number of hops that page is away from the root.

    BFS was used to implement the crawling.

    Jay S. Liu
    jay.s.liu@gmail.com

    May 15, 2012
"""

import re
import sys
import time
import math
import urllib2
import urlparse
import optparse
from cgi import escape
from traceback import format_exc
from Queue import Queue, Empty as QueueEmpty

from BeautifulSoup import BeautifulSoup

__version__ = "0.2.3"               # JSL
__copyright__ = "CopyRight (C) 2008-2011 by James Mills"
__license__ = "MIT"
__author__ = "James Mills"
__author_email__ = "James Mills, James dot Mills st dotred dot com dot au"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)

class Crawler(object):

    def __init__(self, root, depth, locked=True, verbose=False):
        self.root = root
        self.depth = depth
        self.locked = locked
        self.verbose = verbose
        self.host = urlparse.urlparse(root)[1]
        self.urls = []                                  # result stored here
        self.links = 0
        self.followed = 0

    def crawl(self):
        #
        # starting from root
        #
        page = Fetcher(self.root)
        page.fetch()
        q = Queue()
        #
        # take care of level 1 -- reachable urls from root
        #
        height = 1
        for url in page.urls:
            if url not in self.urls:
                host = urlparse.urlparse(url)[1]
                if re.match(".*%s" % self.host, host) or not self.locked:
                    self.links += 1
                    q.put((height, url))            # save url and its depth in queue
                    self.urls.append(url)
        followed = [self.root]

        #
        # other levels -- using BFS
        #
        while True:
            #
            # get the head elment of the queue
            #
            try:
                site = q.get(False)
                height = site[0]                # height
                url = site[1]                   # url
                if self.verbose:
                    print >> sys.stderr, "DeQueue: ", height, url
            except QueueEmpty:
                break
            #
            # BFS -- finding new urls in next level
            #
            n_height = height + 1
            if n_height > self.depth and self.depth > 0:
                break
            if url not in followed:             # this url has not been processed before
                try:
                    host = urlparse.urlparse(url)[1]
                    if re.match(".*%s" % self.host, host) or not self.locked:
                        followed.append(url)    # mark it as processed
                        self.followed += 1
                        page = Fetcher(url)     # search new urls
                        page.fetch()
                        for i, url in enumerate(page):
                            if url not in self.urls:    # found new one
                                self.links += 1
                                q.put((n_height, url))  # add it to queue for BFS
                                self.urls.append(url)   # add it to result
                except Exception, e:
                    print "ERROR: Can't process url '%s' (%s)" % (url, e)
                    print format_exc()
            else:
                if self.verbose:
                    print >> sys.stderr, "skipping ---- ", url

class Fetcher(object):

    def __init__(self, url):
        self.url = url
        self.urls = []

    def __getitem__(self, x):
        return self.urls[x]

    def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def open(self):
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)

    def fetch(self):
        request, handle = self.open()
        self._addHeaders(request)
        if handle:
            try:
                content = unicode(handle.open(request).read(), "utf-8",
                        errors="replace")
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urlparse.urljoin(self.url, escape(href))
                    if url not in self:
                        self.urls.append(url)

def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print "%d. %s" % (i, url)

def parse_options():
    """parse_options() -> opts, args

    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-q", "--quiet",
            action="store_true", default=False, dest="quiet",
            help="Enable quiet mode")

    parser.add_option("-l", "--links",
            action="store_true", default=False, dest="links",
            help="Get links for specified url only")

    parser.add_option("-d", "--depth",
            action="store", type="int", default=3, dest="depth",
            help="Maximum depth to traverse")

    parser.add_option("-v", "--verbose",
            action="store_true", default=False, dest="verbose",
            help="Enable verbose mode")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit, 1

    return opts, args

def main():

    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

    sTime = time.time()

    print "Crawling %s (Max Depth: %d)" % (url, depth)
    crawler = Crawler(url, depth, verbose = opts.verbose)
    crawler.crawl()
    print "\n".join(crawler.urls)

    eTime = time.time()
    tTime = eTime - sTime

    print "Found:    %d" % crawler.links
    print "Followed: %d" % crawler.followed
    print "Stats:    (%d/s after %0.2fs)" % (
            int(math.ceil(float(crawler.links) / tTime)), tTime)

if __name__ == "__main__":
    main()
