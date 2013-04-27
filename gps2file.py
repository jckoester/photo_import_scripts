#!/usr/bin/python
# -*- coding: utf-8 -*-

#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
import subprocess
#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
from lib.pyexiftool_settags import exiftool
#
import shutil

#SETTINGS:
file_exts=('.tif','.nef','.jpg','.png', '.xmp')
photo_exts=('.tif','.nef','.jpg','.png')
#minimum length of counter:
n_zfill=3

def tags_to_file(filepath, xmppath):
    print filepath
    print xmppath
    
    try:
        subprocess.check_call(["exiftool", "-overwrite_original", "-tagsfromfile", xmppath, filepath])
    except subprocess.CalledProcessError:
        print "Exiftool meldete einen Fehler beim Verarbeiten von '"+xmppath+"'."
    return

#Path should be an argument
if len(sys.argv) > 1:
    path = sys.argv[1]

#Check folder
if not (os.path.exists(path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)

print "Starte Kopiere von xmp zu Bild..."
      
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
    files=[ f for f in os.listdir(path)  if f[-4:].lower() in ['.xmp']]

    for i, f in enumerate(files):
        files[i] = os.path.splitext(f)[0]

    for f in files:
        for ext in photo_exts:
            #check if image.ext exists:
            if os.path.exists(os.path.join(path, f+ext.lower())):
                tags_to_file(os.path.join(path, f+ext.lower()), os.path.join(path, f+'.xmp'))
            else:
                if os.path.exists(os.path.join(path, f+ext.upper())):
                    tags_to_file(os.path.join(path, f+ext.upper()), os.path.join(path, f+'.xmp'))
                else:
                    print "Keine xmp-Metadata für Datei '"+f+ext+"'."

    print "Kopieren abgeschlossen."
else:
    print "Kein Pfad angeben."
    sys.exit(0)
