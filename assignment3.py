#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    IS 211 Week 3 Assignment
"""

import csv
import argparse
import urllib2
import re

helpMesage = """\
Enter a URL linking to a .csv file.
Example URL: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
"""
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help=helpMesage)
args = parser.parse_args()


def downloadData(url):
    """Opens a supplied URL link.

    Args:
        url(str): A string for a website URL.

    Returns:
        datafile(various): A variable linked to an applicable datafile found at
        the supplied URL, if valid.

    Example:
        >>> downloadData('http://s3.amazonaws.com/cuny-is211-spring2015
        /weblog.csv')
        <addinfourl at 3043930156L whose fp = <socket._fileobject object at
        0xb56c4a6c>>
    """
    datafile = urllib2.urlopen(url)
    return datafile


def processData(datafile):
    """Processes a URL linked to a .csv file containing file pate, date & time,
    User-Agent, request status, and request size.

    Args:
        datafile(file): A .csv file supplied by user via a URL.

    Returns:
        msg(str): A string containing a synopsis of the number of page hits,
        the percentage of image requests, the browser with the most hits, and
        how many hits that browser had.

    Example:
        >>> load = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015
        /weblog.csv')
        >>> processData(load)
        There were 5000 page hits today, image requests account for 78.77% of
        hits. Google Chrome has the most hits with 2021.
    """

    readfile = csv.reader(datafile)
    linecount = 0
    imgcount = 0

    chrome = ['Google Chrome', 0]
    ie = ['Internet Explorer', 0]
    safari = ['Safari', 0]
    fox = ['Firefox', 0]
    for line in readfile:
        linecount += 1
        if re.search("firefox", line[2], re.I):
            fox[1] += 1
        elif re.search(r"MSIE", line[2]):
            ie[1] += 1
        elif re.search(r"Chrome", line[2]):
            chrome[1] += 1
        elif re.search(r"Safari", line[2]) and not re.search("Chrome", line[2]):
            safari[1] += 1
        if re.search(r"jpe?g|JPE?G|png|PNG|gif|GIF", line[0]):
            imgcount += 1

    img_hit_pct = (float(imgcount) / linecount) * 100

    brwsr_count = [chrome, ie, safari, fox]

    top_brwsr = 0
    top_name = ' '
    for b in brwsr_count:
        if b[1] > top_brwsr:
            top_brwsr = b[1]
            top_name = b[0]
        else:
            continue

    msg = ('There were {} page hits today, image requests account for {}% of '
           'hits. \n{} has the most hits with {}.').format(linecount,
                                                           img_hit_pct,
                                                           top_name,
                                                           top_brwsr)
    print msg


def main():
    """Combines downloadData function and processData into one script to be run
    on the command line."""
    if not args.url:
        raise SystemExit
    try:
        data = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        processData(data)

if __name__ == '__main__':
    main()
