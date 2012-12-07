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
        self.root = root
        self.state_handler = state_handler
        self._modified = False
        self.path = None
        self.project = None
        self.time_widget = None
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
    
    def _basic_wrapper(self, condition, func):
        if condition:
            func()
            self._modified = True
            self.update()
            
    def _ext_wrapper(self, condition, func, period, key):
        if condition:
            func()
            self.time_widget[key].period = period
            self._modified = True
            self.update()
        
    def new_project(self, name = res.UNNAMED):
        path = os.path.join(sys.path[0], res.DEFAULT_FILE)
        self.project = fio.load(path)
        self.time_widget = timelib.TimeWidget(self.root, self.project)
    
    def open_project(self, path):
        self.project = fio.load(path)
    
    def save_project(self, path = None):
        if path is not None:
            self.path = path

        if not self.path:
            raise UnknownPathException()
        else:
            fio.save(self.project, path)
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
    
    def update(self):
        self.state_handler(self)
        #...
