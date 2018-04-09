# -*- coding: utf-8 -*-

import werkzeug.exceptions

# why do we need more than one?
wsgi_apps=[]

def application(environ, start_response):

#    with odoo.api.Environment.manage():
    for handler in wsgi_apps:
        result = handler(environ, start_response)
        if result is None:
            continue
        return result
    # We never returned from the loop.
    return werkzeug.exceptions.NotFound("No handler found.\n")(environ, start_response)
