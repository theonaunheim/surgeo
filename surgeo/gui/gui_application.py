'''Main tkinter gui'''

import os
import platform
import multiprocessing

from tkinter import *
from tkinter.ttk import *
import tkinter

class Gui(object):

    def __init__(self, model):
######### Root
        self.root = Tk()
        self.root.title('Surgeo')
        self.root.geometry('900x700+0+0')
        self.root.configure(background='#1600FF')
######### Structural elements
        self.input_queue = multiprocessing.Queue()
        self.widget_dict = {}
######### Style. Default Darwin and Windows are good. Linux, not so much.
        self.style = Style()
        if 'Linux' in platform.system():
            try:
                self.style.theme_use('clam')
            except tkinter.TclError:
                pass
######### Main frame
        self.main_frame = tkinter.ttk.Frame(self.root).grid(row=0, column=0,
                                                rowspan=10, columnspan=10)
        self.widget_dict['main_frame'] = self.main_frame
######### Logo
        logo_path = os.path.join(os.path.expanduser('~'),
                                 '.surgeo',
                                 'logo.gif') 
        self.logo = PhotoImage(file=logo_path)
        self.logo_label = Label(self.main_frame, image=self.logo, borderwidth=0)
        self.logo_label.grid(row=0, column=0)
        self.widget_dict['logo_label'] = self.logo_label
######### Frame for race data
        self.race_frame = tkinter.ttk.Frame(self.main_frame).grid(row=0, 
                                                                  column=0,
                                                                  rowspan=10, 
                                                                  columnspan=10)
        self.widget_dict['race_frame'] = self.race_frame
######### Add labels and text boxes to race_frame
        self.white_static = Label(self.race_frame, text='White')
        self.white_variable = Label(self.race_frame, text='')
         
        
        # Finally root after all
        self.root.after(100, func=self.update_all)
        
    def csv_process(self):
        pass
        # send strings instead of object references
    
    def help_function(self):
        pass
        
    def race_query(self):
        pass
        
    def update_all(self):
        while not self.input_queue.empty():
            result = self.input_queue.get()
            widget_text = result[0]
            command_text = result[1]
            widget_reference = self.widget_dict[widget_text]
            widget_type = type(widget_reference)
            if widget_type == tkinter.Label:
                widget_reference.config(text=command_text)
        self.root.after(100, func=self.update_all)
'''
Picture frame
=====
image

Console frame
======
prog bar
console

Master frame
======
picture, console and input frames

Input frame
======
#raise invalid zip
text input name
label name
text input zip
label zip
button compute zip/name
button csv process
button load (grey out everything if not db)
custton
text display hispanic
label hispanic
text display white
label white
text display black
label black
text display asian
label asian
text display indian
label indian
text display multiracial
label multi tracial



'''
            
        
