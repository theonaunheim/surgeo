import http.server
import os
import socketserver
import webbrowser
import wsgiref


class GuiBase(object):

    def __init__(self):
        self.this_file_path = os.path.abspath(__file__)
        self.gui_directory = os.listdir(self.this_file_path)
        self.html_directory = os.path.join(self.gui_directory,
                                           'html')

    def activate(self):
        webbrowser.open('localhost:8001')


class LocalServer(object):

    def __init__(self):
        pass
 
        
class LocalHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self):
        pass

