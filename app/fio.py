#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''File Input/Output'''

import html.parser
import html.entities

import timelib
import res

# Version of the table file.
CURRENT_FILE_VERSION = '0.1'

class ProjectFileError(Exception):
    pass

class MarkupReaderBase(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tmpdat = ''
        self._read_data_flag = False
        self.starttags = {}
        self.endtags = {}

    def __enter__(self):
        return self.__class__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    # Properties ###############################################################
    def get_read_data_flag(self):
        return self._read_data_flag
    
    def set_read_data_flag(self, val):
        self._read_data_flag = val
        self.tmpdat = ''
    
    read_data_flag = property(get_read_data_flag, set_read_data_flag)
    ############################################################################
    
    # Inherited from html.parser.HTMLParser ####################################
    def handle_starttag(self, tag, attrs):
        try:
            self.starttags[tag](attrs)
        except KeyError:
            pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        try:
            self.endtags[tag]()
        except KeyError:
            pass

    def handle_data(self, data):
        if self.read_data_flag:
            self.tmpdat += data

    def handle_charref(self, name):
        if self.read_data_flag:
            try:
                self.tmpdat += chr(int(name))
            except ValueError:
                self.tmpdat += '&' + str(int(name)) + ';'

    def handle_entityref(self, name):
        if self.read_data_flag:
            self.tmpdat += html.entities.entitydefs[name]
    ############################################################################
    
class ProjectFileReader(MarkupReaderBase):
    def __init__(self):
        super().__init__()
        
        self._project_stack = []
        self.project = None
        
        self.starttags = {
            'projectfile': self.projectfile_start,
            'project': self.project_start,
            'subprojects': self.subprojects_start,
            'subproject': self.subproject_start,
            'working_days': self.working_days_start,
            'wday': self.wday_start,
            'working': self.working_start,
            'pause': self.pause_start,
            'starttime': self.starttime_start,
            'endtime': self.endtime_start,
        }
        self.endtags = {
            'projectfile': self.projectfile_end,
            'project': self.project_end,
            'subprojects': self.subprojects_end,
            'subproject': self.subproject_end,
            'working_days': self.working_days_end,
            'wday': self.wday_end,
            'working': self.working_end,
            'pause': self.pause_end,
        }
        
    # Properties ###############################################################
    def get_parent_project(self):
        if self._project_stack:
            return self._project_stack[-1]
        else:
            return None
        
    def get_root_project(self):
        if self._project_stack:
            return self._project_stack[0]
        else:
            return self.project
        
    parent_project = property(get_parent_project)
    root_project = property(get_root_project)
    ############################################################################
        
    # Helper functions #########################################################
    def get_project_infos(self, attrs):
        if not attrs:
            raise ProjectFileError('File is broken.')
        
        name = find_attr(attrs, 'name')
        if name is None:
            raise ProjectFileError('Project has no name.')
        elif name == '':
            name = res.UNNAMED
            
        current = find_attr(attrs, 'current')
        if current is None:
            raise ProjectFileError(
                'Attribute "current" missing in "project" element.'
            )
        if current == 'true':
            current = True
        elif current == 'false':
            current = False
        else:
            raise ProjectFileError(
                'Attribute "current" must have the value "true" or "false".'
            )
        
        return name, current
    
    def read_project(self, attrs, cls):
        name, current = self.get_project_infos(attrs)
        self.project = cls(name)
        if current:
            self.root_project.current_project = self.project
    ############################################################################
        
    # Handler for the tags #####################################################
    def projectfile_start(self, attrs):
        if not attrs:
            raise ProjectFileError('No file version found.')

        version = find_attr(attrs, 'version')
        if version is None:
            raise ProjectFileError('No file version found.')
        elif version not in ('0.0', CURRENT_FILE_VERSION):
            raise ProjectFileError(
                'Wrong file version. The found version is {}.'.format(version)
            )
    
    def projectfile_end(self):
        pass
    
    def project_start(self, attrs):
        self.read_project(attrs, timelib.Project)
    
    def project_end(self):
        pass
    
    def subprojects_start(self, attrs):
        self._project_stack.append(self.project)
        self.project = None
    
    def subprojects_end(self):
        self.project = self._project_stack.pop()
    
    def subproject_start(self, attrs):
        self.read_project(attrs, timelib.SubProject)
    
    def subproject_end(self):
        pass
    
    def working_days_start(self, attrs):
        pass
    
    def working_days_end(self):
        pass
    
    def wday_start(self, attrs):
        self.project.working_days.append(timelib.WorkingDay(self.project))
    
    def wday_end(self):
        pass
    
    def working_start(self, attrs):
        pass
    
    def working_end(self):
        pass
    
    def pause_start(self, attrs):
        pass
    
    def pause_end(self):
        pass
    
    def starttime_start(self, attrs):
        pass
    
    def endtime_start(self, attrs):
        pass
    ############################################################################

# Helper functions #############################################################
def find_attr(attrs, name):
    for attr, val in attrs:
        if attr == name:
            return val
    return None
################################################################################

# "Public" functions ###########################################################
def load(path):
    with open(path, 'rb') as f:
        file = f.read().decode('utf_8', 'ignore').strip()
        with ProjectFileReader() as parser:
            try:
                parser.feed(file)
                return parser.project
            except (html.parser.HTMLParseError, ProjectFileError) as exc:
                error(res.FILE_READ_ERROR, exc)
    return None

def save(project, path):
    pass
################################################################################
