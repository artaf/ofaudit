# -*- coding: utf-8 -*-

from server import http
from server import db


PER_PAGE = 30

class Home(http.Controller):
    """
    Functions are called as endpoints func(request, **values)
    :returns: Response or string 
    """
    @http.route(['/','/index'], type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        context = {} #request.env['ir.http'].webclient_rendering_context()
        return http.request.render('index.html', qcontext=context)

    @http.route('/login', type='http', auth="none")
    def login(self):
        context = {} #request.env['ir.http'].webclient_rendering_context()
        return http.request.render('login.html', qcontext=context)

class Menu(http.Controller):
    @http.route('/menu', type='http', auth="user")
    def menu(self):
        return "menu"


class View(http.Controller):
    @http.route('/view/<int:model>/<int:page>', type='http', auth="user")
    def view_tree(self, model=None, page=1):
        query = 'q'
        pagination = db.Pagination(query, PER_PAGE, page, 'index')
        context = { 'pagination': pagination }
        return http.request.render('login.html', qcontext=context)
#        return "view tree model {0} page {1}.".format(str(model), str(page))
