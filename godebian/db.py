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

import urllib

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, \
    Sequence, Boolean, and_, func, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exc import IntegrityError, DataError

from .config import DatabaseConfig

_engine = create_engine(DatabaseConfig.connection, echo=DatabaseConfig.debug)
_metadata = MetaData()

_URL_ID_TYPE = Integer
# sqlalchemy.Integer is not supported with postgres
# check if DB used is postgresql then use
# sqlalchemy.databases.postgres.PGBigInteger or sqlalchemy.databases.postgres.BIGINT
if DatabaseConfig.connection.startswith('postgres'):
    try:
        from sqlalchemy.databases.postgres import PGBigInteger

        _URL_ID_TYPE = PGBigInteger
    except ImportError:
        from sqlalchemy.databases import postgresql

        _URL_ID_TYPE = postgresql.BIGINT

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
    """
    URL class is used to map against urltable in SQL
    """
    def __init__(self, url, id, is_static=False, log=None):
        self.url = urllib.unquote(url)
        self.id = id
        self.is_static = is_static
        self.log = log


mapper(Url, _urltable)
_session = sessionmaker(bind=_engine)


class DbException(Exception):
    """
    Base class for DB exception handling
    """
    def __init__(self, id, url):
        self.id = id
        self.url = url


class DbIdExistsException(DbException):
    """
    This exception will be raised if supplied ID already exists in DB
    """
    def __str__(self):
        return "Id %s exists in Database" % (str(self.id),)


class DbIdOutOfRangeException(DbException):
    """
    Raised when supplied ID is too large
    """
    def __str__(self):
        return "Id %s is too large to be inserted into the database" % (str(self.id),)


def get_url(id):
    """

    :param id: id of shortened URL
    :return: None or URL
    """
    session = _session()
    url = session.query(Url.url).filter(Url.id == id)[:1]
    session.close()
    if url:
        return url[0][0]
    return None


def add_url(url, static_id=None, log=None):
    """

    :param url: url to be shortened
    :param static_id:
    :param log:
    :return: id of shortened URL
    """

    def _add_url_to_session(session, url, id, is_static=False, log=None):

        # Creating new SQLalchemy ORM Object of URL table and adding it to current SQLalchemy session
        new_urlobj = Url(url, id, is_static, log)
        session.add(new_urlobj)
        session.flush()

    def _abort_session(session):
        """
        this func performs rollback, to be called when there is error in DB transaction
        :param session: SQLalchemy session
        :return:
        """
        session.rollback()
        session.close()

    session = _session()
    if not static_id:
        """
        Check if the requested URL is in the database already,
        if so return the id of the existing entry. If not,
        find the next unused id.
        """
        id_query = session.query(Url.id).filter(and_(Url.url == urllib.unquote(url),
                                                     Url.is_static == False))[:1]
        if id_query:
            _abort_session(session)
            return id_query[0][0]

        id = session.execute("""select nextval('%s');""" % (_URL_ID_SEQ,)).fetchone()[0]
        # Perform Shared/Read LOCK on Table
        session.execute("""LOCK TABLE %s in SHARE MODE""" % (_URL_TABLE,))
        while session.query(Url.id).filter(Url.id == id)[:1]:
            id = session.execute("""select nextval('%s');""" % (_URL_ID_SEQ,)).fetchone()[0]
        _add_url_to_session(session, url, id, False, log)

    else:
        """
        A static id was requested. In case the id is used already, an
        DbIdExistsException is raised.
        """
        id = static_id
        try:
            _add_url_to_session(session, url, id, True, log)
        except IntegrityError:
            _abort_session(session)
            raise DbIdExistsException(id, url)
        except DataError:
            _abort_session(session)
            raise DbIdOutOfRangeException(id, url)
    # call commit() to save changes, necessary only if autocommit is OFF
    session.commit()
    session.close()
    return id


def update_url(url, static_id, log=None):
    """
    This function will update static_url mapping of static_id and mapped URL
    :param url: url to be updated
    :param static_id:
    :param log:
    :return: id
    """

    def _update_url_in_session(session, url, id, log=None):
        url_obj = session.query(Url).filter_by(id=id).filter_by(is_static=True).first()
        url_obj.url = url
        session.flush()

    def _abort_session(session):
        """
        this func performs rollback, to be called when there is error in DB transaction
        :param session: SQLalchemy session
        :return:
        """
        session.rollback()
        session.close()

    session = _session()
    try:
        _update_url_in_session(session, url, static_id, log)
    except IntegrityError:
        _abort_session(session)
        raise DbIdExistsException(id, url)
    except DataError:
        _abort_session(session)
        raise DbIdOutOfRangeException(id, url)
    session.commit()
    session.close()
    return id


def count(is_static=False):
    """
    Count total number of static and non static URLs
    Default count non-static ones
    :param is_static:
    :return: count
    """
    session = _session()
    # could be replaced by session.query(sqlalchemy.func.count(Url).scalar()
    count = session.query(Url).filter(Url.is_static == is_static).count()
    session.close()
    return count
