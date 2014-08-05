'''Main tkinter gui'''

import io
import os
import platform
import queue
import sys
import threading
import time
import tkinter

from tkinter import *
from tkinter.ttk import *

import surgeo


class StdoutRedirect(threading.Thread):
    '''This shunts stdout data to a queue that feeds a tkinter.Text window.'''

    def __init__(self, queue):
        super(StdoutRedirect, self).__init__()
        sys.stdout = io.StringIO('')
        sys_module = sys.modules['sys']
        setattr(sys_module, 'stdout', sys.stdout)
        self.queue = queue
        self.daemon = True
        
    def run(self):
        while True:
            time.sleep(.1)
            if len(sys.stdout.getvalue()) > 0:
                command_list = ['console',
                                ''.join([sys.stdout.getvalue(), '\n'])]
                self.queue.put(command_list)
                sys.stdout = io.StringIO('')
        
                
class SpinoffCSV(threading.Thread):
    '''This thread spins off the construction of the csv.'''

    def __init__(self, master_app, infile_path, outfile_path):
        super().__init__()
        self.daemon = True
                
    def run(self):
        master_app.model.process_csv(infile_path,
                                     outfile_path,
                                     verbose=True)
   
   
class Gui(object):
    '''This is the main ttk/tkinter object for the program.'''

    def __init__(self):
######### Root
        self.root = Tk()
        self.root.title('Surgeo')
        self.root.geometry('900x600+0+0')
        self.root.configure(background='#1600FF')
######### Structural elements and create substitute 
        self.input_queue = queue.Queue()
        self.external_sig_queue = queue.Queue()
        redirector = StdoutRedirect(self.input_queue)
        redirector.start()
        # Placeholder for model established at end of setup
        self.model = None
######### Styles.
        self.style = Style()
        # Label style
        self.style.configure('TFrame',
                             relief='flat',
                             background='#1600FF',
                             sticky=W)
        # Label style
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
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=0, column=0, columnspan=10, rowspan=10)
######### Logo
        logo_path = os.path.join(os.path.expanduser('~'),
                                 '.surgeo',
                                 'logo.gif')
        try: 
            self.logo = PhotoImage(file=logo_path)
            self.logo_label = Label(self.main_frame, image=self.logo)
            self.logo_label.grid(row=0, column=0, columnspan=7, sticky=W)
        # If no logo, don't create.
        except tkinter.TclError:
            pass
######### Console text window
        self.console = Text(self.main_frame,
                            height=10,
                            foreground='White',
                            background='#1600FF',
                            font=('Helvetica', 14),
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
        self.surname_text_var = StringVar()
        self.surname_static = Label(self.main_frame, width=15, text='Surname')
        self.surname_static.grid(row=1, column=1, columnspan=1, sticky=W)
        self.surname_variable = Entry(self.main_frame,
                                      font=('Helvetica', 14),
                                      width=20,
                                      style='Alt.TEntry',
                                      validate='key',
                                      validatecommand=self.sur_val_com,
                                      textvariable=self.surname_text_var,
                                      text='')
        self.surname_variable.grid(row=2, column=1, sticky=W)
        self.surname_spacer = Label(self.main_frame)
        self.surname_spacer.grid(row=3, column=1, columnspan=1, sticky=W)
        self.zip_text_var = StringVar()
        self.zip_static = Label(self.main_frame, text='ZIP') 
        self.zip_static.grid(row=4, column=1, columnspan=1, sticky=W) 
        self.zip_variable = Entry(self.main_frame,
                                  font=('Helvetica', 14),
                                  width=5,
                                  style='Alt.TEntry',
                                  validate='key',
                                  validatecommand=self.zip_val_com,
                                  textvariable=self.zip_text_var,
                                  text='')
        self.zip_variable.grid(row=5, column=1,  columnspan=1, sticky=W)
        self.zip_spacer = Label(self.main_frame)
        self.zip_spacer.grid(row=6, column=1, columnspan=2, sticky=W)                                                                     
######### Race percengages      
        self.hispanic_static = Label(self.main_frame, width=10, text='Hispanic')
        self.hispanic_static.grid(row=1, column=2, sticky=W)
        self.hispanic_variable = Label(self.main_frame, text='-')
        self.hispanic_variable.grid(row=1, column=3, sticky=W, columnspan=2)
        self.white_static = Label(self.main_frame, width=10, text='White')
        self.white_static.grid(row=2, column=2, sticky=W)
        self.white_variable = Label(self.main_frame, text='-')
        self.white_variable.grid(row=2, column=3, sticky=W, columnspan=2)
        self.black_static = Label(self.main_frame, width=10, text='Black')
        self.black_static.grid(row=3, column=2, sticky=W)
        self.black_variable = Label(self.main_frame, text='-')
        self.black_variable.grid(row=3, column=3, sticky=W, columnspan=2)
        self.api_static = Label(self.main_frame, width=10, text='Asian')
        self.api_static.grid(row=4, column=2, sticky=W)
        self.api_variable = Label(self.main_frame, text='-')
        self.api_variable.grid(row=4, column=3, sticky=W, columnspan=2)
        self.native_am_static = Label(self.main_frame,
                                      width=10,
                                      text='Native Am')
        self.native_am_static.grid(row=5, column=2, sticky=W)
        self.native_am_variable = Label(self.main_frame, text='-')
        self.native_am_variable.grid(row=5, column=3, sticky=W, columnspan=2)
        self.multiracial_static = Label(self.main_frame,
                                        width=10,
                                        text='Multiracial')
        self.multiracial_static.grid(row=6, column=2, sticky=W)
        self.multiracial_variable = Label(self.main_frame, text='-')
        self.multiracial_variable.grid(row=6, column=3, sticky=W, columnspan=2)
######### Buttons
        self.enter_button = Button(self.main_frame, text='<Enter>')
        self.enter_button.bind('<Button-1>', self.race_query)
        self.enter_button.bind('<Return>', self.race_query)
        self.enter_button.grid(row=2, column=7)                  
        self.csv_process_button = Button(self.main_frame, text='<Input CSV>')
        self.csv_process_button.grid(row=4, column=7)
        self.quit_button = Button(self.main_frame, text='<Quit>')
        self.quit_button.bind('<Button-1>', sys.exit)
        self.quit_button.bind('<Return>', sys.exit)        
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
        self.model = surgeo.SurgeoModel()
######### Finally root after all
        self.root.after(100, func=self.update_all)             
        
    def csv_process(self):
        '''Process csv file.'''
        infile = filedialog.askopenfilename()
        outfile = filedialog.asksaveasfilename()
        # Pass reference to app, infile path and outfile path.
        csv_spinoff_thread = SpinoffCSV(self,
                                        infile_path,
                                        outfile_path)
        csv_spinoff_thread.start()
        csv_spinoff_thread.join()
        
    def race_query(self):
        surgeo_result = self.model.race_data(self.zip_text_var,
                                             self.surname_text_var)
        command_list = []
        command_list.append(['hispanic_variable', 
                             surgeo_result.hispanic])
        command_list.append(['white_variable', 
                             surgeo_result.white])
        command_list.append(['black_variable', 
                             surgeo_result.black])
        command_list.append(['api_variable',
                             surgeo_result.asian_or_pi])
        command_list.append(['native_am_variable', 
                              surgeo_result.american_indian])
        command_list.append(['multiracial_variable',
                             surgeo_result.multiracial])
        for item in command_list:
            self.input_queue.put(item)
                             
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
            widget_text = result[0]
            command_text = result[1]
            # If not command, done on a widget basis
            widget_reference = self.widget_dict[widget_text]
            widget_type = type(widget_reference)
            if widget_type == tkinter.ttk.Label:
                widget_reference.config(text=command_text)               
            if widget_type == tkinter.Text:
                widget_reference.config(state='normal')
                widget_reference.insert('1.0', ''.join([command_text]))
                widget_reference.config(state='disabled')       
        self.root.after(100, func=self.update_all)


