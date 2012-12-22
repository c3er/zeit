#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.filedialog
import tkinter.ttk as ttk

import gui
import controller
import timelib
import res
import res.menu
from misc import *

MIN_SIZE_X = 250
MIN_SIZE_Y = 100

PERIOD_BUTTON_WIDTH = 15

con = None

main_menu = None

# Widgets of interest ##########################################################
menu_file_new = None
menu_file_close = None
menu_subproject_continue = None
menu_subproject_close = None
menu_day_stop = None
menu_day_assign_subproject = None

period_button = None
day_stop_button = None
################################################################################

# Handlers #####################################################################
def adjust_state(con):
    if con.isnew:
        gui.disable(menu_file_new)
        gui.disable(menu_file_close)
        gui.disable(menu_subproject_continue)
        gui.disable(menu_subproject_close)
        gui.disable(menu_day_stop)
        gui.disable(menu_day_assign_subproject)
        gui.disable(day_stop_button)
    elif con.started:
        gui.disable(menu_subproject_continue)
        gui.disable(menu_subproject_close)
        gui.disable(menu_day_assign_subproject)
        gui.enable(menu_file_new)
        gui.enable(menu_file_close)
        gui.enable(menu_day_stop)
        gui.enable(day_stop_button)
    
    if con.paused or not con.started:
        period_button.config(text = res.BUTTON_START)
    else:
        period_button.config(text = res.BUTTON_PAUSE)
    
def start_pause_period():
    if not con.started:
        con.start()
    elif not con.paused:
        con.pause()
    else:
        con.resume()

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
    con.stop()

def attach_day_to_subproject():
    pass
################################################################################

# Appearence ###################################################################
def create_main_menu(root):
    global menu_file_new
    global menu_file_close
    global menu_subproject_continue
    global menu_subproject_close
    global menu_day_stop
    global menu_day_assign_subproject
    
    menu = gui.Menu(root)
    
    # File menu
    file_menu = menu.add_submenu(res.menu.FILE)
    menu_file_new = file_menu.add_item(
        res.menu.NEW_PROJECT, new_project, accelerator = 'Strg+N'
    )
    file_menu.add_item(
        res.menu.OPEN_PROJECT, open_project, accelerator = 'Strg+O'
    )
    file_menu.add_item(
        res.menu.SAVE_PROJECT, save_project, accelerator = 'Strg+S'
    )
    file_menu.add_item(
        res.menu.SAVE_PROJECT_AS,
        save_project_as,
        accelerator = 'Strg+Umschalt+S'
    )
    menu_file_close = file_menu.add_item(
        res.menu.CLOSE_PROJECT, close_project, accelerator = 'Strg+W'
    )
    file_menu.add_seperator()
    file_menu.add_item(res.STOP, root.destroy, accelerator = 'Alt+F4')
    
    # Subproject menu
    subproject_menu = menu.add_submenu(res.menu.SUBPROJECT)
    subproject_menu.add_item(res.menu.NEW_SUBPROJECT, new_subproject)
    menu_subproject_continue = subproject_menu.add_item(
        res.menu.CONTINUE_SUBPROJECT, continue_subproject
    )
    menu_subproject_close = subproject_menu.add_item(
        res.menu.CLOSE_SUBPROJECT, close_subproject
    )
    
    # Day menu
    day_menu = menu.add_submenu(res.DAY)
    day_menu.add_item(res.menu.START_PAUSE_DAY, start_pause_day)
    menu_day_stop = day_menu.add_item(res.STOP, stop_day)
    day_menu.add_seperator()
    menu_day_assign_subproject = day_menu.add_item(
        res.menu.ATTACH_DAY_TO_SUBPROJECT, attach_day_to_subproject
    )
    
    return menu

def toolbar(parent):
    global period_button
    global day_stop_button
    
    frame = ttk.Frame(parent)
    
    period_button = gui.create_button(
        frame, 
        res.BUTTON_START,
        start_pause_period,
        width = -PERIOD_BUTTON_WIDTH
    )
    day_stop_button = gui.create_button(frame, res.BUTTON_END_DAY, stop_day)
    
    return frame

def bind_events(root):
    root.bind('<Control-n>', lambda event: new_project())
    root.bind('<Control-o>', lambda event: open_project())
    root.bind('<Control-s>', lambda event: save_project())
    root.bind('<Control-S>', lambda event: save_project_as())
    root.bind('<Control-w>', lambda event: close_project())
################################################################################

if __name__ == '__main__':
    # Initializing #############################################################
    root = tkinter.Tk()
    root.minsize(MIN_SIZE_X, MIN_SIZE_Y)
    root.wm_title(res.APP_TITLE)
    
    main_menu = create_main_menu(root)
    toolbar(root).pack(anchor = 'n', fill = 'x')
    bind_events(root)
    
    con = controller.Controller(root, adjust_state)
    ############################################################################
    
    root.mainloop()
