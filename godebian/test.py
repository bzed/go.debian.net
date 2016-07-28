from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///godebian.db', echo=True)


_URL_ID_TYPE = Integer
_URL_ID_SEQ = 'url_id_seq'
_metadata = MetaData()
_URL_TABLE = 'godebian_urls'

_urltable = Table(_URL_TABLE, _metadata,
                  Column('pk', Integer, primary_key=True),
                  Column('id', _URL_ID_TYPE, Sequence(_URL_ID_SEQ), index=True, unique=True, nullable=False),
                  Column('url', String, index=True, unique=False, nullable=True),
                  Column('is_static', Boolean, index=False, unique=False, nullable=False, default=False),
                  Column('create_date', DateTime, default=func.now()),
                  Column('log', Text, nullable=True),
                  )


class Url(object):
    """
    URL class is used to map against urltable in SQL
    """
    def __init__(self, url, id, is_static=False, log=None):
        self.url = url
        self.id = id
        self.is_static = is_static
        self.log = log

mapper(Url, _urltable)

_metadata.bind = engine
_metadata.create_all()


seq = Sequence(_URL_ID_SEQ)
id = engine.execute(seq)
print(engine.execute(seq.next_value()))
seq.next_value()

