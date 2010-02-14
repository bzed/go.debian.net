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

from .config import MemcachedConfig

try:
    import pylibmc as memcache
except ImportError:
    import memcache

class MemCacheClass(object):
    def __init__(self, servers, timeout, prefix):
        self._client = memcache.Client(servers)
        self._timeout = timeout
        self._prefix = prefix
        self._pkey = lambda x: "%s:%s" %(prefix, x)

    def add(self, key, value):
        return self._client.add(self._pkey(key), value, self._timeout)

    def set(self, key, value):
        return self._client.set(self._pkey(key), value, self._timeout)

    def get(self, key, default=None):
        value = self._client.get(self._pkey(key))
        if value is None:
            return default
        return value

    def close(self):
        self._client.disconnect_all()

_servers = MemcachedConfig.servers.split(';')
_timeout = MemcachedConfig.timeout
_prefix = MemcachedConfig.prefix
MemCache = MemCacheClass(_servers, _timeout, _prefix)
