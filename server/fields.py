# -*- coding: utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import Column

from sqlalchemy import ForeignKey

from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# TODO:  do like in odoo?
#class AccountAccountType(models.Model):
#    _name = "account.account.type"
#    _description = "Account Type"

#    name = fields.Char(string='Account Type', required=True, translate=True)
