#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

DEBUG = True

def error(msg, exc = None):
    excmsg = '\n' + str(exc) if exc is not None else ''
    tkinter.messagebox.showerror(res.STD_ERROR_TITLE, msg + excmsg)

# This stuff was originally from some demos ####################################
class AutoScrollbar(ttk.Scrollbar):
    '''A scrollbar that hides it self if it's not needed.
    Only works if you use the grid geometry manager.'''
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)
        
    def pack(self, **kw):
        raise TclError("Can not use pack with this widget")
    
    def place(self, **kw):
        raise TclError("Can not use place with this widget")

class curry:
    '''Handles arguments for callback functions.'''
    def __init__(self, callback, *args, **kw):
        self.callback = callback
        self.args = args
        self.kw = kw

    def __call__(self):
        return self.callback(*self.args, **self.kw)
################################################################################
