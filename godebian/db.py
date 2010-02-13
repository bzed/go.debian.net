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
IN NO EVENT SHALL THE FREEBSD PROJECT OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, \
                        Sequence
from sqlalchemy.orm import mapper

from .config import DatabaseConfig

_engine = create_engine(DatabaseConfig.connection, echo=DatabaseConfig.debug)
_metadata = MetaData()

_urltable = Table('godebian_urls', _metadata,
        Column('id', Integer, primary_key=True),
        Column('url', String, index=True, unique=True, nullable=True),
    )
_static_urltable = Table('godebian_static_urls', _metadata,
        Column('pk', Integer, primary_key=True),
        Column('id', Integer, index=True, unique=True, nullable=False),
        Column('url', String, index=True, unique=False, nullable=False),
    )

_metadata.create_all(_engine)

class Url(object):
    def __init__(self, url):
        self.url = url

class StaticUrl(object):
    def __init__(self, id, url):
        self.id = id
        self.url = url

mapper(Url, _urltable)
mapper(StaticUrl, _static_urltable)


