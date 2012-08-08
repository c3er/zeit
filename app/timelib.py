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
        minutes, seconds = divmod(self.length.seconds, 60)
        
        if minutes >= 60:
            hours, minutes = divmod(minutes, 60)
        else:
            hours = 0
            
        days = self.length.days
        
        if days >= 7:
            weeks, days = divmod(days, 7)
        else:
            weeks = 0
            
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
        pass
    
    def resume(self):
        pass

class Period(TimeStamp):
    def __str__(self):
        return '{:02d}:{:02d}:{:02d}'.format(
            self.hours,
            self.minutes,
            self.seconds
        )
    
class Pause(TimeStamp):
    def __str__(self):
        pass
    
class Day:
    pass

class Project:
    pass

class SubProject(Project):
    pass