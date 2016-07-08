# -*- coding: utf-8 -*-
__author__ = "Bernd Zeimetz"
__contact__ = "bzed@debian.org"
__license__ = """
Copyright (C) 2010-2013 Bernd Zeimetz <bzed@debian.org>

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

import os
import re
import IPy

from application.configuration import ConfigSection, ConfigSetting
from application.process import process

# swap config directories, makes more sense in our case.
process.local_config_directory = process.system_config_directory
process.system_config_directory = os.path.realpath(os.path.dirname(__file__))


class IPyNetworkRangeList(list):
    """
    The IP class allows a comfortable parsing and handling for most
    notations in use for IPv4 and IPv6 addresses and networks. It was
    greatly inspired by RIPE's Perl module NET::IP's interface but
    doesn't share the implementation. It doesn't share non-CIDR netmasks,
    so funky stuff like a netmask of 0xffffff0f can't be done here.
    """
    def __new__(cls, value):
        if isinstance(value, (tuple, list)):
            return [IPy.IP(x) for x in value]
        elif isinstance(value, basestring):
            if value.lower() in ('none', ''):
                return []
            return [IPy.IP(x) for x in re.split(r'\s*,\s*', value)]
        else:
            raise TypeError("value must be a string, list or tuple")


class UrlencoderConfig(ConfigSection):
    """
    Convert a mapping object or a sequence of two-element tuples to a “percent-encoded” string,
    suitable to pass to urlopen() above as the optional data argument.
    alphabet : URL encoder default alphabets used for regex compiling in urlencoder.py
    blocksize: length of block allowed
    """
    alphabet = '1qw2ert3yuio4pQWER5TYUIOP6asdfghj7klASDFG8HJKLzxcv9bnmZXCVBN0M'
    blocksize = 22


UrlencoderConfig.read('godebian.conf', 'urlencoder')


class DatabaseConfig(ConfigSection):
    """
    SQLalchemy database configurations
    debug : True initiates SQLalchemy in verbose debug mode
    connection : <sqlengine>://<db_name>
    """
    connection = 'postgresql:///godebian'
    debug = False


DatabaseConfig.read('godebian.conf', 'database')


class MemcachedConfig(ConfigSection):
    """
    Configurations for Memcache daemon
    server : <ip>:<port>
    timeout : request timeout period
    Memcache prefix : key prefixes
    """
    servers = '127.0.0.1:11211'
    timeout = 600
    prefix = 'godebian'


MemcachedConfig.read('godebian.conf', 'memcached')


class FlaskConfig(ConfigSection):
    """
    Flask config context
    debug : True sets verbose mode
    static_dir : location of directory containing static files like css,js,images etc
    template_dir : location of jinja2 templates folder
    allowed_rpc_ips : Allowed IP address for rpc_json api
    """
    debug = False
    template_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'web', 'views'))
    static_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'web', 'static'))
    allowed_rpc_ips = ConfigSetting(type=IPyNetworkRangeList, value=[])
    domain = 'deb.li'
    google_site_verification = ''
    max_content_length = 4 * 1024


FlaskConfig.read('godebian.conf', 'flask')
