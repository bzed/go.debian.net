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

THIS SOFTWARE IS PROVIDED BY THE FREEBSD PROJECT ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE FREEBSD PROJECT OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from application.configuration import ConfigSection

#from application.process import process
#print process.system_config_directory, process.local_config_directory


class UrlencoderConfig(ConfigSection):
    alphabet = '1qw2ert3yuio4pQWER5TYUIOP6asdfghj7klASDFG8HJKLzxcv9bnmZXCVBN0M'
    blocksize = 22
UrlencoderConfig.read('godebian.conf', 'urlencoder')

class DatabaseConfig(ConfigSection):
    connection = 'postgresql+psycopg2://user@password@host:port/dbname'
    debug = False
DatabaseConfig.read('godebian.conf', 'database')
