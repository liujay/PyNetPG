"""
source:
    http://code.activestate.com/recipes/286225-httpexists-find-out-whether-an-http-reference-is-v/

    commented by: Sam Peterson

    minor modification by:
    Jay S Liu
    jay.s.liu@gmail.com
    May 20, 2013

"""

import sys

def check_url(url, redirect_limit=5):
    """Perform HEAD, may throw socket errors"""

    import httplib, urlparse

    def _check(url):
        """Returns a http response object"""

        netloc, path = urlparse.urlsplit(url)[1:3]

        connection = httplib.HTTPConnection(netloc)
        try:
            connection.request("HEAD", path)
            rtn = connection.getresponse()
        except:
            print >> sys.stderr, "  Connection/Response Error on url: %s" % url
            return None
        if isinstance(rtn, httplib.HTTPResponse):       # assert return type
            return rtn
        else:
            return None

    # redirection limit, default of 5
    redirect = redirect_limit
    original_url = url              # save url for output

    # Perform HEAD
    resp = _check(url)
    if resp == None:
        return 0

    # check for redirection
    exist_list = [200, 201, 202, 203, 204, 205, 206]
    redirect_list = [300, 301, 302, 303, 307]

    while resp.status in redirect_list:
        if redirect == redirect_limit:              # first entry
            print >> sys.stderr, "  Redirection on url: %s" % original_url
        # tick the redirect
        redirect -= 1

        # if redirect is 0, we tried :-(
        if redirect == 0:
            # we hit our redirection limit
            print >> sys.stderr, "  Reaching redirection limit on url: %s" % original_url            
            return 0

        # Perform HEAD
        url = resp.getheader('location')
        resp = _check(url)
        if resp == None:
            return 0

    if resp.status in exist_list:
        return 1

    else:
        # Status unsure, might be, 404, 500, 401, 403, raise error
        # with actual status code.
        print >> sys.stderr, "  Not Found on url: %s" % url        
        return 0

def test():
    print check_url("http://www.fcu.edu.tw/")
    print check_url("http://liuj.fcu.edu.tw/")
    print check_url("http://www.fcu.edu.tw/joke/")

if __name__ == "__main__":
    test()
