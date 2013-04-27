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
owner_names={"Jan":['Jan Köster', "jan.koester@koester-becker.de", "http://www.cbjck.de", "cc-by-sa"], "Cornelia":["Cornelia Becker", "cornelia.becker@koester-becker.de", "http://www.cbjck.de", ""]}

def set_owner(filepath, owner, mail="", web="", license=""):
    args={"Creator":owner.decode('utf-8'),"CreatorWorkEmail":mail.decode('utf-8'),"CreatorWorkURL":web.decode('utf-8'),"copyright":license.decode('utf-8')}
    print filepath
    with exiftool.ExifTool() as et:
        et.set_tags(args, filepath)
    return

path = None
owner= None


if len(sys.argv) > 1:
    path = sys.argv[1]
if len(sys.argv) > 2:
    owner = sys.argv[2]
if len(sys.argv) > 3:
    mail = sys.argv[3]
if len(sys.argv) > 4:
    web = sys.argv[4]
if len(sys.argv) > 5:
    license = sys.argv[5]


#Check source folder
if not (os.path.exists(path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)

#Check Owner name
if owner is None or len(owner) <= 0:
    print "Kein Urheber angegeben. Bitte auswählen oder eingeben:"
    outp_text=str("")
    owners=[]
    for i, name in enumerate(owner_names):
        owners.append(name)
        outp_text+=str(i+1)+". "+name+" ("+str(i+1)+")\n"
    outp_text+=str(len(owner_names)+1)+". Beliebiger Urheber (Name eintippen)"
    owner_name = raw_input( outp_text )

    print owner_name
    if '1' <= owner_name <= str(len(owner_names)):
        data=owner_names[owners[int(owner_name)-1]]
        owner=data[0]
        mail=data[1]
        web=data[2]
        license=data[3]
        
    else:
        owner = owner_name
        outp_text=str(len(owner_names)+1)+". Beliebiger Urheber'"+owner+"' (eMail-Adresse eintippen - optional)"
        mail = raw_input( outp_text )
        outp_text=str(len(owner_names)+1)+". Beliebiger Urheber'"+owner+"' (Website eintippen - optional)"
        web = raw_input( outp_text )
        outp_text=str(len(owner_names)+1)+". Beliebiger Urheber '"+owner+"' (Lizenzinformationen eintippen - optional)"
        license = raw_input( outp_text )
        
yn = raw_input( "Setze Urheber auf\t'"+owner+"'\neMail:\t\t\t'"+mail+"'\nWebsite:\t\t'"+web+"'\nLizenz:\t\t\t'"+license+"'\n Bitte bestätigen (j/n)" )
if not yn == "j":
    print "Abbruch."
    sys.exit(0)
else:
    print "Setze Urheber-Daten..."
        
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
            set_owner(os.path.join(path, f), owner, mail, web, license)
        else:
            print "Datei verschwunden: '"+f+ext+"'."
    print "Urheber setzen abgeschlossen."
else:
    print "Kein Pfad angeben."
    sys.exit(0)
