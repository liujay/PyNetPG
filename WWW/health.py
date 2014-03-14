#!/usr/bin/env python

"""Web Crawler/Spider

This module implements a web crawler. This is very _basic_ only
and needs to be extended to do anything usefull with the
traversed pages.
"""

"""

    Jay S. Liu
    jay.s.liu@gmail.com

    May 14, 2012
"""

import sys
import time
import math
import optparse
import wc
import my_check

def parse_options():
    """parse_options() -> opts, args

    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser()

    parser.add_option("-q", "--quiet",
            action="store_true", default=False, dest="quiet",
            help="Enable quiet mode")

    parser.add_option("-l", "--links",
            action="store_true", default=False, dest="links",
            help="Get links for specified url only")

    parser.add_option("-d", "--depth",
            action="store", type="int", default=1, dest="depth",
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
    global verbose

    opts, args = parse_options()

    home = args[0]

    depth = opts.depth
    verbose = opts.verbose

    print "Crawling %s (Max Depth: %d)" % (home, depth)
    crawler = wc.Crawler(home, depth, locked=False)
    crawler.crawl()
    
    count = 0
    healthy = 0
    un_healthy =0
    for url in crawler.urls:
        count += 1
        if verbose:
            print >> sys.stdout, "Checking on: %s" % url
        else:
            sys.stdout.write(".\n")
            sys.stdout.flush()
        if my_check.check_url(url):
            healthy += 1
        else:
            un_healthy += 1
            
    print "\nHealth check for url: %s" % home
    print count, healthy, un_healthy



if __name__ == "__main__":
    main()
