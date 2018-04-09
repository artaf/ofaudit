# -*- coding: utf-8 -*-
import os
import sys

config={}

config['basedir'] = os.path.dirname(sys.argv[0])
config['dbname'] = os.path.join(config['basedir'],'testdb.sqlite')
config['dbdriver'] = "sqlite"
config['dbuser'] = ""
config['dbpassword'] = ""
config['dbhost'] = ""
config['dbport'] = 0

# dialect+driver://username:password@host:port/database
#SQLALCHEMY_DATABASE_URI = config['dbdriver']+':///' + config['dbname']
#SQLALCHEMY_DATABASE_URI =  'postgresql://scott:tiger@localhost/mydatabase'

SQLALCHEMY_MIGRATE_REPO = os.path.join(config['basedir'], 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS=True
SQLALCHEMY_ECHO = True
