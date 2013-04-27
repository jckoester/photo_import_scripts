#!/usr/bin/python
# -*- coding: utf-8 -*-
#=================DESCRIPTION IS MISSING!========================================#

#This script copies all exif, iptc and xmp metadata from a ORIGINALNAME.xmp sidecar to a ORIGINALNAME.RAWEXT.xmp sidecar file
#This is useful if you want to use Bibble5/Corel AfterShotPro alongside with other workflow managemant tool like darktable
#Usage: ./xmpfix.py ORIGINALNAME.RAWEXT
#If you want to use it on all pictures in a directory (including subdirectories) you could use find:
# find /path/to/your/pictures -name ".EXTENSION" -exec ./xmpfix.py {} \;

#Created by Jan Köster <koester_jan@gmx.net>, http://www.cbjck.de
#GitRepo: https://github.com/dasmaeh/xmpfix
#This script is provided "as is" in the hope it helps. No guaranties that ist does waht it is intended to do.
#Use on your own risk.
#=================DESCRIPTION IS MISSING!========================================#
#CAUTION
#This script does currently not import *.RAWEXT.xmp files!

#System environment
import sys
import os
import datetime
#class for manipulating xmp, exif and iptc
import pyexiv2
#
import shutil

#SETTINGS:
file_exts=('.tif','.nef','.jpg','.png', '.xmp')
photo_exts=('.tif','.nef','.jpg','.png')
#minimum length of counter:
n_zfill=3
#target_path for library
#print "Running in TEST MODE"
#target_path="/home/jan/Bilder/TEST"
target_path="/home/jan/Bilder/Originale"
#common project names
project_names=('Zoo', 'Katzen', 'Food', 'ReiseSL')

#uniqify routine
#found here: http://www.peterbe.com/plog/uniqifiers-benchmark
def uniquify(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

#get EXIF date from an image
def getexifdate(path):
    metadata=pyexiv2.ImageMetadata(path)
    metadata.read()
    date=metadata['Exif.Image.DateTime']
    return date.value

path = None
project= None

if len(sys.argv) > 1:
    path = sys.argv[1]
if len(sys.argv) > 2:
    project = sys.argv[2]
if len(sys.argv) > 3:
    startindex = sys.argv[3]
if len(sys.argv) > 4:
    n_zfill=int(sys.argv[4])
#Check source folder
if not (os.path.exists(path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)
#Check target folder:
print "Prüfe Zielverzeichnis..."
if not os.path.exists(target_path):
    print "Zielverzeichnis "+target_path+" nicht verfügbar!"
    sys.exit(0)
else:
    print "OK"

#Check project name
if project is None or len(project) <= 0:
    print "Kein Projektname angegeben. Bitte auswählen oder eingeben:"
    outp_text=str("")
    for i, name in enumerate(project_names):
        outp_text+=str(i+1)+". "+name+" ("+str(i+1)+")\n"
    outp_text+=str(len(project_names)+1)+". Beliebiger Name (direkt eintippen)"
    project_name = raw_input( outp_text )
    print project_name
    if '1' <= project_name <= str(len(project_names)):
        project = project_names[int(project_name)-1]
    else:
        project = project_name
yn = raw_input( "Importiere Bilder in Projekt \""+project+"\"? (j/n)")
if not yn == "j":
    print "Import abgebrochen."
    sys.exit(0)
else:
    print "Importiere..."
        
    #Check if temp path exists
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
        #sort list by exif creation date    
        files.sort(key=lambda f: getexifdate(os.path.join(path, f)))
        #cut extensions
        for i, f in enumerate(files):
            files[i] = os.path.splitext(f)[0]
        # uniqify the list (as combined shots of .jpg and RAW might lead to double entries)
        files_unique=uniquify(files)
        
        #adjust lenght of counter:
        print len(str(len(files)))
        if len(str(len(files)))>n_zfill:
            n_zfill=len(str(len(files)))

        #the renaming:
        #counter
        if len(sys.argv) > 3:
            j=int(startindex)
        else:    
            j=1
        date = None
        for f in files_unique:
            for ext in photo_exts:
                if os.path.exists(os.path.join(path, f+ext.lower())):
                    date=getexifdate(os.path.join(path, f+ext.lower()))
                if os.path.exists(os.path.join(path, f+ext.upper())):
                    date=getexifdate(os.path.join(path, f+ext.upper()))

           # sys.exit(0)
            for ext in  file_exts:
                if os.path.exists(os.path.join(path, f+ext.lower())) or os.path.exists(os.path.join(path, f+ext.upper())):
                    if os.path.exists(os.path.join(path, f+ext.lower())):
                        ext=ext.lower()
                    if os.path.exists(os.path.join(path, f+ext.upper())):
                        ext=ext.upper()
                        
                    name_old = f+ext
                    name_new = project+date.strftime("-%Y-%m-%d-")+ str(j).zfill(n_zfill)+ext
                    
                    #Checking target subfolders
                    target_path_year=os.path.join(target_path,date.strftime("%Y"))
                    if not os.path.exists(target_path_year):
                        print "Erzeuge Verzeichnis "+target_path_year
                        os.makedirs(target_path_year)
                    target_path_month=os.path.join(target_path_year,date.strftime("%m"))
                    if not os.path.exists(os.path.join(target_path_month)):
                        print "Erzeuge Verzeichnis "+target_path_month
                        os.makedirs(target_path_month)
                    target_path_day=os.path.join(target_path_month,date.strftime("%Y-%m-%d-")+project)
                    if not os.path.exists(os.path.join(target_path_day)):
                        print "Erzeuge Verzeichnis "+target_path_day
                        os.makedirs(target_path_day)

                    #The actual process of renaming (and moving)
                    print name_old+" >>> "+name_new
                    if not os.path.exists(os.path.join(target_path_day,name_new)):

                        #os.rename(os.path.join(path,name_old),os.path.join(target_path_day,name_new))
                        shutil.move(os.path.join(path,name_old),os.path.join(target_path_day,name_new))
                    else:
                        print "Datei "+os.path.join(target_path_day,name_new)+" existiert bereits. Datei wird nicht importiert!"

                        
            j+=1
        print "Import abgeschlossen."

        #cleaning up:
        print "Räume auf..."
        try:
            os.rmdir(path)
            print "Verzeichnis "+path+" gelöscht.\n Fertig."
            empty = True
        except OSError:
            empty = False
            print "Verzeichnis "+path+" nicht leer."
   
