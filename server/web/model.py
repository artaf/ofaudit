# -*- coding: utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from server import db

engagements = Table('engagements', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(120)),
)

#query = Entry.query.order_by(Entry.pub_date.desc())