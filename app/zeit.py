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
################################################################################

# Appeareance ##################################################################
def toolbar(root):
    global period_button
    
    frame = ttk.Frame(root)
    
    return frame

def content(root):
    global time_content
    
    frame = ttk.Frame(root)
    
    td, time_content = create_time_display(root, 'Zeit', period)
    td.pack(padx = 2, pady = 2)
    
    return frame
################################################################################

if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title(res.APP_TITLE)
    period = timelib.Working()
    content(root).pack(fill = 'both')
    root.after(UPDATE_TIME, curry(update_time, root))
    root.mainloop()
