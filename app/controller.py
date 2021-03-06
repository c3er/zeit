﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Mediator between the GUI and the data."""


import sys
import os

import timegui
import fio
import res
from misc import *


UPDATE_TIME = 100  # milliseconds


class UnknownPathException(Exception):
    pass


class Controller:
    # XXX This class knows too much about the actual GUI.
    def __init__(self, root, state_handler):
        """Constructor of the "Controller" class.
        
        Parameters:
        - root: Toplevel widget of Tk.
        - state_handler: A handler function, which updates the GUI,
          depending on the state of the controller.
        """
        # GUI related
        self.root = root
        self.frame = None
        self.time_widget = None
        self.project_widget = None
        self.cyclic_handlers = []
        self.state_handler = state_handler
        
        # Data
        self.path = None
        self.project = None
        
        # Data state
        self._modified = False
        self.isnew = True
        
        self.new_project()
        
    # Properties ###############################################################
    @property
    def started(self):
        return self.project.started
    
    @property
    def paused(self):
        return self.project.paused
    
    @property
    def modified(self):
        if self.started and not self.paused:
            return True
        else:
            return self._modified
    ############################################################################
    
    # Internal helper functions ################################################
    def _basic_wrapper(self, condition, func):
        """A wrapper function, which calls the given function, if the given
        condition evaluates to "True", sets the state to "modified" and updates
        the view.
        
        Parameters:
        - condition: If this evaluates to "False", nothing will happen.
        - func: A function object, which will be called only, if the condition
          evaluates to "True".
        """
        if condition:
            func()
            self._modified = True
            self.isnew = False
            self.update()
            
    def _ext_wrapper(self, condition, func, period, name):
        """Like the basic wrapper, but additionally it assigns to the display
        with the given name another period object.
        
        Parameters:
        - condition: If this evaluates to "False", nothing will happen.
        - func: A function object, which will be called only, if the condition
          evaluates to "True".
        - period: A "Period" object, which will be assigned to the given
          display.
        - name: The name of the display, which will have assigned another
          "Period" object.
        """
        if condition:
            func()
            self.time_widget[name].period = period
            self.project_widget.add_item(period)
            self._modified = True
            self.isnew = False
            self.update()
            
    def _register_cyclic_handler(self, widget):
        if not isinstance(widget, timegui.CyclicUpdatable):
            raise TypeError(
                '"widget" must be an instance of "timegui.CyclicUpdatable".'
            )
        self.cyclic_handlers.append(widget)
            
    def _build_frame(self, parent, project):
        if self.frame:
            self.frame.destroy()
        self.frame = ttk.Frame(parent)
        
        self.project_widget = timegui.ProjectWidget(self.frame, project)
        self.project_widget.frame.pack(
            side='left',
            fill='both',
            expand=True
        )
        self._register_cyclic_handler(self.project_widget)
        
        self.time_widget = timegui.TimeWidget(self.frame, project)
        self.time_widget.frame.pack(side = 'left', anchor='n')
        self._register_cyclic_handler(self.time_widget)
        
        self.frame.pack(fill='both', expand=True)
        self.frame.after(UPDATE_TIME, self.cyclic_update)
    ############################################################################
    
    # Handlers for events, which are not caused dirctly by the user ############
    def update(self):
        self.state_handler(self)
        #...
        
    def cyclic_update(self):
        for c in self.cyclic_handlers:
            c.cyclic_update()
        self.frame.after(UPDATE_TIME, self.cyclic_update)
    ############################################################################
        
    # Interface functions for the GUI handler ##################################
    def new_project(self):
        """Loads a default file, containing an empty project
        and updates the GUI.
        """
        path = os.path.join(sys.path[0], res.DEFAULT_FILE)
        self.project = fio.load(path)
        self._build_frame(self.root, self.project)
        self.update()
    
    def open_project(self, path):
        self.project = fio.load(path)
        self._build_frame(self.root, self.project)
        self.isnew = False
        self.path = path
        self.update()
    
    def save_project(self, path = None):
        if path is not None:
            self.path = path

        if not self.path:
            raise UnknownPathException()
        else:
            fio.save(self.project, self.path)
            self.update()
    
    def close_project(self):
        pass
    
    def start(self):
        self._basic_wrapper(not self.started, self.project.start)
    
    def pause(self):
        self._ext_wrapper(
            self.started and not self.paused,
            self.project.pause,
            self.project.current_day.current_pause,
            res.DISPLAY_PAUSE
        )
    
    def resume(self):
        self._ext_wrapper(
            self.started and self.paused,
            self.project.resume,
            self.project.current_day.current_working,
            res.DISPLAY_PERIOD
        )
    
    def stop(self):
        self._basic_wrapper(self.started, self.project.stop)
    ############################################################################
