#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Jaime Irurzun <jaime.irurzun@gmail.com>
# 

class Group(object):
    
    def __init__(self, name, id=None):
        super(Group, self).__init__()
        self.id = id
        self.name = name
        self._parent = None
        self.children = []
        
    def add_child(self, child):
        child._parent = self
        self.children.append(child)
    
    def set_children(self, children):
        for child in children:
            self.add_child(child) 
        
    def get_full_name(self):
        if self._parent is None:
            return self.name
        else:
            return self._parent.get_full_name() + " > " + self.name

    def __repr__(self):
        return "Group(id = %i, full_name = '%s')" % (
                self.id,
                self.get_full_name()
            )