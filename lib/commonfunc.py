#!/usr/bin/python
# -*- coding: utf-8 -*-
##Imports
import sys
import os
import subprocess
import datetime
import shutil
import re
#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyexiftool_settags/'))

#from pyexiftool_settags import exiftool
import exiftool
#Global vars
file_exts=('.tif','.nef','.jpg','.png', '.xmp', 'xcf')
photo_exts=('.tif','.nef','.jpg','.png', 'xcf')
verbose=False
dryrun=False

#Erorr handling
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class PathError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

#get EXIF value from an image
def getexifvalue(path, args):
#    args={name}

    with exiftool.ExifToolHelper() as et:
        value = et.get_tags(path, args)
    return value

def rename_tiffs(path):
    #rename all tiff to tif
    files_tiff = [ f for f in os.listdir(path)  if f[-4:].lower() == 'tiff']
    if len(files_tiff)>0:
        print("Umbenennen von *.tiff nach *.tif")
        for t in files_tiff:
            name=os.path.splitext(t)[0]
            os.rename(os.path.join(path, t), os.path.join(path,name+".tif"))
    return

def et_write(path, *args, **kwargs):

    if args:
        optstr="-"
        optstr+=' -'.join(args)+" "
    else:
        optstr=""

    argsstr=""
    for k in kwargs.keys():
        argsstr+="-"+k+"="+kwargs[k]+" "

    try:
        if optstr:
            subprocess.check_call(["exiftool", "-overwrite_original", optstr, argsstr, path])
        else:
            subprocess.check_call(["exiftool", "-overwrite_original", argsstr, path])
    except subprocess.CalledProcessError:
        print("Exiftool meldete einen Fehler beim Verarbeiten von '"+path+"'.")
    return

def rename(path, *args, **kwargs):
    #check if path exists:
    if not os.path.exists(path):
        print("Datei "+path+" existiert nicht.")

    name_old, ext = os.path.splitext(path)
    folderpath=os.path.dirname(path)

    date=False
    camera=False
    shuttercount=False
    name_new_start=False
    name_new_end=False

    filename=os.path.basename(path)

    #Check for alternative JPG
    if kwargs['suffix']=='ORI' and ext=='.NEF' and os.path.exists(name_old+'.JPG'):
        kwargs['suffix']='ORI_ALT'

    #Get exif information:
    values = getexifvalue(path, {'DateTimeOriginal','ModifyDate', 'Model', 'ShutterCount', 'ImageNumber', 'SerialNumber', 'FileNumber'} )
    values=values[0]

    if('EXIF:Model' in values):
        if('EXIF:DateTimeOriginal' in values):
            date=values['EXIF:DateTimeOriginal']
            date=datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
        else:
            date=values['EXIF:ModifyDate']
            date=datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
        camera=values['EXIF:Model']
        name_new_start=date.strftime("%Y%m%d-%H%M%S")+"_"
        name_new_end="_"+kwargs['suffix']+ext.lower()

        if(values['EXIF:Model'][:5]=='NIKON'):
             camera=values['EXIF:Model'][6:]

        if(values['EXIF:Model'][:5]=='Canon'):
            camera=values['EXIF:Model'][6:]
            camera=camera.replace(" ", "")

        if(values['EXIF:Model']=='Pre'):
            camera="PalmPre"

        if(values['EXIF:Model'][:5]=='NIKON' and not 'MakerNotes:ShutterCount' in values.keys()	):
            if('XMP:ImageNumber' in values.keys()):
                shuttercount=values['XMP:ImageNumber']
                name_new_start+=camera+"_"+str(shuttercount).zfill(6)
            else:
                if verbose:
                    print("Kein Wert für ShutterCount gefunden. Überspringe Datei %s." % path)
                    if(not kwargs['force']):
                        return
                else:
                    name_new_start+=camera+"_"+date.strftime("%H%M%S")+"_"
                    c=0
                    while(os.path.exists(os.path.join(folderpath,name_new_start+str(c)+name_new_end))):
                        c+=1
                        name_new_start+=str(c)

        elif(values['EXIF:Model'][:5]=='NIKON'):
            shuttercount=values['MakerNotes:ShutterCount']
            camera=values['EXIF:Model'][6:]
            name_new_start+=camera+"_"+str(shuttercount).zfill(6)
            # print(name_new_start)
        elif(values['EXIF:Model'][:5]=='Canon' and values['MakerNotes:FileNumber']):
            name_new_start+=camera+"_"+str(values['MakerNotes:FileNumber'])
        else:
            name_new_start+=camera+"_"+date.strftime("%H%M%S")+"_"
            c=0
            while(os.path.exists(os.path.join(folderpath,name_new_start+str(c)+name_new_end))):
                c+=1
#                name_new_start+=camera+"_"+date.strftime("%H%M%S")+"_"+str(c)
            name_new_start+=str(c)


    else:
        if verbose:
            print("Kein Kameramodell in EXIF gespeichert. Umbenennen fehlgeschlagen für Datei: "+path)

    if(re.search('(BEA)', kwargs['suffix'])):
            c=0
            name_new_end="_"+kwargs['suffix']+"_" + str(c)+ext.lower()
            while(os.path.exists(os.path.join(folderpath, name_new_start+name_new_end))):
                c+=1
                name_new_end="_"+kwargs['suffix']+"_"+str(c)+ext.lower()

    if name_new_end and name_new_start:
        name_new=name_new_start+name_new_end
        if verbose:
            print("Benenne um: "+os.path.basename(path)+" >> "+name_new)
        if not dryrun:
            shutil.move(path,os.path.join(folderpath,name_new))
        else: 
            print("Simulation! Es wurde keine Datei umbenannt.")

        if os.path.exists(name_old+'.xmp'):
            name_new_end_xmp="_"+kwargs['suffix']+".xmp"
            name_new_xmp=name_new_start+name_new_end_xmp
            xmppath = path.replace(ext, ".xmp")
        if os.path.exists(name_old+'.XMP'):
            name_new_end_xmp="_"+kwargs['suffix']+".xmp"
            name_new_xmp=name_new_start+name_new_end_xmp
            xmppath = path.replace(ext, ".XMP")
        
        if xmppath:
            if verbose:
                print("Bennene xmp-Sidecar um: "+ os.path.basename(xmppath)+" >> "+name_new_xmp)
            if not dryrun:
                shutil.move(xmppath,os.path.join(folderpath,name_new_xmp))
    else:
        if verbose:
            print("Umbennennen fehlgeschlagen für %s" % path)
    return


#apply procfun with arguments in procargs on each file in path
def process_folder(path, procfun, procargs, prockwargs):
    #Check if path exists
    if os.path.exists(path):
        if verbose:
            print("Verarbeite Ordner "+path)
        rename_tiffs(path)

        files=[ f for f in os.listdir(path)  if f[-4:].lower() in photo_exts]
        for f in files:
            if os.path.exists(os.path.join(path, f)):
                if verbose:
                    print("Verarbeite Datei '"+f+"'.")
                #print procfun
                procfun(os.path.join(path, f), *procargs, **prockwargs)
            else:
                print("Datei verschwunden: '"+f+ext+"'.")
        return
    else:
        raise PathError(path, "Pfad existiert nicht")
    return
