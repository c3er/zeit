#!/usr/bin/env python
# -*- coding: utf-8 -*-

'Data structures to manage project oriented time recording.'

import datetime

import res

class PeriodError(Exception):
    pass

# Base classes. Shall not be instancieted directly. ############################
class _TimeStamp:
    def __init__(self, starttime = None, stoptime = None):
        if starttime is None:
            self.starttime = datetime.timedelta()
        else:
            self.starttime = starttime
            
        if stoptime is None:
            self.stoptime = self.starttime
        else:
            self.stoptime = stoptime
            
        self.stopped = True
        
        self._weeks = 0
        self._days = 0
        self._hours = 0
        self._minutes = 0
        self._seconds = 0
    
    def __str__(self):
        'Needs to be implemented by inheriting classes.'
        raise NotImplementedError()
    
    # Helper functions #########################################################
    @staticmethod
    def _split_times(t, length):
        '''Helper function to split a great number of a period (e.g. seconds)
        into the corresponding value of the greater period (e.g. minutes) and
        the remaining part of the given period.
        
        Parameters:
            - t: The value, which shall be splitted.
            - length: the length of the bigger period. E.g. the value would be
              60 if "t" would be a value in seconds and the bigger period shall
              be minutes.
        
        Returns:
            A tuple, containing two Values:
                1. The value in the bigger period.
                2. The remaining part of the smaller period.
        '''
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
        
    def _get_time(self, t):
        self._split_length()
        return t
    ############################################################################

    # Properties ###############################################################
    @property
    def current(self):
        if not self.stopped:
            self.stoptime = datetime.datetime.today()
        return self.stoptime
    
    @property
    def length(self):
        return self.current - self.starttime
    
    @property
    def weeks(self):
        return self._get_time(self._weeks)
    
    @property
    def days(self):
        return self._get_time(self._days)
    
    @property
    def hours(self):
        return self._get_time(self._hours)
    
    @property
    def minutes(self):
        return self._get_time(self._minutes)
    
    @property
    def seconds(self):
        return self._get_time(self._seconds)
    
    @property
    def name(self):
        'Needs to be implemented by inheriting classes.'
        raise NotImplementedError()
    
    @property
    def parent(self):
        'Needs to be implemented by inheriting classes.'
        raise NotImplementedError()
    
    @property
    def children(self):
        'Needs to be implemented by inheriting classes.'
        raise NotImplementedError()
    ############################################################################

    def start(self):
        if self.stopped:
            self.starttime = datetime.datetime.today()
            self.stoptime = self.starttime
            self.stopped = False
    
    def stop(self):
        if not self.stopped:
            self.stoptime = datetime.datetime.today()
            self.stopped = True

class _Period(_TimeStamp):
    def __init__(self, working_day = None, *args, **kw):
        super().__init__(*args, **kw)
        self.working_day = working_day
        
    def __str__(self):
        return '{:02d}:{:02d}:{:02d}'.format(
            self.hours,
            self.minutes,
            self.seconds
        )
    
    @property
    def parent(self):
        return self.working_day
        
class _AtomicPeriod(_Period):
    'A Period that cannot have child Periods.'
    @property
    def children(self):
        return []
################################################################################
    
class Working(_AtomicPeriod):
    @property
    def name(self):
        return res.PERIOD_NAME_WORKING

class Pause(_AtomicPeriod):
    @property
    def name(self):
        return res.PERIOD_NAME_PAUSE
    
class WorkingDay(_Period):
    def __init__(self, project, *args, **kw):
        super().__init__(*args, **kw)
        self.periods = []
        self.paused = False
        self.project = project
        self._date_str = None
        
    def _get_current_period(self, cls):
        for p in reversed(self.periods):
            if isinstance(p, cls):
                return p
        raise PeriodError('No "' + cls.__name__ + '" period found in this day.')
    
    def _get_working_periods(self):
        working_periods = []
        for p in self.periods:
            if isinstance(p, Working):
                working_periods.append(p)
        return working_periods
    
    # Properties ###############################################################
    @property
    def length(self):
        length = datetime.timedelta()  # 0
        for p in self.periods:
            if isinstance(p, Working):
                length += p.length
        return length
    
    @property
    def current_working(self):
        return self._get_current_period(Working)
    
    @property
    def current_pause(self):
        return self._get_current_period(Pause)
    
    @property
    def current_period(self):
        if self.paused:
            return self.current_pause
        else:
            return self.current_working
        
    @property
    def date_str(self):
        if self._date_str is None:
            working_periods = self._get_working_periods()
            if not working_periods:
                raise PeriodError()
            
            starttime = working_periods[0].starttime
            self._date_str = str(starttime.date())

        return self._date_str
        
    @property
    def name(self):
        return ' '.join((res.DAY, self.date_str))
    
    @property
    def parent(self):
        return self.project
    
    @property
    def children(self):
        return self.periods
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

class Project(_TimeStamp):
    '''Note: The implementation needs to be instanciated from a file to work
    properly.
    '''
    def __init__(self, name, *args, **kw):
        super().__init__(*args, **kw)
        self._name = None
        self.name = name
        self.subprojects = []
        self.working_days = []
        self.current_project = None
        self.parent_project = None
        self.started = False
        
        # The start/stop mechanism from the TimeStamp class
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
    @property
    def length(self):
        td = datetime.timedelta()
        for sp in self.subprojects:
            td += sp.length
        for wd in self.working_days:
            td += wd.length
        return td
    
    @property
    def current_day(self):
        return self.current_project.working_days[-1]
    
    @property
    def paused(self):
        return self.current_day.paused
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        self._name = val
    
    @property
    def parent(self):
        return None
    
    @property
    def children(self):
        return self.subprojects + self.working_days
    ############################################################################
    
    def start(self, subproject = None):
        'Starts a new working day of the project.'
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
    
    @property
    def parent(self):
        return self.parent_project
