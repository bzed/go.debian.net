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

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, \
                        Sequence, Boolean, and_, func, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exc import IntegrityError, DataError

from .config import DatabaseConfig

_engine = create_engine(DatabaseConfig.connection, echo=DatabaseConfig.debug)
_metadata = MetaData()

_URL_ID_TYPE = Integer
if DatabaseConfig.connection.startswith('postgres'):
    from sqlalchemy.databases.postgres import PGBigInteger
    _URL_ID_TYPE = PGBigInteger

_URL_TABLE = 'godebian_urls'
_URL_ID_SEQ = 'url_id_seq'
_urltable = Table(_URL_TABLE, _metadata,
        Column('pk', Integer, primary_key=True),
        Column('id', _URL_ID_TYPE, Sequence(_URL_ID_SEQ), index=True, unique=True, nullable=False),
        Column('url', String, index=True, unique=False, nullable=True),
        Column('is_static', Boolean, index=False, unique=False, nullable=False, default=False),
        Column('create_date', DateTime, default=func.now()),
        Column('log', Text, nullable=True),
    )
_metadata.create_all(_engine)

class Url(object):
    def __init__(self, url, id, is_static=False, log=None):
        self.url = url
        self.id = id
        self.is_static = is_static
        self.log = log

mapper(Url, _urltable)
_Session = sessionmaker(bind=_engine)

class DbException(Exception):
    def __init__(self, id, url):
        self.id = id
        self.url = url

class DbIdExistsException(DbException):
    def __str__(self):
        return "Id %s exists in Database" % (str(self.id), )

class DbIdOutOfRangeException(DbException):
    def __str__(self):
        return "Id %s is too large to be inserted into the database" %(str(self.id), )

def get_url(id):
    session = _Session()
    url = session.query(Url.url).filter(Url.id == id)[:1]
    session.close()
    if url:
        return url[0][0]
    return None


def add_url(url, static_id=None, log=None):
    def _add_url_to_session(session, url, id, is_static=False, log=None):
        new_urlobj = Url(url, id, is_static, log)
        session.add(new_urlobj)
        session.flush()

    def _abort_session(session):
        session.rollback()
        session.close()

    session = _Session()
    if not static_id:
        """ Check if the requested URL is in the database already,
            if so return the id of the existing entry. If not,
            find the next unused id.
        """
        id_query = session.query(Url.id).filter(and_(Url.url == url, 
                                               Url.is_static == False))[:1]
        if id_query:
            _abort_session(session)
            return id_query[0][0]

        id = session.execute("""select nextval('%s');""" % (_URL_ID_SEQ,)).fetchone()[0]
        session.execute("""LOCK TABLE %s in SHARE MODE""" % (_URL_TABLE, ))
        while session.query(Url.id).filter(Url.id == id)[:1]:
            id = session.execute("""select nextval('%s');""" % (_URL_ID_SEQ,)).fetchone()[0]
        _add_url_to_session(session, url, id, False, log)

    else:
        """ A static id was requested. In case the id is used already, an
            UrlIdExistsException is raised. """
        id = static_id
        try:
            _add_url_to_session(session, url, id, True, log)
        except IntegrityError:
            _abort_session(session)
            raise UrlIdExistsException(id, url)
        except DataError:
            _abort_session(session)
            raise UrlIdOutOfRangeException(id, url)
    session.commit()
    session.close()
    return id

