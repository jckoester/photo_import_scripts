#!/usr/bin/python
# -*- coding: utf-8 -*-
#=================DESCRIPTION IS MISSING!========================================#

################ ACHTUNG ###################
#-Parameter wurden auf argparse umgestellt.
#-verwendet jetzt die process-folder Prozedur aus lib/commonfunc.py


#System environment
import sys
import os
import datetime
import subprocess
import argparse


#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
#from lib.pyexiftool_settags import exiftool
from lib import commonfunc as cf

#SETTINGS:
#file_exts=('.tif','.nef','.jpg','.png', '.xmp')
#photo_exts=('.tif','.nef','.jpg','.png')
owner_names={"Jan":[u"Jan Köster".encode('utf-8'), u"jan.koester@koester-becker.de".encode('utf-8'), u"http://www.cbjck.de".encode('utf-8'), u"cc-by-sa".encode('utf-8')], "Cornelia":["Cornelia Becker", "cornelia.becker@koester-becker.de", "http://www.cbjck.de", ""]}

##function for doing the work:
def set_owner(path, *args, **kwargs):
    try:
        subprocess.check_call(["exiftool", "-overwrite_original", "-Creator="+kwargs['Creator'], "-CreatorWorkEmail="+kwargs['CreatorWorkEmail'], "-CreatorWorkURL="+kwargs['CreatorWorkURL'], "-Copyright="+kwargs['Copyright'], path])
    except subprocess.CalledProcessError:
        print "Exiftool meldete einen Fehler beim Verarbeiten von '"+path+"'."
    return
##defining the options:
parser = argparse.ArgumentParser(description='Set owner and copyright information for all images in a folder or a single image file.')

parser.add_argument("path", help="Path of the folder containing the images")
parser.add_argument("-owner", help="Name of the copyright owner")
parser.add_argument("-mail", help="Email address of the copyright owner")
parser.add_argument("-web", help="Homepage of the copyright owner")
parser.add_argument("-license", help="License information for the images")

parser.add_argument("-y", "--dontask", action="store_true", help="Perform the command without asking for confirmation.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")

#Processing the arguments
args = parser.parse_args()


path = None
owner= None
verbose=False

#Check for verbose mode
if args.verbose:
    verbose=True
    cf.verbose=True


#Check source folder
if not (os.path.exists(args.path)):
    print "Ordner "+args.path+" existiert nicht"
    sys.exit(0)

#Check other params if in quiet mode:
if args.dontask and len(args.owner)==0:
    print "No owner set. Quitting."
    sys.exit(0)

#Check Owner name
if args.owner is None or len(args.owner) <= 0:
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
        mail = raw_input( outp_text ).decode()
        outp_text=str(len(owner_names)+1)+". Beliebiger Urheber'"+owner+"' (Website eintippen - optional)"
        web = raw_input( outp_text )
        outp_text=str(len(owner_names)+1)+". Beliebiger Urheber '"+owner+"' (Lizenzinformationen eintippen - optional)"
        license = raw_input( outp_text )
else:
    owner = args.owner
    mail = args.mail
    web = args.web
    license = args.license

if not args.dontask:
    yn = raw_input( "Setze Urheber auf\t'"+owner+"'\neMail:\t\t\t'"+mail+"'\nWebsite:\t\t'"+web+"'\nLizenz:\t\t\t'"+license+"'\n Bitte bestätigen (j/n)" )
    if not yn == "j":
        print "Abbruch."
        sys.exit(0)
if verbose:
    print "Setze Urheber-Daten..."

procopts=[]
procargs = {"Creator":owner, "CreatorWorkEmail":mail, "CreatorWorkURL":web, "Copyright":license}

if os.path.isdir(args.path):
    cf.process_folder(args.path, set_owner, procopts, procargs)
elif os.path.isfile(args.path):
    set_owner(args.path, *procopts, **procargs)
sys.exit(0)

