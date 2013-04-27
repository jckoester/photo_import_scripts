#!/usr/bin/python
# -*- coding: utf-8 -*-
#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
from lib.pyexiftool_settags import exiftool

#SETTINGS:
file_exts=('.tif','.nef','.jpg','.png', '.xmp')
photo_exts=('.tif','.nef','.jpg','.png')

def set_event(filepath, eventname):
    args={"event":eventname}
    print filepath
    with exiftool.ExifTool() as et:
        et.set_tags(args, filepath)
    return

path = None
event= None

if len(sys.argv) > 1:
    path = sys.argv[1]
if len(sys.argv) > 2:
    event = sys.argv[2]

#Check source folder
if not (os.path.exists(path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)

#Check event name
if event is None or len(event) <= 0:
    outp_text = "Kein Projektname angegeben. Bitte eingeben:"
    event_name = raw_input( outp_text )
    event = event_name
yn = raw_input( "Setze Ereignis auf \""+event+"\"? (j/n)")
if not yn == "j":
    print "Abbruch."
    sys.exit(0)
else:
    print "Setze Ereignis-Tag..."
        
#Check if path exists
if os.path.exists(path):
    #rename all tiff to tif
    files_tiff = [ f for f in os.listdir(path)  if f[-4:].lower() == 'tiff']
    if len(files_tiff)>0:
        print "Umbenennen von *.tiff nach *.tif"
        for t in files_tiff:       
            name=os.path.splitext(t)[0]
            os.rename(os.path.join(path, t), os.path.join(path,name+".tif"))
            
    #create a list of file names from image files in our folder
    files=[ f for f in os.listdir(path)  if f[-4:].lower() in photo_exts]
    for f in files:
        if os.path.exists(os.path.join(path, f)):
            set_event(os.path.join(path, f), event)
        else:
            print "Datei verschwunden: '"+f+ext+"'."
    print "Ereignis setzen abgeschlossen."
else:
    print "Kein Pfad angeben."
    sys.exit(0)
