# -*- coding: utf-8 -*-

import urlparse

#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()
#from sqlalchemy import ForeignKey
#from sqlalchemy.orm import relationship

#session.commit()
#session.rollback()
#session.query()
#session.delete()

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy.orm import dynamic_loader
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import mapper

from werkzeug.utils import cached_property

#from werkzeug.local import Local, LocalManager
#local = Local()
#local_manager = LocalManager([local])
#application = local('application')

metadata = MetaData()


###
#engine = create_engine('sqlite:///:memory:', echo=True)
#from sqlalchemy.orm import sessionmaker
#Session = sessionmaker(bind=engine)
#session = Session()
#session.close()
###

class DBConnection(object):
    def __init__(self, db_uri):
        self.dburi = db_uri
        us = urlparse.urlsplit(db_uri)
#        print us
        if len(us.netloc) > 1:
            self.dbname = us.netloc
        self.database_engine = create_engine(self.dburi, echo=True)
#        session_factory = sessionmaker(bind=self.engine)()
#        self.session = 
        session_factory = create_session(self.database_engine, autoflush=True, autocommit=False)
        self.session = scoped_session(session_factory)
#        self.metadata = MetaData()

    def close(self):
#        self.session.close()
        self.session.remove()

#    def __bool__(self):
#        raise NotImplementedError()

#    __nonzero__ = __bool__

def db_connect(db_uri):
    return DBConnection(db_uri)
###


class Pagination(object):
    """
    Paginate a SQLAlchemy query object.
    """
    def __init__(self, query, per_page, page, endpoint):
        self.query = query
        self.per_page = per_page
        self.page = page
        self.endpoint = endpoint

    @cached_property
    def entries(self):
        return self.query.offset((self.page - 1) * self.per_page) \
                         .limit(self.per_page).all()

    @cached_property
    def count(self):
        return self.query.count()

    has_previous = property(lambda x: x.page > 1)
    has_next = property(lambda x: x.page < x.pages)
    previous = property(lambda x: url_for(x.endpoint, page=x.page - 1))
    next = property(lambda x: url_for(x.endpoint, page=x.page + 1))
    pages = property(lambda x: max(0, x.count - 1) // x.per_page + 1)
