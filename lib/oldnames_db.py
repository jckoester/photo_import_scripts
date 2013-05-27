#!/usr/bin/python
# -*- coding: utf-8 -*-
##Imports
import os
import subprocess
import datetime
import shutil
import re
import sqlite3
import commonfunc as cf
#class for manipulating xmp, exif and iptc
#import pyexiv2
#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
from pyexiftool_settags import exiftool
#Global vars
file_exts=('.tif','.nef','.jpg','.png', '.xmp')
photo_exts=('.tif','.nef','.jpg','.png')
verbose=False


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

def init():
    conn = sqlite3.connect('oldnames.db')
    #init
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE oldnames (oldname, timestamp, camera, shuttercount)''')

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return

def scan(path):
    conn = sqlite3.connect('oldnames.db')
    c = conn.cursor()

    #check if path exists:
    if not os.path.exists(path):
        print "Datei "+path+" existiert nicht."

    #Get Filename
    filename = os.path.basename(path)

    #Get exif information:
    values = cf.getexifvalue(path, {'DateTimeOriginal', 'Model', 'ShutterCount', 'SerialNumber'} )

    if('EXIF:Model' in values):
        date=values['EXIF:DateTimeOriginal']
        date=datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
        camera=values['EXIF:Model']
        
        if(values['EXIF:Model'][:5]=='NIKON'):
             camera=values['EXIF:Model'][6:]

        if(values['EXIF:Model'][:5]=='NIKON' and not 'MakerNotes:ShutterCount' in values.keys()	):
            #Setze ShutterCount auf leeren String:
            shuttercount=""

        elif(values['EXIF:Model'][:5]=='NIKON'):
            shuttercount=values['MakerNotes:ShutterCount']
            camera=values['EXIF:Model'][6:]
        else:
            if verbose:
                print "Für Kamera "+camera+" wurde keine Prozedur definiert."
            return
        if shuttercount:
            print date, camera, shuttercount
            #Check if dataset already in db:
            t=(filename, date, camera, shuttercount)
            c.execute("SELECT * FROM oldnames WHERE oldname = ? AND timestamp = ? AND   camera = ? AND shuttercount = ?", t )
            if not c.fetchone():
                if verbose:
                    print "Speichere %s für Datei %s." % (shuttercount, path)
                c.execute("INSERT INTO oldnames VALUES (?,?,?,?)", t)
                conn.commit()
                conn.close()
            else:
                if verbose:
                    print "%s aus Datei %s schon gespeichert." % (shuttercount, path)
        else:
            print "Kein ShutterCount in EXIF gespeichert. Datei: "+path+" wurde übersprungen."

    else:
        print "Kein Kameramodell in EXIF gespeichert. Datei: "+path+" wurde übersprungen."

    return

def get_shuttercount(oldname):
    conn = sqlite3.connect('oldnames.db')
    c = conn.cursor()

    #Look in database:
    t=(oldname, )
    if verbose:
        print "Datenbank-Suche nach %s %s" % t
    c.execute("SELECT shuttercount FROM oldnames WHERE oldname = ?", t )

    shuttercount=c.fetchone()
    if not shuttercount:
        if verbose:
            print "Keine Daten gefunden."
            return False
    else:
        if verbose:
            print "ShutterCount %s zu %s gefunden." % (shuttercount[0], oldname)
        return shuttercount[0]

def check(path, *args, **kwargs):
    #check if path exists:
    if not os.path.exists(path):
        print "Datei "+path+" existiert nicht."
    #Get Filename
    filename = os.path.basename(path)

    return get_shuttercount(filename)
    
