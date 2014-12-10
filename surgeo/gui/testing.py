import os
import pickle
import re
import sqlite3
import threading
import time
from cgi import parse_qs, escape
from wsgiref.simple_server import make_server


def index(environ, start_response):
    '''Index is mounted at '/'.'''
    start_response('200 OK', [('Content-Type', 'text/html'), 
                              ('Expires', 'Mon, 25 Jun 2020 21:31:12 GMT')])
    return [str(open(os.path.join(settings_dict['application_dir'],
                                  'index_page.html')).read())]

def submit(environ, start_response):
    '''This takes POST data and is mounted at 'tuzigoot/submit'.'''
    try:
       request_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
       request_body_size = 0
    try:
        request_body = environ['wsgi.input'].read(request_size)
        post_data = parse_qs(request_body)
        company = post_data.get('Company')[0]
        product = post_data.get('Product')[0]
        subprod = post_data.get('Subprod')[0]
        frequency = post_data.get('Frequency')[0]
        try:
            email = post_data.get('email')[0]
        except TypeError:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [str('Invalid address or unpermitted domain.')]
        # WSIG escape
        email = escape(email)
        # case insensitive
        email = email.lower()
        company = escape(company)
        subprod = escape(subprod)
        frequency = escape(frequency)
        # Errors
        # Improper domain
        name, at, domain = email.partition('@')
        if domain == '':
            start_response('200 OK', [('Content-Type', 'text/html')])
            print 'domain'
            return [str('Invalid address or unpermitted domain.')]

        # Commit to local db
        if company and product and subprod and frequency and email:
            request.create_local_request(email,
                                         frequency,
                                         company, 
                                         product, 
                                         subprod)

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [str(open(os.path.join(settings_dict['application_dir'],
                                      'success_page.html')).read())]
    # TODO Be more specific
    except IndexError:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ['You killed Tuzigoot. I hope you are proud of yourself.']
    except IndexError:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ['You killed Tuzigoot. I hope you are proud of yourself.']
    



def application(environ, start_response):
    # Get path from URL
    path = environ['PATH_INFO'].lstrip('/').rstrip('/')
    for regex, function in map_regex_to_function:
        # Match regex to path
        match = re.search(regex, path)
        if match:
            return function(environ, start_response)
    return error_404(environ, start_response)

class Server_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.server = make_server('', 8080, application)
        print "Server_Thread initialized. Serving."
    def run(self):
        while self.running == True:
           self.server.serve_forever()
