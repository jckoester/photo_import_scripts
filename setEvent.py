#!/usr/bin/python
# -*- coding: utf-8 -*-
#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
import subprocess
import argparse
from lib import commonfunc as cf

path = None
event= None

##defining the options:
parser = argparse.ArgumentParser(description='Set event for all images in a folder or a given image file.')

parser.add_argument("path", help="Path of the folder containing the images or path to the image file")
parser.add_argument("-event", help="Name of the event")

parser.add_argument("-y", "--dontask", action="store_true", help="Perform the command without asking for confirmation.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")

#Processing the arguments
args = parser.parse_args()

#Check for verbose mode
if args.verbose:
    verbose=True
    cf.verbose=True

#Check source folder
if not (os.path.exists(args.path)):
    print "Ordner "+args.path+" existiert nicht"
    sys.exit(0)

#Check other params if in quiet mode:
if args.dontask and len(args.event)==0:
    print "No owner set. Quitting."
    sys.exit(0)

#Check event name
if args.event is None or len(args.event) <= 0:
    outp_text = "Kein Projektname angegeben. Bitte eingeben:"
    event_name = raw_input( outp_text )
    args.event = event_name

if not args.dontask:
    yn = raw_input( "Setze Ereignis auf \""+args.event+"\"? (j/n)")
    if not yn == "j":
        print "Abbruch."
        sys.exit(0)
if verbose:
    print "Setze Ereignis-Tag..."

procopts=[]
procargs = {"Event":args.event}


if os.path.isdir(args.path):
    cf.process_folder(args.path, cf.et_write, procopts, procargs)
elif os.path.isfile(args.path):
    cf.et_write(args.path, *procopts, **procargs)
sys.exit(0)

