﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import tkinter
import tkinter.ttk as ttk

import res
from misc import *

UPDATE_TIME = 100

class PeriodError(Exception):
    pass

class TimeStamp:
    def __init__(self, starttime = None, endtime = None):
        if starttime is None:
            self.starttime = datetime.timedelta()
        else:
            self.starttime = starttime
            
        if endtime is None:
            self.endtime = self.starttime
        else:
            self.endtime = endtime
            
        self.stopped = True
        
        self._weeks = 0
        self._days = 0
        self._hours = 0
        self._minutes = 0
        self._seconds = 0
    
    def __str__(self):
        raise NotImplementedError()
    
    # Helper functions #########################################################
    def _split_times(self, t, length):
        if t >= length:
            val, t = divmod(t, length)
        else:
            val = 0
        return val, t
    
    def _split_length(self):
        minutes, seconds = self._split_times(self.length.seconds, 60)
        hours, minutes = self._split_times(minutes, 60)
        weeks, days = self._split_times(self.length.days, 7)
            
        self._weeks = weeks
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
    ############################################################################

    # Properties ###############################################################
    def get_current(self):
        if not self.stopped:
            self.endtime = datetime.datetime.today()
        return self.endtime
    
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

    def start(self):
        if self.stopped:
            self.starttime = datetime.datetime.today()
            self.endtime = self.starttime
            self.stopped = False
    
    def stop(self):
        if not self.stopped:
            self.endtime = datetime.datetime.today()
            self.stopped = True

class Period(TimeStamp):
    def __init__(self, working_day = None, *args, **kw):
        super().__init__(*args, **kw)
        self.working_day = working_day
        
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
    
class WorkingDay(Period):
    def __init__(self, project, *args, **kw):
        super().__init__(*args, **kw)
        self.periods = []
        self.paused = False
        self.project = project
        
    # Properties ###############################################################
    def _get_current_period(self, cls):
        for p in reversed(self.periods):
            if isinstance(p, cls):
                return p
        raise PeriodError('No "' + cls.__name__ + '" period found in this day.')
    
    def get_length(self):
        length = datetime.timedelta()
        for p in self.periods:
            if isinstance(p, Working):
                length += p.length
        return length
    
    def get_current_working(self):
        return self._get_current_period(Working)
    
    def get_current_pause(self):
        return self._get_current_period(Pause)
    
    def get_current_period(self):
        if self.paused:
            return self.current_pause
        else:
            return self.current_working
    
    length = property(get_length)
    current_working = property(get_current_working)
    current_pause = property(get_current_pause)
    current_period = property(get_current_period)
    ############################################################################
    
    def start(self):
        self.current_working.start()
     
    def pause(self):
        if not self.paused:
            self.current_working.stop()
            self.periods.append(Working(self))
            self.current_pause.start()
            self.paused = True
    
    def resume(self):
        if self.paused:
            self.current_pause.stop()
            self.periods.append(Pause(self))
            self.current_working.start()
            self.paused = False
            
    def stop(self):
        self.current_period.stop()
        super().stop()

class Project(TimeStamp):
    def __init__(self, name, *args, **kw):
        super().__init__(*args, **kw)
        self.name = name
        self.subprojects = []
        self.working_days = []
        self.current_project = None
        self.parent_project = None
        self.started = False
        
        # The start/stop mechanic from the TimeStamp class
        # is not of interest here
        self.stopped = True
        
    def __str__(self):
        return '{:02d}:{:02d}:{:02d}:{:02d}:{:02d}'.format(
            self.weeks,
            self.days,
            self.hours,
            self.minutes,
            self.seconds
        )
        
    # Properties ###############################################################
    def get_length(self):
        td = datetime.timedelta()
        for sp in self.subprojects:
            td += sp.length
        for wd in self.working_days:
            td += wd.length
        return td
    
    def get_current_day(self):
        return self.current_project.working_days[-1]
    
    def get_paused(self):
        return self.current_day.paused
    
    length = property(get_length)
    current_day = property(get_current_day)
    paused = property(get_paused)
    ############################################################################
    
    def start(self, subproject = None):
        '''Starts a new working day of the project.'''
        if self.stopped:
            self.current_day.start()
            self.started = True
            self.stopped = False
    
    def pause(self):
        self.current_day.pause()
    
    def resume(self):
        self.current_day.resume()
    
    def stop(self):
        if not self.stopped:
            self.current_day.stop()
            self.stopped = True

class SubProject(Project):
    def __init__(self, name, project, *args, **kw):
        super().__init__(name, *args, **kw)
        self.parent_project = project

# GUI related ##################################################################
class DisplayContainer:
    def __init__(self, parent, label, period):
        self.frame = None
        self.label = label
        self.parent = parent
        self.content = None
        self.period = period
        
        self.update()
    
    def _cyclic_update(self):
        p = str(self.period)
        if p != self.content.get():
            self.content.set(p)

        self.frame.after(UPDATE_TIME, self._cyclic_update)
        
    def update(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = ttk.Labelframe(self.parent, text = self.label)
        
        self.content = tkinter.StringVar()
        tkinter.Label(self.frame,
            background = 'black',
            foreground = 'yellow',
            font = ('Consolas', 20, 'bold'),
            textvariable = self.content
        ).pack()
        self.content.set(str(self.period))
        
        self.frame.pack(anchor = 'e')
        self.frame.after(UPDATE_TIME, self._cyclic_update)

class TimeWidget:
    def __init__(self, parent, project):
        self.frame = None
        self.parent = parent
        self.project = project
        self.displays = []
        
        self.update()
        
    def __getitem__(self, key):
        for d in self.displays:
            if d.label == key:
                return d
        raise KeyError('Display not found.')
    
    def _build_frame(self):
        day = self.project.current_day
        working = day.current_working
        pause = day.current_pause
        
        if not self.displays:
            self.displays.append(
                DisplayContainer(self.frame, res.DISPLAY_PERIOD, working)
            )
            self.displays.append(
                DisplayContainer(self.frame, res.DISPLAY_PAUSE, pause)
            )
            self.displays.append(DisplayContainer(self.frame, res.DAY, day))
            
            project = day.project
            while project is not None:
                self.displays.append(
                    DisplayContainer(self.frame, project.name, project)
                )
                project = project.parent_project
        else:
            for d in self.displays:
                d.update()
        
    def update(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = ttk.Frame(self.parent)
        self._build_frame()
        self.frame.pack()
################################################################################
