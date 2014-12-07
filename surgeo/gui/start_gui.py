from surgeo.gui.gui_classes import GuiBase


def start_gui(self):
    gui = GuiBase()
    gui.activate()

'''
def application(environ, start_response):
if environ['REQUEST_METHOD'] == 'GET':
response_headers = [
('Content-Type', 'text/html'),
('Content-Length', str(len(body))),
]
start_response('200 OK', response_headers)
yield body
else:
response_headers = [('Content-Type', 'text/plain')]
start_response('200 OK', response_headers)
for bit in ['Each ', 'bit ', 'should ', 'be a ', 'chunk.']:
yield bit
time.sleep(1) 
'''

