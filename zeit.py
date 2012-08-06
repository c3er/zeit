#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import time
#import calendar

import tkinter
import tkinter.ttk as ttk

time_content = None
counter = 0

class curry:
    '''Handles arguments for callback functions.'''
    def __init__(self, callback, *args, **kw):
        self.callback = callback
        self.args = args
        self.kw = kw

    def __call__(self):
        return self.callback(*self.args, **self.kw)

def update_time(root):
    global counter
    
    counter += 1
    if (counter % 10) == 0:
        val = int(time_content.get())
        time_content.set(str(val + 1))
        
    root.after(100, curry(update_time, root))

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
    content(root).pack(fill = 'both')
    root.after(100, curry(update_time, root))
    root.mainloop()
