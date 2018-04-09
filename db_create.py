# -*- coding: utf-8 -*-

import os.path
from migrate.versioning import api

from server.config import config
from server.config import SQLALCHEMY_MIGRATE_REPO
from server import db


#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), 'addons'))
#import audit_isa

SQLALCHEMY_DATABASE_URI = config['dbdriver']+':///' + config['dbname']

dbi = db.db_connect(SQLALCHEMY_DATABASE_URI)
db.metadata.create_all(dbi.database_engine)

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
