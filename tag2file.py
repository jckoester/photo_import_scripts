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

def clean_tags(xmppath):
    with exiftool.ExifTool() as et:
        tagslist = et.get_tag('tagslist', xmppath)

    if(tagslist):
        tagslist = [t for t in tagslist if not "_Digikam_root_tag_" in t]
        print tagslist
    
        args={"tagslist":','.join(tagslist)}
        print args
        with exiftool.ExifTool() as et:
            et.set_tags(args, xmppath)
        os.remove(xmppath+"_original")
    else:
        print "Nothing to clean!"
    return

def tags_to_file(filepath, xmppath):
    print filepath
    print xmppath
    
    try:
        subprocess.check_call(["exiftool", "-overwrite_original", "-tagsfromfile", xmppath, filepath])
        os.remove(xmppath)
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
    files=[ f for f in os.listdir(path)  if f[-4:].lower() in photo_exts]

    for f in files:
        #check if image.xmp exists:
        if os.path.exists(os.path.join(path, f+'.xmp')):
            clean_tags(os.path.join(path, f+'.xmp'))
            tags_to_file(os.path.join(path, f), os.path.join(path, f+'.xmp'))
        else:
            if os.path.exists(os.path.join(path, f+'.XMP')):
                clean_tags(os.path.join(path, f+'.xmp'))
                tags_to_file(os.path.join(path, f), os.path.join(path, f+'.XMP'))
            else:
                print "Keine xmp-Metadata für Datei '"+f+"'."

    print "Kopieren abgeschlossen."
else:
    print "Kein Pfad angeben."
    sys.exit(0)
