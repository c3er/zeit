#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''File Input/Output'''

import html.parser
import html.entities

import timelib

# Version of the table file.
CURRENT_FILE_VERSION = '0.1'

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
                self.tmpdat += '?'

    def handle_entityref(self, name):
        if self.read_data_flag:
            self.tmpdat += html.entities.entitydefs[name]
    ############################################################################
    
class ProjectFileReader(MarkupReaderBase):
    def __init__(self):
        super().__init__()
        #...
        self.starttags = {
            'projectfile': self.projectfile_start
        }
        self.endtags = {
            'projectfile': self.projectfile_end
        }
        
    # Handler for the tags #####################################################
    def projectfile_start(self, attrs):
        pass
    
    def projectfile_end(self):
        pass
    ############################################################################

# "Public" functions ###########################################################
def load(path):
    pass

def save(project, path):
    pass
################################################################################
