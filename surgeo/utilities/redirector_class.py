'''Redirects data as necessary.'''
import multiprocessing
import sys

from xmlrpc.server import SimpleXMLRPCRequestHandler as Handler
from xmlrpc.server import SimpleXMLRPCServer as Server


class Redirector(multiprocessing.Process):
    '''This shunts stdout data to a queue that redirects.

    Properties:
        self.queue: queue where input is put
        self.flag: process goes only when flagged with no materia
        self.daemon: process killed on exit
        self.running: alternative means of killing process
        self.destination: where output is sent
        self.destination_type: type of destination
        self.return_queue = output queue
        self.server = takes rpc calls
        self.namespace = namespace package

    Methods:
        self.direct_to_null(): send output to null
        self.direct_to_queue(): send output to queue
        self.direct_to_stdout(): send output to stdout
        self.direct_to_file(): send output to a file
        self.run(): main run method
        self.push(): add item to queue for redirection

    '''

    def __init__(self,
                 return_queue=None):
        super().__init__()
        self.daemon = True
        self.running = True
        self.destination = sys.stdout
        self.destination_type = 'TextIOWrapper'
        self.return_queue = return_queue
        self.server = Server(('localhost', 8000),
                             requestHandler=Handler,
                             allow_none=True,
                             logRequests=False)

#### Instance related items

    def run(self):
        '''Main run method for process.'''
        # Setup
        self.server.register_function(self.push, 'push')
        self.server.register_function(self.direct_to_null,
                                      'direct_to_null')
        self.server.register_function(self.direct_to_queue,
                                      'direct_to_queue')
        self.server.register_function(self.direct_to_stdout,
                                      'direct_to_stdout')
        self.server.register_function(self.direct_to_file,
                                      'direct_to_file')
        self.server.register_introspection_functions()
        self.server.serve_forever()

    def push(self, item):
        '''Process and threadsafe add to queue for output.'''
        if self.destination_type == 'TextIOWrapper':
            # If stdout, print
            if self.destination.name == '<stdout>':
                print(str(item))
            # If file, write to file
            else:
                with open(self.destination, 'a+') as target:
                    target.write(item)
        # Queue
        elif self.destination_type == 'Queue':
            self.destination.put(item)
        # If unknown, suppress
        else:
            pass

#### Direct to items

    def direct_to_null(self):
        '''Sends output nowhere.'''
        self.destination = None
        self.destination_type = self.destination.__class__.__name__

    def direct_to_queue(self):
        '''Sends output to a queue.'''
        self.destination = self.return_queue
        self.destination_type = self.destination.__class__.__name__

    def direct_to_stdout(self):
        '''Sends output to stdout.'''
        self.destination = sys.stdout
        self.destination_type = self.destination.__class__.__name__

    def direct_to_file(self, path):
        '''Sends output to a file.'''
        self.destination = path
        self.destination_type = self.destination.__class__.__name__

