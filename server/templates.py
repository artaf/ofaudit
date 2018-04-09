# -*- coding: utf-8 -*-

import os

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from config import config


class Tmplt(object):
    tmplt_lookup = None

    def __init__(self):
        tmplt_dirs = [os.path.join(config['basedir'],'static/templates'), ]
        self.tmplt_lookup = TemplateLookup(directories=tmplt_dirs, collection_size=500) #module_directory='/tmp/mako_modules'
#        print tmplt_dirs

    def render(self, template, qcontext):
#        print "render: ", template
        try:
            tmplt = self.tmplt_lookup.get_template(template)
#            print tmplt
        except exceptions.TopLevelLookupException:
            print ("Cant find template '%s'") % template
            return str.encode("Cant find template '%s'" % template)
        try:
            return tmplt.render(**qcontext)
        except:
            return exceptions.html_error_template().render()

templates = Tmplt()

if __name__ == "__main__":
#    config['basedir']=''
    r = templates.render('index.html', dict() )
    print type(r)

