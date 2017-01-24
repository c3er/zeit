#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""GUI elements to use for time recording."""


import datetime
import collections
import tkinter
import tkinter.ttk as ttk

import timedata
import gui
import res


class CyclicUpdatable:
    def cyclic_update(self):
        raise NotImplementedError()


class DisplayContainer(CyclicUpdatable):
    def __init__(self, parent, label, period):
        self.frame = None
        self.label = label
        self.parent = parent
        self.content = None
        self.period = period
        
        self.update()
    
    def cyclic_update(self):
        p = str(self.period)
        if p != self.content.get():
            self.content.set(p)
        
    def update(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = ttk.Labelframe(self.parent, text=self.label)
        
        self.content = tkinter.StringVar()
        tkinter.Label(
            self.frame,
            background='black',
            foreground='yellow',
            font=('Consolas', 20, 'bold'),
            textvariable=self.content
        ).pack()
        self.content.set(str(self.period))
        
        self.frame.pack(anchor='e')


class TimeWidget(CyclicUpdatable):
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
            self.displays.append(DisplayContainer(self.frame, res.DISPLAY_PERIOD, working))
            self.displays.append(DisplayContainer(self.frame, res.DISPLAY_PAUSE, pause))
            self.displays.append(DisplayContainer(self.frame, res.DAY, day))
            
            project = day.project
            while project is not None:
                self.displays.append(DisplayContainer(self.frame, project.name, project))
                project = project.parent_project
        else:
            for d in self.displays:
                d.update()
        
    def cyclic_update(self):
        for d in self.displays:
            d.cyclic_update()
        
    def update(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = ttk.Frame(self.parent)
        self._build_frame()
        

class ProjectWidgetItem(collections.UserList):
    """An item for the "ProjectWidget". Basically this object consists of a list
    of the values, which shall be shown. This implementation is able to get
    access to the current values of the actual item, not just the values of
    creation time of an instance of this class.
    """
    def __init__(self, item, item_name, values):
        """Parameters:
            - item: An item, which must be a subclass of "_TimeStemp".
            - item_name: Name of the item. Must be identical to the name, which
              is used in the "values".
            - values: Not actual values but strings, which must contain valid
              python code. When the data is accessed, these "values" will be
              evaluated. This is done this way, to get always the current values
              of the item instead of the values of creation time of this object.
              Note: The count of the values list must be identical to the column
              count of the ProjectWidget, to which this object belongs to.
        """
        super().__init__()
        
        self.children = []
        self.parent = self._link2parent(item)
        
        self.item = item
        self.item_name = item_name
        
        self.__data = None
        self.data = self._build_data(values)
        
        self.lastcalled = ()
        self._tmpdata = []
        
    def __hash__(self):
        return id(self)
    
    # Helper functions #########################################################
    @staticmethod
    def _build_data(data):
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(item)
            else:
                raise TypeError('Values must be strings, containing valid Python code.')
        return result
    
    def _link2parent(self, item):
        # XXX Very hacky
        setattr(item, 'widget_ref', self)
        itemparent = item.parent
        
        if itemparent is None:
            return None
        elif not hasattr(itemparent, 'widget_ref'):
            raise AttributeError('Parent of item is not assigned to a "ProjectWidgetItem" yet.')
        else:
            parent = itemparent.widget_ref
            parent.children.append(self)
            return parent
    ############################################################################
    
    # Properties ###############################################################
    # XXX May break in future implementations of "collections.UserList".
    # The attribute "data" of "collections.UserList" is overwritten with
    # properties to accomplish the needed functionality.
    
    @property
    def data(self):
        namespace = {self.item_name: self.item}
        data = []
        
        for val in self.__data:
            result = eval(val, namespace)
            
            if hasattr(result, 'microsecond'):
                us = result.microsecond
            elif hasattr(result, 'microseconds'):
                us = result.microseconds
            
            us = datetime.timedelta(microseconds = us)
            result -= us
            data.append(str(result))
            
        self.lastcalled = tuple(self._tmpdata)
        self._tmpdata = data
        
        return data
    
    @data.setter
    def data(self, val):
        if isinstance(val, (list, collections.UserList)):
            self.__data = val
        else:
            raise TypeError('Value can only be a list object.')
    ############################################################################
        
        
class ProjectWidget(CyclicUpdatable):
    def __init__(self, parent, project):
        event_mapping = {
            '<<TreeviewOpen>>': self.update_tree,
            "<MouseWheel>": self.wheelscroll,
        }
        self.timestamp_values = (
            'stamp.starttime',
            'stamp.stoptime',
            'stamp.stoptime - stamp.starttime'
        )
        self.project = project
        self.frame = ttk.Frame(parent)
        self.treeview = self._build_treeview(self.frame, project, event_mapping)
        self.period_mapping = self._connect_project(project)
        
    # Helper functions for initializing ########################################
    def _connect_project(self, project):
                
        def insert_items(period_mapping, timestamp, parent):
            item, node = self._insert_item(timestamp, parent)
            period_mapping[item] = node
            for child in timestamp.children:
                insert_items(period_mapping, child, node)
        
        if type(project) != timedata.Project:
            raise TypeError('Parameter "project" must be of type "Project".')
        
        period_mapping = collections.OrderedDict()
        insert_items(period_mapping, project, '')

        return period_mapping
        
    @staticmethod
    def _build_treeview(parent, project, event_mapping):
        
        def setup_columns(tree, columns):
            tree.heading('#0', text = res.PROJECT_COLUMN_NAME, anchor='w')
            for col in columns:
                tree.heading(col, text=col, anchor='w')
                tree.column(col, width=100)
                
        def setup_scrollbars(parent, tree):
            vsb = gui.AutoScrollbar(parent, orient="vertical", command=tree.yview)
            hsb = gui.AutoScrollbar(parent, orient = "horizontal", command = tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            tree.grid(column=0, row=0, sticky='nsew', in_=parent)
            vsb.grid(column=1, row=0, sticky='ns')
            hsb.grid(column=0, row=1, sticky='ew')
    
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_rowconfigure(0, weight=1)
            
        columns = (
            res.PROJECT_COLUMN_FROM,
            res.PROJECT_COLUMN_UNTIL,
            res.PROJECT_COLUMN_DURATION
        )
        tree = ttk.Treeview(columns=columns)
        
        setup_columns(tree, columns)
        setup_scrollbars(parent, tree)
        
        gui.bind_events(tree, event_mapping)
    
        return tree
    ############################################################################
    
    def _insert_item(self, timestamp, tkparent):
        item = ProjectWidgetItem(timestamp, 'stamp', self.timestamp_values)
        node = self.treeview.insert(
            tkparent,
            'end',
            text=timestamp.name,
            values=tuple(item),
            open=True
        )
        return item, node
    
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
        # XXX
        pass
    ############################################################################
    
    def cyclic_update(self):
        for item, node in self.period_mapping.items():
            lastcalled = item.lastcalled
            itemdata = tuple(item)
            if itemdata != lastcalled:
                self.treeview.item(node, values=itemdata)
    
    def add_item(self, period):
        parent = period.parent
        if parent is None:
            raise ValueError('"period" must be a subelement of an existing item.')

        parent_item = parent.widget_ref
        for child in parent_item.children:
            if child.item == period:
                return
        
        parent_node = self.period_mapping[parent_item]
        item, node = self._insert_item(period, parent_node)
        self.period_mapping[item] = node
