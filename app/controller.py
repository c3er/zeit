#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timelib
from misc import *

class Controller:
    def __init__(self, state_handler):
        self.state_handler = state_handler
        #...
    
    def update(self):
        self.state_handler(self)
        #...
