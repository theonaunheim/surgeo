import io
import os
import queue
import sys

class Redirector():
    '''This shunts stdout data to a queue that redirects.'''

    def __init__(self, queue):
        super().__init__()
        self.queue = queue.Queue()

    def add(self, item):
        self.queue.put(item)
        sys.stdout.write(''.join([item, '\n'])
        
    def direct_to_file(self):
        fake_stdout = io.StringIO('')
        setattr(sys.modules['sys'], 'stdout', fake_stdout)
                             
    def direct_to_null(self):
        null_file = open(os.devnull, 'w')
        setattr(sys.modules['sys'], 'stdout', null_file)
        
    def direct_to_stdout(self):
        true_stdout = sys.__stdout__
        setattr(sys.modules['sys'], 'stdout', true_stdout)
        
    def quiet(self):
        self.direct_to_null()
    
    def verbose(self):
        self.direct_to_stdout()

