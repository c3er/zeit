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
        
        self._weeks = 0
        self._days = 0
        self._hours = 0
        self._minutes = 0
        self._seconds = 0
    
    def __str__(self):
        raise NotImplementedError
    
    # Properties ###############################################################
    def get_current(self):
        if not self._ended:
            self._current = datetime.datetime.today()
        return self._current
    
    def get_length(self):
        return self.current - self.starttime
    
    def get_weeks(self):
        self._split_length()
        return self._weeks
    
    def get_days(self):
        self._split_length()
        return self._days
    
    def get_hours(self):
        self._split_length()
        return self._hours
    
    def get_minutes(self):
        self._split_length()
        return self._minutes
    
    def get_seconds(self):
        self._split_length()
        return self._seconds
    
    current = property(get_current)
    length = property(get_length)
    
    weeks = property(get_weeks)
    days = property(get_days)
    hours = property(get_hours)
    minutes = property(get_minutes)
    seconds = property(get_seconds)
    ############################################################################
    
    def _split_length(self):
        minutes, seconds = _split_times(self.length.seconds, 60)
        hours, minutes = _split_times(minutes, 60)
        weeks, days = _split_times(self.length.days, 7)
            
        self._weeks = weeks
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
    
    def end(self):
        if not self._ended:
            self._current = datetime.datetime.today()
            self._ended = True
            
    def stop():
        raise NotImplementedError
    
    def resume(self):
        raise NotImplementedError

class Period(TimeStamp):
    def __str__(self):
        return '{:02d}:{:02d}:{:02d}'.format(
            self.hours,
            self.minutes,
            self.seconds
        )
    
class Working(Period):
    pass

class Pause(Period):
    pass
    
class Day(TimeStamp):
    pass

class Project(TimeStamp):
    def __init__(self):
        super().__init__()
        #...

class SubProject(Project):
    pass

def _split_times(t, length):
    if t >= length:
        val, t = divmod(t, length)
    else:
        val = 0
    return val, t