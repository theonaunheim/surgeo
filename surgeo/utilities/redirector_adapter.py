import multiprocessing
import threading
import xmlrpc.client

from surgeo.utilities.redirector_class import Redirector


class RedirectorAdapter(object):
    '''Adapter for redirector.'''
    def __init__(self):
        self.return_queue = multiprocessing.Queue()
        self.redirect_queue = None
        self.mode = 'stdout'
        Redirector(self.return_queue).start()
        self.remote = xmlrpc.client.ServerProxy('http://localhost:8000')

    def write(self, item):
        self.remote.push(item)
        if self.mode == 'queue' and self.redirect_queue is not None:
            threading.Timer(.01, self.queue_transfer).start()

    def direct_to_null(self):
        self.remote.direct_to_null()
        self.mode = 'null'

    def direct_to_queue(self, queue):
        '''Transfer from return queue to argument queue.'''
        self.redirect_queue = queue
        self.remote.direct_to_queue()
        self.mode = 'queue'

    def direct_to_stdout(self):
        self.remote.direct_to_stdout()
        self.mode = 'stdout'

    def direct_to_file(self, path):
        self.remote.direct_to_file(path)
        self.mode = 'file'

    def queue_transfer(self):
        self.redirect_queue.put(self.return_queue.get_nowait())

