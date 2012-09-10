#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Mediator between the GUI and the data.'''

import timelib
import res
from misc import *

class UnknownPathException(Exception):
    pass

class Controller:
    def __init__(self, root, state_handler):
        self.root = root
        self.state_handler = state_handler
        self.modified = False
        self.project = None
        self.time_widget = None
        self.new_project()
        
    def new_project(self, name = res.UNNAMED):
        self.project = timelib.Project(name)
        self.time_widget = timelib.TimeWidget(self.root, self.project)
    
    def open_project(self, path):
        pass
    
    def save_project(self, path = None):
        pass
    
    def close_project(self):
        pass
    
    def start_time(self):
        self.project.start()
        self.modified = True
        print('Time started')
    
    def stop_time(self):
        pass
    
    def pause_time(self):
        pass
    
    def resume_time(self):
        pass
    
    def update(self):
        self.state_handler(self)
        #...
