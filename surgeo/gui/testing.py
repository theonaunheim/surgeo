import os
import http.server
import socketserver
import threading


class SurgeoHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            print(self.path)
            f = open(parent_dir + os.sep + self.path, 'rb')
            self.send_response(200)
            # Misc headers for different types
            if self.path.endswith('.png'):
                self.send_header('Content-type',
                                 'image/png')
            if self.path.endswith('.css'):
                self.send_header('Content-type',
                                 'text/css')
            if self.path.endswith('.html'):
                self.send_header('Content-type',
                                 'text/html')
                print('ha')
            if self.path.endswith('.js'):
                self.send_header('Content-type',
                                 'text/javascript')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
                
        except IOError:
            self.send_error(404)
     

    def do_POST(self):
        pass

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', 8001),
                                    SurgeoHandler)
    server.serve_forever()
                                


    
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

