'''Main tkinter gui'''

import platform
import threading
import queue

from tkinter import *
from tkinter.ttk import *

class Gui(object):

    def __init__(self, model):
        # Root
        self.root = Tk()
        self.root.title('Surgeo')
        self.root.geometry('900x700+0+0')
        # Structural elements
        self.input_queue = queue.Queue()
        self.widget_list = []
        # Style. Default Darwin and Windows are good. Linux, not so much.
        self.style = ttk.Style()
        if 'Linux' in platform.system():
            try:
                self.style.theme_use('clam')
            except tkinter.TclError:
                pass
        # 


    def csv_process(self):
        pass
        # get
    
    def help_function(self):
        pass
        
    def race_query(self):
        pass
