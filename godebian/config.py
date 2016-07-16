# -*- coding: utf-8 -*-
from __future__ import print_function

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
from types import ClassType, TypeType
import json

config_files = dict(production="/etc/godebian_config.json",
                    development="godebian_config.json")

#production_mode = False for development mode
production_mode = False


class FileNotFound(Exception):
    """
    Raised when specified config file path does not exist
    """
    def __init__(self,fname):
        self.fname = fname

    def __str__(self):
        return "File not found at location {0}".format(self.fname)


def get_config_dict():
    """
    config data priority:
    config attributes mentioned in class declaration can be overriden by data in json files
    Selection of JSON file is done by checking production_mode flag
    :return: data : configuration data loaded from json file in dict format
    """
    if production_mode:
        fname = config_files['production']
    else:
        fname = config_files['development']

    if not os.path.exists(fname):
        raise FileNotFound(fname=fname)

    with open(fname) as data_file:
        data = json.load(data_file)

    return data


class ConfigSection(object):
    """
    Defines a section in the configuration file

    Settings defined in superclasses are not inherited, but cloned as if
    defined in the subclass using ConfigSetting. All other attributes
    are inherited as normal.
    """

    @classmethod
    def __read__(cls, section):
        """
        :param section: section can be database,urlencoder,memcached,flask
        :return:
        """
        data = get_config_dict()
        if data:
            if data.get(section,False):
                for key,value in data.get(section).items():
                    try:
                        setattr(cls,key,value)
                    except Exception as e:
                        msg = "ignoring invalid config value: %s.%s=%s (%s)." % (section, key, value, e)
                        print(msg)
            else:
                raise ValueError("A config file and section are required for reading settings")

    #monkey patch
    read = __read__


class ConfigSetting(object):
    """
    Code belongs to python-application package in application/configuration/__init__.py
    Hacky way to keep things from breaking
    Used here so as no much code updating is required while porting this code
    """
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.type_is_class = isinstance(type, (ClassType, TypeType))

    def __get__(self, obj, objtype):
        return self.value

    def __set__(self, obj, value, convert=True):
        if convert and value is not None and not (self.type_is_class and isinstance(value, self.type)):
            value = self.type(value)
        self.value = value


# swap config directories, makes more sense in our case.
# process.local_config_directory = process.system_config_directory
# process.system_config_directory = os.path.realpath(os.path.dirname(__file__))

class IPyNetworkRangeList(list):
    """
    Todo:
    replace IP based verification to token based

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
UrlencoderConfig.read(section='urlencoder')


class DatabaseConfig(ConfigSection):
    """
    SQLalchemy database configurations
    debug : True initiates SQLalchemy in verbose debug mode
    connection : <sqlengine>://<db_name>
    """
    connection = 'postgresql:///godebian'
    debug = False
DatabaseConfig.read(section='database')


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
MemcachedConfig.read(section='memcached')


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
FlaskConfig.read(section='flask')
