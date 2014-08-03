'''Main tkinter gui'''

import os
import platform
import multiprocessing
import sys
import tkinter

from tkinter import *
from tkinter.ttk import *

import surgeo

class StdoutRedirect(multiprocessing.Process):

    def __init__(self, queue):
        super(StdoutRedirect, self).__init__()
        self.queue = queue
        self.daemon = True
       # sys.stdout = open('stdout_file', 'w')
        
    def run(self):
        while True:
            import time; time.sleep(1)
            self.queue.put(['white_variable','aaa'])
        '''
            if sys.stdout:
                command_tuple = ('console', 'ab')
                                # str(sys.stdout.read()))
                self.queue.put(command_tuple)
        '''
        
class Gui(object):

    def __init__(self, model):
######### Root
        self.root = Tk()
        self.root.title('Surgeo')
        self.root.geometry('900x600+0+0')
        self.root.configure(background='#1600FF')
######### Structural elements
        self.input_queue = multiprocessing.Queue()
        StdoutRedirect(self.input_queue).start()
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
                             width=16,
                             fieldbackgroundcolor='#1600FF',
                             insertbackground='White',
                             insertwidth=1,
                             insertcolor='White',
                             sticky=W)
        # Button style
        self.style.configure('TButton',
                             foreground='White',
                             background='#1600FF',
                             focuscolor='White',
                             relief='flat',
                             width=16,
                             active='#1600FF',
                             font=('Helvetica', 14),
                             sticky=W)
        self.style.map('TButton',background=
                       [('selected', '#1600FF'), ('active', '#1600FF')])
######### Kludge
        self.style.element_create('plain.field', 'from', 'default')
        self.style.layout('Alt.TEntry',
                          [('Entry.plain.field', {'children': [(
                            'Entry.background', {'children': [(
                            'Entry.padding', {'children': [(
                            'Entry.textarea', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})], 'sticky': 'nswe'})],
                            'border':'2', 'sticky': 'nswe'})])
        self.style.configure('Alt.TEntry',
                             background='white', 
                             foreground='white',
                             insertbackground='white',
                             fieldbackground='#1600FF',
                             borderwidth=0)
######### Main frame
        self.main_frame = Frame(self.root, padding=(10,0,0,0))
        self.main_frame.grid(row=0, column=0, columnspan=10, rowspan=10)
######### Logo
        logo_path = os.path.join(os.path.expanduser('~'),
                                 '.surgeo',
                                 'logo.gif')
        try: 
            self.logo = PhotoImage(file=logo_path)
            self.logo_label = Label(self.main_frame, image=self.logo)
            self.logo_label.grid(row=0, column=0, columnspan=7, sticky=W)
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
                            relief='flat')
        self.console.grid(row=0, column=7, columnspan=3)
######### Entry validators
        # valid percent substitutions (from the Tk entry man page)
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        self.zip_val_com = (self.root.register(self.zip_val_func),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.sur_val_com = (self.root.register(self.sur_val_func),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')                         
######### Add labels and text boxes to zip and surname
        self.horiz_space_1 = Label(self.main_frame, width=5)
        self.horiz_space_1.grid(row=0, 
                                column=0, 
                                columnspan=1, 
                                rowspan=5, 
                                sticky=W)
        self.prompt_1 = Label(self.main_frame, text='>>>')
        self.prompt_1.grid(row=2, column=0, columnspan=1, sticky=E)
        self.prompt_2 = Label(self.main_frame, text='>>>')
        self.prompt_2.grid(row=5, column=0, columnspan=1, sticky=E)
        self.surname_static = Label(self.main_frame, width=15, text='Surname')
        self.surname_static.grid(row=1, column=1, columnspan=1, sticky=W)
        self.surname_variable = Entry(self.main_frame,
                                      font=('Helvetica', 14),
                                      width=20,
                                      style='Alt.TEntry',
                                      validate='key',
                                      validatecommand=self.sur_val_com,
                                      text='')
        self.surname_variable.grid(row=2, column=1, sticky=W)
        self.surname_spacer = Label(self.main_frame)
        self.surname_spacer.grid(row=3, column=1, columnspan=1, sticky=W)
        self.zip_static = Label(self.main_frame, text='ZIP') 
        self.zip_static.grid(row=4, column=1, columnspan=1, sticky=W) 
        self.zip_variable = Entry(self.main_frame,
                                  font=('Helvetica', 14),
                                  width=5,
                                  style='Alt.TEntry',
                                  validate='key',
                                  validatecommand=self.zip_val_com,
                                  text='')
        self.zip_variable.grid(row=5, column=1,  columnspan=1, sticky=W)
        self.zip_spacer = Label(self.main_frame)
        self.zip_spacer.grid(row=6, column=1, columnspan=2, sticky=W)                                                                     
######### Race percengages      
        self.hispanic_static = Label(self.main_frame, width=10, text='Hispanic')
        self.hispanic_static.grid(row=1, column=2, sticky=W)
        self.hispanic_variable = Label(self.main_frame, text='-')
        self.hispanic_variable.grid(row=1, column=3, sticky=W)
        self.white_static = Label(self.main_frame, width=10, text='White')
        self.white_static.grid(row=2, column=2, sticky=W)
        self.white_variable = Label(self.main_frame, text='-')
        self.white_variable.grid(row=2, column=3, sticky=W)
        self.black_static = Label(self.main_frame, width=10, text='Black')
        self.black_static.grid(row=3, column=2, sticky=W)
        self.black_variable = Label(self.main_frame, text='-')
        self.black_variable.grid(row=3, column=3, sticky=W)
        self.api_static = Label(self.main_frame, width=10, text='Asian')
        self.api_static.grid(row=4, column=2, sticky=W)
        self.api_variable = Label(self.main_frame, text='-')
        self.api_variable.grid(row=4, column=3, sticky=W)
        self.native_am_static = Label(self.main_frame,
                                      width=10,
                                      text='Native Am')
        self.native_am_static.grid(row=5, column=2, sticky=W)
        self.native_am_variable = Label(self.main_frame, text='-')
        self.native_am_variable.grid(row=5, column=3, sticky=W)
        self.multiracial_static = Label(self.main_frame,
                                        width=10,
                                        text='Multiracial')
        self.multiracial_static.grid(row=6, column=2, sticky=W)
        self.multiracial_variable = Label(self.main_frame, text='-')
        self.multiracial_variable.grid(row=6, column=3, sticky=W)
######### Buttons
        self.enter_button = Button(self.main_frame, text='<Enter>')
        self.enter_button.grid(row=2, column=7)                  
        self.csv_process_button = Button(self.main_frame, text='<Input CSV>')
        self.csv_process_button.grid(row=4, column=7)
        self.quit_button = Button(self.main_frame, text='<Quit>')
        self.quit_button.grid(row=6, column=7)
######### Add items to widget_dict
        self.widget_dict = {}
        self.widget_dict['console'] = self.console
        self.widget_dict['hispanic_variable'] = self.hispanic_variable
        self.widget_dict['white_variable'] = self.white_variable 
        self.widget_dict['black_variable'] = self.black_variable
        self.widget_dict['api_variable'] = self.api_variable
        self.widget_dict['native_am_variable'] = self.native_am_variable
        self.widget_dict['multiracial_variable'] = self.multiracial_variable
        self.widget_dict['surname_variable'] = self.surname_variable
        self.widget_dict['zip_variable'] = self.zip_variable
######### Finally root after all
        self.root.after(100, func=self.update_all)
        
    def csv_process(self):
        pass
        # send strings instead of object references
    
    def help_function(self):
        pass
        
    def race_query(self):
        pass

    def zip_val_func(self, d, i, P, s, S, v, V, W):
        '''Only numbers, and no more than 5 numbers.'''
        # valid percent substitutions (from the Tk entry man page)
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        #
        # If not an integer, disallow
        try:
            int(S)
        except ValueError:
            return False
        # If first number is a zero, disallow.
        if P == '0':
            return False
        # If more than 5 digits and insertion, disallow.
        if d == '1':
            if len(s) > 4:
                return False
            else:
                return True
        else:
            return True
        
    def sur_val_func(self, d, i, P, s, S, v, V, W):
        '''Do not allow more than 20 characters.'''
        # valid percent substitutions (from the Tk entry man page)
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        #
        # If action is insertion
        if d == '1':
            # If length is greater than 20, disallow
            if len(s) > 19:
                return False
            else:
                return True
        # If deletion, allow
        else:
            return True
            
    def update_all(self):
        while not self.input_queue.empty():
            result = self.input_queue.get()
            print(type(self.csv_process_button))
            widget_text = result[0]
            command_text = result[1]
            widget_reference = self.widget_dict[widget_text]
            widget_type = type(widget_reference)
            if widget_type == tkinter.Label:
                widget_reference.config(text=command_text)
            if widget_type == tkinter.Text:
                widget_reference.config(text=command_text)
        self.root.after(100, func=self.update_all)


