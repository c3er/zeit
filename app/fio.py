#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''File Input/Output'''

import datetime
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
        self.starttime = None
        self.endtime = None
        self.inworking = False
        self.inpause = False
        
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
        if not name:
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
            
    def read_time(self, attrs):
        year = int(find_attr(attrs, 'year'))
        month = int(find_attr(attrs, 'month'))
        day = int(find_attr(attrs, 'day'))
        hours = int(find_attr(attrs, 'hours'))
        minutes = int(find_attr(attrs, 'minutes'))
        seconds = int(find_attr(attrs, 'seconds'))
        
        if year == month == day == hours == minutes == seconds == -1:
            time = datetime.datetime.today()
        else:
            time = datetime.datetime(year, month, day, hours, minutes, seconds)
            
        return time
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
        self.inworking = True
    
    def working_end(self):
        self.project.current_day.periods.append(
            timelib.Working(
                self.project.current_day, self.starttime, self.endtime
            )
        )
        self.inworking = False
    
    def pause_start(self, attrs):
        self.inpause = True
    
    def pause_end(self):
        self.project.current_day.periods.append(
            timelib.Pause(
                self.project.current_day, self.starttime, self.endtime
            )
        )
        self.inpause = False
    
    def starttime_start(self, attrs):
        self.starttime = self.read_time(attrs)
    
    def endtime_start(self, attrs):
        self.endtime = self.read_time(attrs)
    ############################################################################

# Helper functions #############################################################
def find_attr(attrs, name):
    for attr, val in attrs:
        if attr == name:
            return val
    return None

def write_tag(tag, *args, attrs = None, content = None):
    '''Writes a tag, following the XML syntax.
    
    Parameters:
    - tag: Contains the name of the tag.
    - attrs: A list (or tuple), containing tuples in the form "(attr, val)".
      The first element is the name of the attribute and the second is its
      value.
    - content: Contains the whole content between start and end tag. If its
      value is None, the resulting tag will be a start/end tag.
    
    Returns:
    A string, containing the written tag.
    '''
    output = '<' + tag
    
    if attrs is not None:
        for attr, val in attrs:
            output += ' ' + attr + '="' + val + '"'

    if content is not None:
        output += '>\n' + str(content) + '\n</' + tag + '>\n'
    else:
        output += '/>\n'
    
    return output
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
