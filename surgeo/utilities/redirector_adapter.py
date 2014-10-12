import multiprocessing
import xmlrpc.client

from surgeo.utilities.redirector_class import Redirector


class RedirectorInterface(object):

    def __init__(self):
        self.return_queue = multiprocessing.Queue()
        Redirector(self.return_queue).start()
        self.remote = xmlrpc.client.ServerProxy('http://localhost:8000')
        
    def output_target(self, target):
        

interface = RedirectorInterface()

