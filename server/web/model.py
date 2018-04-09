# -*- coding: utf-8 -*-

#from sqlalchemy import Table
#from sqlalchemy import Column
#from sqlalchemy import ForeignKey
#from sqlalchemy import Boolean
#from sqlalchemy import Integer
#from sqlalchemy import String
#from sqlalchemy import DateTime

from server import db
from server.fields import Base, Column, Integer, String

#engagements = Table('engagements', db.metadata,
#    Column('id', Integer, primary_key=True),
#    Column('name', String(120)),
#)

#query = Entry.query.order_by(Entry.pub_date.desc())

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)

class AuditEngagements(Base):
    __tablename__ = 'audit_engagements'
    id = Column(Integer, primary_key=True)
    name = Column(String)

