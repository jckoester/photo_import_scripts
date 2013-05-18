#!/usr/bin/python
# -*- coding: utf-8 -*-
#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime

del_exts=('.xmp', '_original')
path = None

if len(sys.argv) > 1:
    path = sys.argv[1]

#Check if path exists
if os.path.exists(path):
            
    #create a list of file names from files to delete in our folder
    files=[ f for f in os.listdir(path)  if f[-4:].lower() in del_exts or f[-9:].lower() in del_exts ]
    for f in files:
        os.remove(path+f)        
    print "Aufräumen abgeschlossen."
else:
    print "Kein Pfad angeben."
    sys.exit(0)
