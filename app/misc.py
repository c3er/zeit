#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

DEBUG = True

def error(msg, exc = None):
    excmsg = '\n' + str(exc) if exc is not None else ''
    tkinter.messagebox.showerror(res.STD_ERROR_TITLE, msg + excmsg)

# This stuff was originally from some demos ####################################
class curry:
    '''Handles arguments for callback functions.'''
    def __init__(self, callback, *args, **kw):
        self.callback = callback
        self.args = args
        self.kw = kw

    def __call__(self):
        return self.callback(*self.args, **self.kw)
################################################################################
