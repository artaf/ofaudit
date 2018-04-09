# -*- coding: utf-8 -*-

from server import http
from server import db
from model import *


PER_PAGE = 30

# test context
user = User()
CONTEXT ={ 'company': 'Test Company', 'user': user }


class Home(http.Controller):
    """
    Functions are called as endpoints func(request, **values)
    :returns: Response or string 
    """
    @http.route(['/','/index'], type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        context = CONTEXT.copy()
        context.update( {} ) #request.env['ir.http'].webclient_rendering_context()
        return http.request.render('index.html', qcontext=context)

    @http.route('/login', type='http', auth="none")
    def login(self):
        context = CONTEXT.copy()
        context.update( {} ) #request.env['ir.http'].webclient_rendering_context()
        return http.request.render('login.html', qcontext=context)

class Menu(http.Controller):
    @http.route('/menu', type='http', auth="user")
    def menu(self):
        # return from DB
        menu = { 1: 'Menu 1', 2: 'Menu 2', 3: 'Menu 3' }
        context = CONTEXT.copy()
        context.update( {'menu': menu} )
        print context
        return http.request.render('menu.mako', qcontext=context)


class View(http.Controller):
    @http.route('/view/<int:model>/<int:page>', type='http', auth="user")
    def view_tree(self, model=None, page=1):
        query = 'q'
        pagination = db.Pagination(query, PER_PAGE, page, 'index')
        context = CONTEXT.copy()
        context.update( { 'pagination': pagination } )
        return http.request.render('login.html', qcontext=context)
#        return "view tree model {0} page {1}.".format(str(model), str(page))
