#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Bernd Zeimetz"
__contact__ = "bzed@debian.org"
__license__ = """
Copyright (C) 2010 Bernd Zeimetz <bzed@debian.org>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys

def config():
    print """graph_args --base 1000 -l 0 --vertical-label URLs
graph_title deb.li usage
graph_category deb.li
graph_info This graphs shows statistics of the number of URLs stored in deb.li.
graph_order dynamic custom
dynamic.label dynamically generated ShortURLs
custom.label custom ShortURLs
dynamic.draw AREA
custom.draw STACK
dynamic.info ShortURLs which were automatically generated while inserting a new URL.
custom.info Custom ShortURL which was assigned on request."""

def stats():
    from godebian.manage import count
    print "dynamic.value %s\ncustom.value %s" \
            %(str(count(is_static=False)), str(count(is_static=True)))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'config':
            config()
    else:
        stats()

