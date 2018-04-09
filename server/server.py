# -*- coding: utf-8 -*-
#import sys

from werkzeug.serving import run_simple

from wsgi_apps import application

def main():
    run_simple('127.0.0.1', 5000, application, use_debugger=True, use_reloader=True) #static_files
