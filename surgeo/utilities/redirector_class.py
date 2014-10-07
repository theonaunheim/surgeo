import io
import multiprocessing
import os
import queue
import sys


class Redirector(multiprocessing.Process):
    '''This shunts stdout data to a queue that redirects.'''

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = True
        self.daemon = True

    def add(self, item):
        self.queue.put(item)
        sys.stdout.write(''.join([item, '\n']))

    def direct_to_file(self):
        fake_stdout = io.StringIO('')
        setattr(sys.modules['sys'], 'stdout', fake_stdout)

    def direct_to_null(self):
        null_file = open(os.devnull, 'w')
        setattr(sys.modules['sys'], 'stdout', null_file)

    def direct_to_stdout(self):
        true_stdout = sys.__stdout__
        setattr(sys.modules['sys'], 'stdout', true_stdout)

    def kill(self):
        self.running = False

    def quiet(self):
        self.direct_to_null()

    def run(self):
        while self.running is True:
            try:
                popped_item = self.queue.get(True, .1)
                sys.stdout.write(popped_item)
            except queue.Empty:
                pass
        self.terminate()

    def verbose(self):
        self.direct_to_stdout()

