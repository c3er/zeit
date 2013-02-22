#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Mediator between the GUI and the data.'''

import sys
import os

import timelib
import fio
import res
from misc import *

class UnknownPathException(Exception):
    pass

class Controller:
    def __init__(self, root, state_handler):
        '''Constructor of the "Controller" class.
        
        Parameters:
        - root: Toplevel widget of Tk.
        - state_handler: A handler function, which updates the GUI,
          depending on the internal state of the controller.
        '''
        self.root = root
        self.state_handler = state_handler
        self._modified = False
        self.path = None
        self.project = None
        self.time_widget = None
        self.isnew = True
        self.new_project()
        
    # Properties ###############################################################
    def get_started(self):
        return self.project.started
    
    def get_paused(self):
        return self.project.paused
    
    def get_modified(self):
        if self.started and not self.paused:
            return True
        else:
            return self._modified
    
    started = property(get_started)
    paused = property(get_paused)
    modified = property(get_modified)
    ############################################################################
    
    # Internal helper functions ################################################
    def _basic_wrapper(self, condition, func):
        '''A wrapper function, which calls the given function, if the given
        condition evaluates to "True", sets the state to "modified" and updates
        the view.
        
        Parameters:
        - condition: If this evaluates to "False", nothing will happen.
        - func: A function object, which will be called only, if the condition
          evaluates to "True".
        '''
        if condition:
            func()
            self._modified = True
            self.isnew = False
            self.update()
            
    def _ext_wrapper(self, condition, func, period, name):
        '''Like the basic wrapper, but additionally it assigns to the display
        with the given name another period object.
        
        Parameters:
        - condition: If this evaluates to "False", nothing will happen.
        - func: A function object, which will be called only, if the condition
          evaluates to "True".
        - period: A "Period" object, which will be assigned to the given
          display.
        - name: The name of the display, which will get another "Period" object.
        '''
        if condition:
            func()
            self.time_widget[name].period = period
            self._modified = True
            self.isnew = False
            self.update()
    ############################################################################
    
    def update(self):
        self.state_handler(self)
        #...
        
    # Interface functions for the GUI handler ##################################
    def new_project(self, name = res.UNNAMED):
        path = os.path.join(sys.path[0], res.DEFAULT_FILE)
        self.project = fio.load(path)
        self.time_widget = timelib.TimeWidget(self.root, self.project)
        self.update()
    
    def open_project(self, path):
        self.project = fio.load(path)
        self.time_widget = timelib.TimeWidget(self.root, self.project)
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
