#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.filedialog
import tkinter.ttk as ttk

import controller
import timelib
import res
import res.menu
from misc import *

MIN_SIZE_X = 250
MIN_SIZE_Y = 100

con = None

main_menu = None

menu_project_save = None
menu_project_save_as = None
menu_project_close = None
menu_subproject_close = None
menu_day_stop = None

period_button = None

class Menu:
    def __init__(self, tkparent):
        self.children = []
        
        if not isinstance(self, SubMenu):
            tkparent.option_add('*tearOff', False)
            
        self.tkmenu = tkinter.Menu(tkparent)
        
        if not isinstance(self, SubMenu):
            tkparent.config(menu = self.tkmenu)
            
        self.tkparent = tkparent
        self.label = None
    
    def add_submenu(self, label):
        submenu = SubMenu(label, self, self.tkmenu)
        self.tkmenu.add_cascade(label = label, menu = submenu.tkmenu)
        self.children.append(submenu)
        return submenu
    
    def add_item(self, label, command, *args, **kw):
        item = MenuItem(self, label, command)
        self.tkmenu.add_command(*args, label = label, command = command, **kw)
        self.children.append(item)
        return item
    
    def add_seperator(self):
        self.tkmenu.add_separator()
    
class SubMenu(Menu):
    def __init__(self, label, parent, *args, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.label = label
        
    def disable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'disabled')
    
    def enable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'enabled')
    
class MenuItem:
    def __init__(self, parent, label, command):
        self.parent = parent
        self.label = label
        self.command = command
        
    def disable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'disabled')
    
    def enable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'enabled')

# Helper functions #############################################################
def _widget_config(tk_func, menu_func):
    if isinstance(widget, (tkinter.Button, ttk.Button)):
        tk_func()
    elif isinstance(widget, (SubMenu, MenuItem)):
        menu_func()
    else:
        raise TypeError()

def disable(widget):
    _widget_config(curry(widget.config, state = 'disabled'), widget.disable)

def enable(widget):
    _widget_config(curry(widget.config, state = 'enabled'), widget.enable)

def create_button(frame, label, command):
    button = ttk.Button(frame, text = label, command = command)
    button.pack(side = 'left')
    return button
################################################################################

# Handlers #####################################################################
def adjust_state(con):
    pass
    
def start_pause_period():
    if not con.started:
        con.start()
    elif not con.paused:
        con.pause()
    else:
        con.resume()

def end_day():
    pass

def new_project():
    pass

def open_project():
    path = tkinter.filedialog.askopenfilename(
        filetypes = [(res.PROJECT_FILE_STR, res.PROJECT_FILE_EXT)]
    )
    if path:
        con.open_project(path)

def save_project():
    try:
        con.save_project()
    except controller.UnknownPathException:
        save_project_as()

def save_project_as():
    path = tkinter.filedialog.asksaveasfilename(
        filetypes = [(res.PROJECT_FILE_STR, res.PROJECT_FILE_EXT)]
    )
    if path:
        if not path.endswith(res.PROJECT_FILE_EXT):
            path += res.PROJECT_FILE_EXT
        con.save_project(path)

def close_project():
    pass

def new_subproject():
    pass

def continue_subproject():
    pass

def close_subproject():
    pass

def start_pause_day():
    pass

def stop_day():
    pass

def attach_day_to_subproject():
    pass
################################################################################

# Appearence ###################################################################
def create_main_menu(root):
    global menu_project_save
    global menu_project_save_as
    global menu_project_close
    global menu_subproject_close
    global menu_day_stop
    
    menu = Menu(root)
    
    # File menu
    file_menu = menu.add_submenu(res.menu.FILE)
    file_menu.add_item(res.STOP, root.destroy, accelerator = 'Alt+F4')
    
    # Project menu
    project_menu = menu.add_submenu(res.menu.PROJECT)
    project_menu.add_item(
        res.menu.NEW_PROJECT, new_project, accelerator = 'Strg+N'
    )
    project_menu.add_item(
        res.menu.OPEN_PROJECT, open_project, accelerator = 'Strg+O'
    )
    menu_project_save = project_menu.add_item(
        res.menu.SAVE_PROJECT, save_project, accelerator = 'Strg+S'
    )
    menu_project_save_as = project_menu.add_item(
        res.menu.SAVE_PROJECT_AS,
        save_project_as,
        accelerator = 'Strg+Umschalt+S'
    )
    menu_project_close = project_menu.add_item(
        res.menu.CLOSE_PROJECT, close_project, accelerator = 'Strg+W'
    )
    
    # Subproject menu
    subproject_menu = menu.add_submenu(res.menu.SUBPROJECT)
    subproject_menu.add_item(res.menu.NEW_SUBPROJECT, new_subproject)
    subproject_menu.add_item(res.menu.CONTINUE_SUBPROJECT, continue_subproject)
    menu_subproject_close = subproject_menu.add_item(
        res.menu.CLOSE_SUBPROJECT, close_subproject
    )
    
    # Day menu
    day_menu = menu.add_submenu(res.DAY)
    day_menu.add_item(res.menu.START_PAUSE_DAY, start_pause_day)
    menu_day_stop = day_menu.add_item(res.STOP, stop_day)
    day_menu.add_seperator()
    day_menu.add_item(
        res.menu.ATTACH_DAY_TO_SUBPROJECT, attach_day_to_subproject
    )
    
    return menu

def toolbar(parent):
    global period_button
    
    frame = ttk.Frame(parent)
    
    period_button = create_button(frame, res.BUTTON_START, start_pause_period)
    create_button(frame, res.BUTTON_END_DAY, end_day)
    
    return frame

def bind_events(root):
    root.bind('<Control-n>', lambda event: new_project())
    root.bind('<Control-o>', lambda event: open_project())
    root.bind('<Control-s>', lambda event: save_project())
    root.bind('<Control-S>', lambda event: save_project_as())
    root.bind('<Control-w>', lambda event: close_project())
################################################################################

if __name__ == '__main__':
    # Initializing
    root = tkinter.Tk()
    root.minsize(MIN_SIZE_X, MIN_SIZE_Y)
    root.wm_title(res.APP_TITLE)
    main_menu = create_main_menu(root)
    toolbar(root).pack(anchor = 'n', fill = 'x')
    bind_events(root)
    con = controller.Controller(root, adjust_state)
    
    root.mainloop()
