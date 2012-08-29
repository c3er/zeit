#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

import timelib
import res
from misc import *

UPDATE_TIME = 100

period_button = None

time_content = None
counter = 0
period = None

# Helper functions #############################################################
def create_button(frame, label, command):
    button = ttk.Button(frame, text = label, command = command)
    button.pack(side = 'left')
    return button

def create_time_display(parent, label, period):
    lf = ttk.Labelframe(parent, text = label)
    
    content = tkinter.StringVar()
    tkinter.Label(lf,
        background = 'black',
        foreground = 'yellow',
        font = ('Consolas', 20, 'bold'),
        textvariable = content
    ).pack()
    content.set(str(period))
    
    return lf, content
################################################################################

# Handlers #####################################################################
def update_time(root):
    p = str(period)
    if p != time_content.get():
        time_content.set(p)
        
    root.after(UPDATE_TIME, curry(update_time, root))
    
def start_stop_period():
    pass

def end_day():
    pass

def new_project():
    pass

def open_project():
    pass

def save_project():
    pass

def save_project_as():
    pass

def close_project():
    pass

def new_subproject():
    pass

def continue_subproject():
    pass

def close_subproject():
    pass
################################################################################

# Appearence ###################################################################
def main_menu(root):
    root.option_add('*tearOff', False)
    menu = tkinter.Menu(root)
    root.config(menu = menu)
    
    file_menu = tkinter.Menu(menu)
    menu.add_cascade(label = res.MENU_FILE, menu = file_menu)
    file_menu.add_command(
        label = res.MENU_END,
        command = root.destroy,
        accelerator = 'Alt+F4'
    )
    
    project_menu = tkinter.Menu(menu)
    menu.add_cascade(label = res.MENU_PROJECT, menu = project_menu)
    project_menu.add_command(
        label = res.MENU_NEW_PROJECT,
        command = new_project,
        accelerator = 'Strg+N'
    )
    project_menu.add_command(
        label = res.MENU_OPEN_PROJECT,
        command = open_project,
        accelerator = 'Strg+O'
    )
    project_menu.add_command(
        label = res.MENU_SAVE_PROJECT,
        command = save_project,
        accelerator = 'Strg+S'
    )
    project_menu.add_command(
        label = res.MENU_SAVE_PROJECT_AS,
        command = save_project_as,
        accelerator = 'Strg+Umschalt+S'
    )
    project_menu.add_command(
        label = res.MENU_CLOSE_PROJECT,
        command = close_project,
        accelerator = 'Strg+W'
    )
    
    subproject_menu = tkinter.Menu(menu)
    menu.add_cascade(label = res.MENU_SUBPROJECT, menu = subproject_menu)
    subproject_menu.add_command(
        label = res.MENU_NEW_SUBPROJECT,
        command = new_subproject
    )
    subproject_menu.add_command(
        label = res.MENU_CONTINUE_SUBPROJECT,
        command = continue_subproject
    )
    subproject_menu.add_command(
        label = res.MENU_CLOSE_SUBPROJECT,
        command = close_subproject
    )

def toolbar(parent):
    global period_button
    
    frame = ttk.Frame(parent)
    
    period_button = create_button(frame, res.BUTTON_START, start_stop_period)
    create_button(frame, res.BUTTON_END_DAY, end_day)
    
    return frame

def content(root):
    global time_content
    
    frame = ttk.Frame(root)
    
    main_menu(root)
    toolbar(frame).pack(anchor = 'n', fill = 'x', padx = 2, pady = 2)
    
    td, time_content = create_time_display(frame, 'Zeit', period)
    td.pack(anchor = 'n', padx = 2, pady = 2)
    
    return frame

def bind_events(root):
    root.bind('<Control-n>', lambda event: new_project())
    root.bind('<Control-o>', lambda event: open_project())
    root.bind('<Control-s>', lambda event: save_project())
    root.bind('<Control-S>', lambda event: save_project_as())
    root.bind('<Control-w>', lambda event: close_project())
################################################################################

if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title(res.APP_TITLE)
    period = timelib.Working()  # XXX
    content(root).pack(fill = 'both')
    bind_events(root)
    root.after(UPDATE_TIME, curry(update_time, root))
    root.mainloop()
