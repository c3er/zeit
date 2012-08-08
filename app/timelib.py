#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime

from misc import *

class TimeStamp:
    def __init__(self):
        self.starttime = datetime.datetime.today()
        self._current = self.starttime
        self._ended = False
    
    def __str__(self):
        raise NotImplementedError
    
    # Properties ###############################################################
    def get_current(self):
        if not self._ended:
            self._current = datetime.datetime.today()
        return self._current
    
    def get_length(self):
        return self.current - self.starttime
    
    current = property(get_current)
    length = property(get_length)
    ############################################################################
    
    def end(self):
        if not self._ended:
            self._current = datetime.datetime.today()
            self._ended = True

class Period(TimeStamp):
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        length = self.length
        minutes, seconds = divmod(length.seconds, 60)
        if minutes > 59:
            hours, minutes = divmod(minutes, 60)
        else:
            hours = 0
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    
class Pause(TimeStamp):
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        pass