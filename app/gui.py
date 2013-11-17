#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Helper module for using Tk.'''

import tkinter
import tkinter.ttk as ttk

class _CanDisabled:
    '''Helper class to make it possible to disable/enable menu items.'''
    
    def disable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'disabled')
    
    def enable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'normal')

# Menu related #################################################################
class Menu:
    def __init__(self, tkparent):
        self.children = []
        
        # XXX...
        if not isinstance(self, SubMenu):
            tkparent.option_add('*tearOff', False)
            
        self.tkmenu = tkinter.Menu(tkparent)
        
        # ... ugly!
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
    
class SubMenu(Menu, _CanDisabled):
    def __init__(self, label, parent, *args, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.label = label
    
class MenuItem(_CanDisabled):
    def __init__(self, parent, label, command):
        self.parent = parent
        self.label = label
        self.command = command
################################################################################

def disable(widget):
    if isinstance(widget, (tkinter.Button, ttk.Button)):
        widget.config(state = 'disabled')
    elif isinstance(widget, _CanDisabled):
        widget.disable()
    else:
        raise TypeError()

def enable(widget):
    if isinstance(widget, (tkinter.Button, ttk.Button)):
        widget.config(state = 'enabled')
    elif isinstance(widget, _CanDisabled):
        widget.enable()
    else:
        raise TypeError()

def create_button(frame, label, command, *args, **kw):
    button = ttk.Button(frame, *args, text = label, command = command, **kw)
    button.pack(side = 'left')
    return button

def bind_events(widget, event_mapping):
    for event, func in event_mapping.items():
        widget.bind(event, func)
        
# This stuff was originally from some demos ####################################
class AutoScrollbar(ttk.Scrollbar):
    '''A scrollbar that hides it self if it's not needed.
    Only works if you use the grid geometry manager.
    '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)
        
    def pack(self, **kw):
        raise tkinter.TclError("Can not use pack with this widget")
    
    def place(self, **kw):
        raise tkinter.TclError("Can not use place with this widget")
################################################################################
