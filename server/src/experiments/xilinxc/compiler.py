#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Luis Rodriguez <luis.rodriguez@opendeusto.es>
#


import subprocess
import os


class Compiler(object):
    
    BASE_PATH = ".." + os.sep + ".." + os.sep + "experiments" + os.sep + "xilinxc" + os.sep + "files"
    DEBUG = False
    
    def __init__(self, filespath = BASE_PATH):
        self.filespath = filespath
        if(self.DEBUG):
            print "[Xilinxc Compiler]: Running from " + os.getcwd()
            
    def feed_vhdl(self, vhdl, debugging = False):
        """
        Replaces the local vhdl file contents with the provided code.
        Warning: It will replace the file contents.
        @param vhdl String containing the new VHDL code.
        """
        vhdlpath = self.filespath + os.sep + "base.vhd"
        if(debugging):
            print "[DBG]: Feed_vhdl pretending to replace %s with: " % (vhdlpath)
            print vhdl
        else:
            f = file(vhdlpath, "w")
            f.write(vhdl)
            f.close()
            
    def feed_ucf(self, ucf, debugging = False):
        """
        Replaces the local ucf file contents with the provided ucf.
        Warning: It will replace the file contents.
        @param ucf String containing the new UCF code.
        """
        ucfpath = self.filespath + os.sep + "FPGA_2012_2013_def.ucf"
        if(debugging):
            print "[DBG]: Feed_ucf pretending to replace %s with " % (ucfpath)
            print ucf
        else:
            f = file(ucfpath, "w")
            f.write(ucf)
            f.close()
    
    def synthesize(self):
        process = subprocess.Popen(["xst", "-intstyle", "ise", "-ifn", "base.xst", 
                                    "-ofn", "base.syr"], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.filespath)
        
        so, se = process.communicate()
        
        if(self.DEBUG):
            print so, se
        
        if len(se) > 0 or "ERROR:" in so:
            return False
        
        return True
    
    def ngdbuild(self):
        process = subprocess.Popen(["ngdbuild", "-intstyle", "ise", "-dd", "_ngo", "-nt", "timestamp", "-uc", "FPGA_2012_2013_def.ucf", 
                                    "-p", "xc3s1000-ft256-4", "base.ngc", "base.ngd"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.filespath)

        so, se = process.communicate()
        
        if(self.DEBUG): 
            print so, se

        if len(se) == 0 and "NGDBUILD done." in so:
            return True
        
        return False
    
    def map(self):
        process = subprocess.Popen(["map", "-intstyle", "ise", "-p", "xc3s1000-ft256-4", 
                                    "-cm", "area", "-ir", "off", "-pr", "off", "-c", "100", 
                                    "-o", "base_map.ncd", "base.ngd", "base.pcf"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.filespath)
        
        so, se = process.communicate()
        
        if(self.DEBUG):
            print so, se
        
        if len(se) == 0 and "Mapping completed." in so:
            return True
        
        return False;
        
    def par(self):
        process = subprocess.Popen(["par", "-w", "-intstyle", "ise", "-ol", "high", "-t", "1",
                                    "base_map.ncd", "base.ncd", "base.pcf"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.filespath)
        
        so, se = process.communicate()
        
        if(self.DEBUG):
            print so, se
        
        if len(se) == 0 and "PAR done!" in so:
            return True
        
        return False
    
    def implement(self):
        result = self.ngdbuild()
        if(result):
            result = self.map()
            if(result):
                result = self.par()
                return result
        return False
    
    def generate(self):
        process = subprocess.Popen(["bitgen", "-intstyle", "ise", "-f", "base.ut", 
                                    "base.ncd"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.filespath)
        
        # We use process.wait rather than process.communicate because
        # when bitgen is executed, WebTalk stays running in the background,
        # which causes an error. And there seems to be no way to disable it.
        
        r = process.wait()
        
        if(self.DEBUG):
            print process.stdout.read()
            print process.stderr.read()
        
        if(r == 0):
            return True
        
        return False
    

if __name__ == "__main__":
    
    Compiler.DEBUG = True

    c = Compiler()
    
    print c.synthesize()
    print c.ngdbuild()
    print c.implement()
    print c.generate()
    
    print "Good bye"