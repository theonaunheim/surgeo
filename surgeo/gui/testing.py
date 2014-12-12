
import threading
import cgi
import wsgiref.simple_server


def app(environment, start_response):
    '''Index is mounted at '/'.'''
    start_response('200 OK', [('Content-Type', 'text/html')])
    # fp = file pinter
    post_data = cgi.FieldStorage(fp=environment['wsgi.input'],
                                 environ=environment.copy(),
                                 keep_blank_values=True)
    print(post_data)
    #return ['string']

class Server_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.server = wsgiref.simple_server.make_server('localhost',
                                                        8001,
                                                        app)
        print("Server_Thread initialized. Serving.")
    def run(self):
        while self.running == True:
           self.server.serve_forever()
           
if __name__ == '__main__':
    server = Server_Thread()
    server.start()
    
    
    
'''
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the 
remote resource at http://localhost:8001/. 
This can be fixed by moving the resource to the same domain or enabling CORS.
('CONTENT_TYPE', 'text/plain'), 
('SHELL', '/bin/bash'), 
('PATH_INFO', '/'), 
('REQUEST_METHOD', 'GET'), 
('USER', 'theo'), 
('REMOTE_ADDR', '127.0.0.1'), 
('SERVER_PORT', '8001'), 
('QUERY_STRING', ''), 
('LOGNAME', 'theo'), 
('HOME', '/home/theo'), 
('CONTENT_LENGTH', ''), 
('PWD', '/home/theo'),
('_', '/usr/bin/python3'),
('LANG', 'en_US.UTF-8'), 
('HTTP_ACCEPT_LANGUAGE', 'en-US,en;q=0.5'),
('PATH', '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games'), 
('HTTP_USER_AGENT', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'), 
('HTTP_ACCEPT', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
('REMOTE_HOST', ''),
('HTTP_HOST', 'localhost:8001'), 
'''

