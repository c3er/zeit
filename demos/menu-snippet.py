#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Taken from the IDLE source

menu_specs = [
    ("file", "_File"),
    ("edit", "_Edit"),
    ("format", "F_ormat"),
    ("run", "_Run"),
    ("options", "_Options"),
    ("windows", "_Windows"),
    ("help", "_Help"),
]

def createmenubar(self):
    mbar = self.menubar
    self.menudict = menudict = {}
    for name, label in self.menu_specs:
        underline, label = prepstr(label)
        menudict[name] = menu = Menu(mbar, name=name)
        mbar.add_cascade(label=label, menu=menu, underline=underline)
    if macosxSupport.runningAsOSXApp():
        # Insert the application menu
        menudict['application'] = menu = Menu(mbar, name='apple')
        mbar.add_cascade(label='IDLE', menu=menu)
    self.fill_menus()
    self.recent_files_menu = Menu(self.menubar)
    self.menudict['file'].insert_cascade(3, label='Recent Files',
                                         underline=0,
                                         menu=self.recent_files_menu)
    self.base_helpmenu_length = self.menudict['help'].index(END)
    self.reset_help_menu_entries()
    
def prepstr(s):
    '''Helper to extract the underscore from a string,
	e.g. prepstr("Co_py") returns (2, "Copy").
	'''
    i = s.find('_')
    if i >= 0:
        s = s[:i] + s[i+1:]
    return i, s