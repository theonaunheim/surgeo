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
######### Styles.
        self.style = Style()
        # Label style
        self.style.configure('TFrame',
                             relief='solid',
                             sticky=W)
        self.style.configure('TLabel',
                             foreground='White',
                             background='#1600FF',
                             font=('Helvetica', 14),
                             sticky=W)
        # Entry style
        self.style.configure('TEntry',
                             foreground='#1600FF',
                             background='White',
                             font=('Helvetica', 14),
                             sticky=W) 
                              
######### Main frame
        self.main_frame = Frame(self.root, padding=(10,0,0,0)).grid(row=0, 
                                                column=0, 
                                                columnspan=10, 
                                                rowspan=10)
        self.widget_dict['main_frame'] = self.main_frame

######### Logo
        logo_path = os.path.join(os.path.expanduser('~'),
                                 '.surgeo',
                                 'logo.gif')
        try: 
            self.logo = PhotoImage(file=logo_path)
            self.logo_label = Label(self.main_frame, 
                                    image=self.logo)
            self.logo_label.grid(row=0, column=0, columnspan=7)
            self.widget_dict['logo_label'] = self.logo_label
        # If no logo, don't create tkinter.
        except _tkinter.TclError:
            pass
######### Console text window
        self.console = Text(self.main_frame,
                            height=20,
                            foreground='White',
                            background='#1600FF',
                            borderwidth=0,
                            highlightbackground='#1600FF',
                            state='disabled',
                            relief='flat').grid(row=0, 
                                                column=7,
                                                columnspan=3)
######### Add labels and text boxes to zip and surname
        self.surname_static = Label(self.main_frame,
                                    text='Surname').grid(row=1,
                                                         column=1,
                                                         columnspan=2,
                                                         sticky=W)
        self.surname_variable = Entry(self.main_frame,
                                      text='').grid(row=2, column=1, sticky=W)
        self.surname_spacer = Label(self.main_frame).grid(row=3, 
                                                          column=1,
                                                          columnspan=2,
                                                          sticky=W)
        self.zip_static = Label(self.main_frame,
                                text='ZIP').grid(row=4,
                                                 column=1, 
                                                 columnspan=2,
                                                 sticky=W)   
        self.zip_variable = Entry(self.main_frame,
                                  text='').grid(row=5, 
                                                column=1, 
                                                columnspan=2, 
                                                sticky=W)
        self.zip_spacer = Label(self.main_frame).grid(row=6, 
                                                      column=1,
                                                      columnspan=2,
                                                      sticky=W)     
        
        self.horiz_space_1 = Label(self.main_frame).grid(row=1, 
                                                         column=2,
                                                         columnspan=1,
                                                         rowspan=5,
                                                         sticky=W)
######### Race percengages      
        self.white_static = Label(self.main_frame, text='White')
        self.white_variable = Label(self.main_frame, text='')
         

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
queue
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
            
        
