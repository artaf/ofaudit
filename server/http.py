# -*- coding: utf-8 -*-
import collections
import functools
import inspect
import os
import werkzeug.local
import werkzeug.routing
import werkzeug.wrappers
from werkzeug.wsgi import SharedDataMiddleware
#from werkzeug.wrappers import Response
#from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound

from db import db_connect
from config import config
from templates import templates
from wsgi_apps import wsgi_apps

# 1 week cache for statics as advised by Google Page Speed
STATIC_CACHE = 60 * 60 * 24 * 7

#----------------------------------------------------------
# RequestHandler
#----------------------------------------------------------
# Thread local global request object
_request_stack = werkzeug.local.LocalStack()
request = _request_stack()

class WebRequest(object):
    def __init__(self, httprequest):
        self.httprequest = httprequest
        self.endpoint = None
        self.endpoint_arguments = None
        self.auth_method = None

    def set_handler(self, endpoint, arguments, auth):
        self.endpoint_arguments = arguments
        self.endpoint = endpoint
        self.auth_method = auth

    def _call_endpoint(self, *args, **kwargs):
        request = self
        if self.endpoint.routing['type'] != self._request_type:
            msg = "%s, %s: Function declared as capable of handling request of type '%s' but called with a request of type '%s'"
            params = (self.endpoint.original, self.httprequest.path, self.endpoint.routing['type'], self._request_type)
            raise werkzeug.exceptions.BadRequest(msg % params)
        if self.endpoint_arguments:
            kwargs.update(self.endpoint_arguments)
        return self.endpoint(*args, **kwargs)

    def __enter__(self):
        _request_stack.push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _request_stack.pop()


class JsonRequest(WebRequest):
    _request_type = "json"

    def __init__(self, *args):
        super(JsonRequest, self).__init__(*args)

    def dispatch(self):
        pass


class HttpRequest(WebRequest):
    _request_type = "http"

    def __init__(self, *args):
        super(HttpRequest, self).__init__(*args)
        params = collections.OrderedDict(self.httprequest.args)
        params.update(self.httprequest.form)
        params.update(self.httprequest.files)
        self.params = params

    def dispatch(self):
        r = self._call_endpoint(**self.params)
        if not r:
            r = Response(status=204)  # no content
        return r

    def render(self, template, qcontext=None, **kw):
#        response = Response(template=template, qcontext=qcontext, **kw)
#        return response.render()
        return templates.render(template, qcontext)

# rendering not used in this class
class Response(werkzeug.wrappers.Response):
    """ Response object passed through controller route chain.

    In addition to the :class:`werkzeug.wrappers.Response` parameters, this
    class's constructor can take the following additional parameters
    for QWeb Lazy Rendering.

    :param basestring template: template to render
    :param dict qcontext: Rendering context to use
    :param int uid: User id to use for the ir.ui.view render call,
                    ``None`` to use the request's user (the default)

    these attributes are available as parameters on the Response object and
    can be altered at any time before rendering

    Also exposes all the attributes and methods of
    :class:`werkzeug.wrappers.Response`.
    """
    default_mimetype = 'text/html'

    def __init__(self, *args, **kw):
        template = kw.pop('template', None)
        qcontext = kw.pop('qcontext', None)
        uid = kw.pop('uid', None)
        super(Response, self).__init__(*args, **kw)
        self.set_default(template, qcontext, uid)

    def set_default(self, template=None, qcontext=None, uid=None):
        self.template = template
        self.qcontext = qcontext or dict()
        self.uid = uid

    def render(self):
        return templates.render(self.template,self.qcontext)
#        start_response("404 Not Found", [])


        """ Renders the Response's template, returns the result
        """
#        env = request.env(user=self.uid or request.uid or odoo.SUPERUSER_ID)
#        self.qcontext['request'] = request
#        return env["ir.ui.view"].render_template(self.template, self.qcontext)



#----------------------------------------------------------
# Controller and route registration
#----------------------------------------------------------
controllers_per_module = collections.defaultdict(list)

class ControllerType(type):
    def __init__(cls, name, bases, attrs):
        super(ControllerType, cls).__init__(name, bases, attrs)
        name_class = ("%s.%s" % (cls.__module__, cls.__name__), cls)
        class_path = name_class[0].split(".")

#        if not class_path[:2] == ["odoo", "addons"]:
#            module = ""
#        else:
#            # we want to know all modules that have controllers
#            module = class_path[2]

        module = ""
        #module = class_path[2]
        # but we only store controllers directly inheriting from Controller
        if not "Controller" in globals() or not Controller in bases:
            return
        controllers_per_module[module].append(name_class)

Controller = ControllerType('Controller', (object,), {})

def route(route=None, **kw):
    """Decorator marking the decorated method as being a handler for
    requests. The method must be part of a subclass of ``Controller``.

    :param route: string or list. The route part that will determine which
                  http requests will match the decorated method.
                  Can be a single string or an array of strings.
                  See werkzeug's routing documentation for the format of
                  route expression (http://werkzeug.pocoo.org/docs/routing/ ).
    :param type: The type of request, can be ``'http'`` or ``'json'``.
    :param auth: The type of authentication method, can on of the following:

                 * ``user``: The user must be authenticated and the current request
                   will perform using the rights of the user.
                 * ``public``: The user may or may not be authenticated. If she isn't,
                   the current request will perform using the shared Public user.
                 * ``none``: The method is always active, even if there is no
                   database. Mainly used by the framework and authentication
                   modules. There request code will not have any facilities to access
                   the database nor have any configuration indicating the current
                   database nor the current user.
    :param methods: A sequence of http methods this route applies to. If not
                    specified, all methods are allowed.

    """
    routing = kw.copy()
    assert 'type' not in routing or routing['type'] in ("http", "json")
    def decorator(f):
        if route:
            if isinstance(route, list):
                routes = route
            else:
                routes = [route]
            routing['routes'] = routes
        @functools.wraps(f)
        def response_wrap(*args, **kw):
            response = f(*args, **kw)
## TODO: 
            if isinstance(response, Response): #or f.routing_type == 'json':
                return response

            if isinstance(response, werkzeug.wrappers.BaseResponse):

                print "werkzeug.wrappers.BaseResponse"

            if isinstance(response, basestring):

                print "basestring"

                return Response(response)
# TODO: wrong response
            return response

        response_wrap.routing = routing
        response_wrap.original_func = f
        return response_wrap
    return decorator


#----------------------------------------------------------
# WSGI Layer
#----------------------------------------------------------

# request.data json
# request.args.get('param') GET
# request.form.get('param') POST
# request.files  enctype=multipart/form-data
# request.values: объединены args и form, предпочитая args
#  = request.get_json() or request.values
class WsgiApp:
    """
    Root WSGI application for the Web Client.
    """
    routing_map = werkzeug.routing.Map(strict_slashes=False, converters=None)

    def __init__(self):
        self._loaded = False

    def get_request(self, httprequest):
        # deduce type of request
        if httprequest.args.get('jsonp'):
            return JsonRequest(httprequest)
        if httprequest.mimetype in ("application/json", "application/json-rpc"):
            return JsonRequest(httprequest)
        else:
            return HttpRequest(httprequest)

    def dispatch(self, environ, start_response):
        httprequest = werkzeug.wrappers.Request(environ)
        request = self.get_request(httprequest)

        print "req vals", [x for x in httprequest.values.iterlists()]

        with request:
            url_adapter = self.routing_map.bind_to_environ(environ)
            try:
                endpoint, arguments = url_adapter.match()
                print "endp", endpoint, "args:", arguments
# TODO auth ???
                request.set_handler(endpoint, arguments, "none")
                response = request.dispatch()
            except NotFound, e:
                response = e
            except (HTTPException, werkzeug.routing.RequestRedirect), e:
                response = e

            print "wsgi resp type: ", type(response)
            return response(environ, start_response)

    def wsgi_app(environ, start_response):
        # will be replace with SharedDataMiddleware
        pass

    def __call__(self, environ, start_response):
        if not self._loaded:
            self._loaded = True

            # db TODO: check if created
            SQLALCHEMY_DATABASE_URI = config['dbdriver']+':///' + config['dbname']
            self.db=db_connect(SQLALCHEMY_DATABASE_URI)
            print self.db

            # get all functions, they are endpoints, in Controller classes
            for _, cls in controllers_per_module[""]:
                obj = cls()
                members = inspect.getmembers(obj, inspect.ismethod)
                for _, mv in members: # member name + member instance
                    routing = dict(type='http', auth='user', methods=None, routes=None)
                    if hasattr(mv, 'routing'):
                        routing.update(mv.routing)

#                        print "has routing: ", mv, "auth: ", routing['auth'], "routing: ", mv.routing

                        assert routing['routes'], "Method %r has not route defined" % mv
                        for url in routing['routes']:
                            xtra_keys = 'defaults subdomain build_only strict_slashes redirect_to alias host'.split()
                            kw = {k: routing[k] for k in xtra_keys if k in routing}
                            endpoint = mv
#                            print "url:", url, "methods:", routing['methods'], "endp: "
                            self.routing_map.add(werkzeug.routing.Rule(url, endpoint=endpoint, methods=routing['methods'], **kw))

#                    print routing

            # add static folders
            statics={ '/static': os.path.join(config['basedir'], 'static') }
            self.wsgi_app = werkzeug.wsgi.SharedDataMiddleware(self.dispatch, statics, cache_timeout=STATIC_CACHE)

        return self.wsgi_app(environ, start_response)


wsgi_apps.append(WsgiApp())
