#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''File Input/Output'''

import datetime
import html.parser
import html.entities

import timelib
import res

# Use this to mark incompatibilities.
CURRENT_FILE_VERSION = '0.1'

class ProjectFileError(Exception):
    pass

class MarkupReaderBase(html.parser.HTMLParser):
    '''XXX Must be documented!
    '''
    def __init__(self):
        super().__init__()
        self.tmpdat = ''
        self._read_data_flag = False
        self.starttags = self._fill_tagdict('starttag')
        self.endtags = self._fill_tagdict('endtag')

    # Needed to use it with a "with" statement #################################
    def __enter__(self):
        return self.__class__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    ############################################################################
        
    # Properties ###############################################################
    @property
    def read_data_flag(self):
        return self._read_data_flag
    
    @read_data_flag.setter
    def read_data_flag(self, val):
        self._read_data_flag = val
        self.tmpdat = ''
    ############################################################################
    
    def _fill_tagdict(self, tag_marker):
        '''Helper method to fill the dictionaries for handling the tags.
        
        The dictionary that is returned has the following form:
        {<tag-name1>: handler1,
         <tag-name2>: handler2,
         ...
         <tag-nameN>: handlerN}
        
        A handler must be named with the following schema:
        <value of tag_marker>_<name of tag>
        Every method which is named after this schema will be added to the
        dictionary as mentioned above.
        '''
        tagdict = {}
        attrs = dir(self)
        
        for attr in attrs:
            if attr.startswith(tag_marker):
                # It shall be possible to use underlines in tag names.
                tmp = attr.split('_')[1:]
                tag_name = '_'.join(tmp)
                
                tagdict[tag_name] = getattr(self, attr)
                
        return tagdict
    
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
        
    # Properties ###############################################################
    @property
    def parent_project(self):
        if self._project_stack:
            return self._project_stack[-1]
        else:
            return None
        
    @property
    def root_project(self):
        if self._project_stack:
            return self._project_stack[0]
        else:
            return self.project
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
    def starttag_projectfile(self, attrs):
        if not attrs:
            raise ProjectFileError('No file version found.')

        version = find_attr(attrs, 'version')
        if version is None:
            raise ProjectFileError('No file version found.')
        elif version not in ('0.0', CURRENT_FILE_VERSION):
            raise ProjectFileError(
                'Wrong file version. The found version is {}.'.format(version)
            )
    
    def endtag_projectfile(self):
        pass
    
    def starttag_project(self, attrs):
        self.read_project(attrs, timelib.Project)
    
    def endtag_project(self):
        pass
    
    def starttag_subprojects(self, attrs):
        self._project_stack.append(self.project)
        self.project = None
    
    def endtag_subprojects(self):
        self.project = self._project_stack.pop()
    
    def starttag_subproject(self, attrs):
        self.read_project(attrs, timelib.SubProject)
    
    def endtag_subproject(self):
        pass
    
    def starttag_working_days(self, attrs):
        pass
    
    def endtag_working_days(self):
        pass
    
    def starttag_wday(self, attrs):
        self.project.working_days.append(timelib.WorkingDay(self.project))
    
    def endtag_wday(self):
        pass
    
    def starttag_working(self, attrs):
        self.inworking = True
    
    def endtag_working(self):
        self.project.current_day.periods.append(
            timelib.Working(
                self.project.current_day, self.starttime, self.endtime
            )
        )
        self.inworking = False
    
    def starttag_pause(self, attrs):
        self.inpause = True
    
    def endtag_pause(self):
        self.project.current_day.periods.append(
            timelib.Pause(
                self.project.current_day, self.starttime, self.endtime
            )
        )
        self.inpause = False
    
    def starttag_starttime(self, attrs):
        self.starttime = self.read_time(attrs)
    
    def starttag_endtime(self, attrs):
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
