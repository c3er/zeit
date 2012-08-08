#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

import timelib
from misc import *

UPDATE_TIME = 100

time_content = None
counter = 0
period = None

def update_time(root):
    p = str(period)
    if p != time_content.get():
        time_content.set(p)
        
    root.after(UPDATE_TIME, curry(update_time, root))

def content(root):
    global time_content
    
    frame = ttk.Frame(root)
    
    time_content = tkinter.StringVar()
    tkinter.Label(frame,
        background = 'black',
        foreground = 'yellow',
        font = ('Consolas', 20, 'bold'),
        textvariable = time_content
    ).pack()
    time_content.set('0')
    
    return frame

if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title('Zeiterfassung')
    period = timelib.Period()
    content(root).pack(fill = 'both')
    root.after(UPDATE_TIME, curry(update_time, root))
    root.mainloop()
