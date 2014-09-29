
import io
import os
import queue
import sys
import threading
import time

from tkinter import *

import surgeo

        
class StdoutRedirect(threading.Thread):
    '''This shunts stdout data to a queue that feeds a tkinter.Text window.'''

    def __init__(self, queue):
        super(StdoutRedirect, self).__init__()
        stringio = io.StringIO('')
        self.sys_module = sys.modules['sys']
        setattr(self.sys_module, 'stdout', stringio)
        self.queue = queue
        self.daemon = True
        
    def run(self):
        while True:
            time.sleep(.1)
            try:
                item = self.queue.get_nowait()
                self.queue.put(item)
                self.sys_module =  io.StringIO('')
            except queue.Empty:
                pass
                

class SetupWin(object):
    '''This is the main ttk/tkinter object for the program.'''

    def __init__(self):
######### Root
        self.root = Tk()
        self.root.title('Surgeo')
        self.root.geometry('900x600+0+0')
        self.root.configure(background='#1600FF')
######### Console
        self.console = Text(self.root,
                            height=10,
                            foreground='White',
                            background='#1600FF',
                            font=('Helvetica', 14),
                            borderwidth=0,
                            highlightbackground='#1600FF',
                            state='disabled',
                            relief='flat')
        self.console.pack()
######### Structural elements and create substitute 
        self.input_queue = queue.Queue()
        redirector = StdoutRedirect(self.input_queue)
        redirector.start()
        self.root.after(100, func=self.setup)
        self.root.after(200, func=self.update_all)

        
    def setup(self):
        db_path = os.path.join(os.path.expanduser('~'),
                               '.surgeo',
                               'census.db')
        if not os.path.exists(db_path):
            surgeo.data_setup(verbose=True)
        sys.stdout = sys.__stdout__
        self.root.destroy()
        
    def update_all(self):
        while not self.input_queue.empty():
            result = self.input_queue.get()
            sys.stderr.write(result)
            self.console.config(state='normal')
            self.console.insert('1.0', result)
            self.console.config(state='disabled')
            print('a')
        self.root.after(100, func=self.update_all)



        
                        
