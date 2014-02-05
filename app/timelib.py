#!/usr/bin/env python
# -*- coding: utf-8 -*-

'Data structures to manage project oriented time recording.'

import datetime
import collections
import tkinter
import tkinter.ttk as ttk

import gui
import res
from misc import *

UPDATE_TIME = 100

class PeriodError(Exception):
    pass

# Base classes. Shall not be instancieted directly. ############################
class _TimeStamp:
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
            self.endtime = datetime.datetime.today()
        return self.endtime
    
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
            self.endtime = self.starttime
            self.stopped = False
    
    def stop(self):
        if not self.stopped:
            self.endtime = datetime.datetime.today()
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
        return None
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
        def find_starttime(working_periods):
            first_working = working_periods[0]
            if not first_working.started:
                return datetime.datetime.today()
            else:
                return first_working.starttime
        
        if self._date_str is None:
            working_periods = self._get_working_periods()
            if not working_periods:
                raise PeriodError()
            
            starttime = find_starttime(working_periods)
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
        
class ProjectWidgetItem(collections.UserList):
    def __init__(self, item, item_name, *args):
        super().__init__()
        
        self.__data = None
        self.item = item
        self.item_name = item_name
        
        if args is not None:
            self.data = self._build_data(args)
        else:
            raise PeriodError('No data found in the arguments.')
    
    @staticmethod
    def _build_data(data):
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(item)
            else:
                raise TypeError(
                    'Arguments must be strings, containing valid Python code.'
                )
        return result
    
    # Properties ###############################################################
    @property
    def parent(self):
        return self.item.parent
    
    @property
    def children(self):
        return self.item.children
    
    @property
    def data(self):
        namespace = {self.item_name: self.item}
        return [str(eval(item, namespace)) for item in self.__data]
    
    @data.setter
    def data(self, val):
        if isinstance(val, (list, collections.UserList)):
            self.__data = val
        else:
            raise TypeError()
    ############################################################################
        
class ProjectWidget:
    def __init__(self, parent, project):
        event_mapping = {
            '<<TreeviewOpen>>': self.update_tree,
            "<MouseWheel>": self.wheelscroll,
        }
        self.project = project
        self.frame = ttk.Frame(parent)
        self.treeview = self._build_treeview(self.frame, project, event_mapping)
        self.period_mapping = self._connect_project(self.treeview, project)
        
    # Helper functions #########################################################
    @staticmethod
    def _connect_project(treeview, project):
        def insert_children(treeview, period_mapping, parent):
            # XXX
            for child in parent.children:
                pass
        
        if type(project) != Project:
            raise TypeError('Parameter "project" must be of type "Project".')
        
        period_mapping = collections.OrderedDict()
        item = ProjectWidgetItem(
            project,
            'project',
            'project.name',
            'project.starttime',
            'project.endtime',
            'project.endtime - project.starttime'
        )
        node = treeview.insert('', 'end', values = tuple(item))
        period_mapping[node] = item
        
        insert_children(treeview, period_mapping, project)
        # ...
        return period_mapping
        
    @staticmethod
    def _build_treeview(parent, project, event_mapping):
        def setup_columns(tree, columns):
            for col in columns:
                tree.heading(col, text = col, anchor = 'w')
                tree.column(col, width = 100)
                
        def setup_scrollbars(parent, tree):
            vsb = gui.AutoScrollbar(parent,
                orient = "vertical",
                command = tree.yview
            )
            hsb = gui.AutoScrollbar(parent,
                orient = "horizontal",
                command = tree.xview
            )
            tree.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
            tree.grid(column = 0, row = 0, sticky = 'nsew', in_ = parent)
            vsb.grid(column = 1, row = 0, sticky = 'ns')
            hsb.grid(column = 0, row = 1, sticky = 'ew')
    
            parent.grid_columnconfigure(0, weight = 1)
            parent.grid_rowconfigure(0, weight = 1)
            
        columns = (
            res.PROJECT_COLUMN_NAME,
            res.PROJECT_COLUMN_FROM,
            res.PROJECT_COLUMN_UNTIL,
            res.PROJECT_COLUMN_DURATION
        )
        tree = ttk.Treeview(columns = columns, show = "headings")
        
        setup_columns(tree, columns)
        setup_scrollbars(parent, tree)
        
        gui.bind_events(tree, event_mapping)
    
        return tree
    ############################################################################
    
    # Handlers #################################################################
    @staticmethod
    def wheelscroll(event):
        tree = event.widget
        if isinstance(tree, ttk.Treeview):
            if event.delta > 0:
                tree.yview('scroll', -2, 'units')
            else:
                tree.yview('scroll', 2, 'units')

    def update_tree(self, event):
        pass
    ############################################################################
    
    def update(self):
        pass
################################################################################
