#!/usr/bin/python
# -*- coding: utf-8 -*-

#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
#class for manipulating xmp, exif and iptc
import pyexiv2
#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
from lib.pyexiftool_settags import exiftool
#
import shutil

#SETTINGS:
file_exts=('.tif','.nef','.jpg','.png', '.xmp')
photo_exts=('.tif','.nef','.jpg','.png')
#minimum length of counter:
n_zfill=3

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

#get EXIF value from an image
def getexifvalue(path, args):
#    args={name}

    with exiftool.ExifTool() as et:
        value = et.get_tags(args, filepath)
    return value


#rename all tiffs
def rename_tiffs():
    files_tiff = [ f for f in os.listdir(path)  if f[-4:].lower() == 'tiff']
    if len(files_tiff)>0:
        print "Umbenennen von *.tiff nach *.tif"
        for t in files_tiff:       
            name=os.path.splitext(t)[0]
            os.rename(os.path.join(path, t), os.path.join(path,name+".tif"))
    return


path = None
owner= None

if len(sys.argv) > 1:
    path = sys.argv[1]
if len(sys.argv) > 2:
    owner = sys.argv[2]

#Check folder
if not (os.path.exists(path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)

owner_shorts={"Jan":"JK", "Cornelia":"CB"}

#Check Owner sign
if owner is None or len(owner) <= 0:
    print "Kein Kürzel angegeben. Bitte auswählen oder eingeben:"
    outp_text=str("")
    owners=[]
    for i, name in enumerate(owner_shorts):
        owners.append(name)
        outp_text+=str(i+1)+". "+name+" ("+str(i+1)+")\n"
    outp_text+=str(len(owner_shorts)+1)+". Beliebiger Urheber (Kürzel eintippen)"
    owner_name = raw_input( outp_text )

    print owner_name
    if '1' <= owner_name <= str(len(owner_shorts)):
        owner=owner_shorts[owners[int(owner_name)-1]]
    else:
        owner = owner_name
        
yn = raw_input( "Setze Kürzel auf\t'"+owner+"'\n Bitte bestätigen (j/n)" )
if not yn == "j":
    print "Abbruch."
    sys.exit(0)
else:
    print "Starte Umbenennen..."
      
#Check if path exists
if os.path.exists(path):
    #rename all tiff to tif
    rename_tiffs()
            
    #create a list of file names from image files in our folder
    files=[ f for f in os.listdir(path)  if f[-4:].lower() in photo_exts]
    #sort list by exif creation date    
    #files.sort(key=lambda f: getexifdate(os.path.join(path, f)))
    #cut extensions
    for i, f in enumerate(files):
        files[i] = os.path.splitext(f)[0]
    # uniqify the list (as combined shots of .jpg and RAW might lead to double entries)
    files_unique=uniquify(files)
    
    #rename:
    #walk through all files:
    for f in files_unique:
        #walk through all exts
        for ext in photo_exts:
            #reset filepath
            filepath=False
            if os.path.exists(os.path.join(path, f+ext.lower())):
                filepath=os.path.join(path, f+ext.lower())
            if os.path.exists(os.path.join(path, f+ext.upper())):
                filepath=os.path.join(path, f+ext.upper())

            if(filepath):
                #The naming schema depends on the camera, so first find out which cam has taken the pic:
                values = getexifvalue(filepath, {'DateTimeOriginal', 'Model', 'ShutterCount', 'SerialNumber'} )

                if('EXIF:Model' in values):
                    date=values['EXIF:DateTimeOriginal']
                    date=datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
                    camera=values['EXIF:Model']
#                    serialno=values['MakerNotes:SerialNumber']
#                    if(values['EXIF:Model']=='NIKON D70'):
#                        serialno=serialno[4:12]

                    if(values['EXIF:Model'][:5]=='NIKON'):
                        shuttercount=values['MakerNotes:ShutterCount']
                        
                        camera=values['EXIF:Model'][6:]

                        name_new=owner+"_"+date.strftime("%Y%m%d")+"_"+camera+"_"+str(shuttercount).zfill(6)+"_ORI"+ext.upper()
                    else:
                        c=0
                        name_new=owner+"_"+date.strftime("%Y%m%d")+"_"+camera+"_"+date.strftime("%H%M%S")+"_"+str(c)+"_ORI"+ext.upper()
                        while(os.path.exists(name_new)):
                            c+=1
                            name_new=owner+"_"+date.strftime("%Y%m%d")+"_"+camera+"_"+date.strftime("%H%M%S")+"_"+str(c)+"_ORI"+ext.upper()
 
                    name_old= f+ext
                    print name_old+" >> "+name_new
                    shutil.move(filepath,os.path.join(path,name_new))
                    
                else:
                    print "No Camera Model set in file "+f+"."+ext+". Skipping file."

    print "Umbenennen abgeschlossen."

