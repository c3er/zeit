#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Helper module for using Tk.'''

import tkinter
import tkinter.ttk as ttk

class CanDisabled:
    def disable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'disabled')
    
    def enable(self):
        self.parent.tkmenu.entryconfigure(self.label, state = 'enabled')

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
    
class SubMenu(Menu, CanDisabled):
    def __init__(self, label, parent, *args, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.label = label
    
class MenuItem(CanDisabled):
    def __init__(self, parent, label, command):
        self.parent = parent
        self.label = label
        self.command = command

def disable(widget):
    if isinstance(widget, (tkinter.Button, ttk.Button)):
        widget.config(state = 'disabled')
    elif isinstance(widget, (SubMenu, MenuItem)):
        widget.disable()
    else:
        raise TypeError()

def enable(widget):
    if isinstance(widget, (tkinter.Button, ttk.Button)):
        widget.config(state = 'enabled')
    elif isinstance(widget, (SubMenu, MenuItem)):
        widget.enable()
    else:
        raise TypeError()

def create_button(frame, label, command):
    button = ttk.Button(frame, text = label, command = command)
    button.pack(side = 'left')
    return button
