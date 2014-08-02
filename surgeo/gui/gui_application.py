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
                             width=16,
                             fieldbackgroundcolor='#1600FF',
                             insertbackground='White',
                             insertwidth=1,
                             insertcolor='White',
                             sticky=W)
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
            self.logo_label.grid(row=0, column=0, columnspan=7, sticky=W)
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
        self.horiz_space_1 = Label(self.main_frame, width=5).grid(row=0, 
                                                         column=0,
                                                         columnspan=1,
                                                         rowspan=5,
                                                         sticky=W)
        self.prompt_1 = Label(self.main_frame,
                              text='>>>').grid(row=2,
                                               column=0,
                                               columnspan=1,
                                               sticky=E)
        self.prompt_2 = Label(self.main_frame,
                              text='>>>').grid(row=5,
                                               column=0,
                                               columnspan=1,
                                               sticky=E)
        self.surname_static = Label(self.main_frame,
                                    width=15,
                                    text='Surname').grid(row=1,
                                                         column=1,
                                                         columnspan=1,
                                                         sticky=W)
        self.surname_variable = Entry(self.main_frame,
                                      font=('Helvetica', 14),
                                      width=20,
                                      style='Alt.TEntry',
                                      validate='key',
                                      validatecommand=self.sur_val_com,
                                      text='').grid(row=2, 
                                                    column=1,
                                                    sticky=W)
        self.surname_spacer = Label(self.main_frame).grid(row=3, 
                                                          column=1,
                                                          columnspan=1,
                                                          sticky=W)
        self.zip_static = Label(self.main_frame,
                                text='ZIP').grid(row=4,
                                                 column=1, 
                                                 columnspan=1,
                                                 sticky=W)   
        self.zip_variable = Entry(self.main_frame,
                                  font=('Helvetica', 14),
                                  width=5,
                                  style='Alt.TEntry',
                                  validate='key',
                                  validatecommand=self.zip_val_com,
                                  text='').grid(row=5, 
                                                column=1, 
                                                columnspan=1, 
                                                sticky=W)
        self.zip_spacer = Label(self.main_frame).grid(row=6, 
                                                      column=1,
                                                      columnspan=2,
                                                      sticky=W)                       
                             
                             

######### Race percengages      
        self.hispanic_static = Label(self.main_frame,
                                     width=10,
                                     text='Hispanic').grid(row=1,
                                                           column=2,
                                                           sticky=W)
        self.hispanic_variable = Label(self.main_frame,
                                       text='-').grid(row=1, 
                                                     column=3,
                                                     sticky=W)
        self.white_static = Label(self.main_frame,
                                  width=10,
                                  text='White').grid(row=2,
                                                     column=2,
                                                     sticky=W)
        self.white_variable = Label(self.main_frame,
                                    text='-').grid(row=2, 
                                                  column=3,
                                                  sticky=W)
        self.black_static = Label(self.main_frame,
                                  width=10,
                                  text='Black').grid(row=3,
                                                     column=2,
                                                     sticky=W)
        self.black_variable = Label(self.main_frame,
                                    text='-').grid(row=3, 
                                                  column=3,
                                                  sticky=W)
        self.api_static = Label(self.main_frame,
                                width=10,
                                text='Asian').grid(row=4,
                                                   column=2,
                                                   sticky=W)
        self.api_variable = Label(self.main_frame,
                                  text='-').grid(row=4, 
                                                column=3,
                                                sticky=W)
        self.native_am_static = Label(self.main_frame,
                                      width=10,
                                      text='Native Am').grid(row=5,
                                                                   column=2,
                                                                   sticky=W)
        self.native_am_variable = Label(self.main_frame,
                                        text='-').grid(row=5, 
                                                      column=3,
                                                      sticky=W)
        self.multiracial_static = Label(self.main_frame,
                                        width=10,
                                        text='Multiracial').grid(row=6,
                                                                 column=2,
                                                                 sticky=W)
        self.multiracial_variable = Label(self.main_frame,
                                        text='-').grid(row=6, 
                                                      column=3,
                                                      sticky=W)

        # Finally root after all
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
            widget_text = result[0]
            command_text = result[1]
            widget_reference = self.widget_dict[widget_text]
            widget_type = type(widget_reference)
            if widget_type == tkinter.Label:
                widget_reference.config(text=command_text)
        self.root.after(100, func=self.update_all)

