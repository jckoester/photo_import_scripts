#!/usr/bin/python2
# -*- coding: utf-8 -*-

#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
import subprocess
import argparse
from lib import commonfunc as cf

##defining the options:
parser = argparse.ArgumentParser(description='Rename all files in a folder (or a single file) accourding to a fixed naming scheme creating unique filenames.')

parser.add_argument("path", help="Path of the folder containing the images / path to the image")

parser.add_argument("-s", "--suffix", default="", help="suffix indicating the type of image. (eg ORI for original file, DMA for digital master, PRN for a printer optimzed file (please use PRN_profilename for profiled images))")

parser.add_argument("-f", "--force", action="store_true", help="Force renaming using time if no shuttercount is set.")

parser.add_argument("-y", "--dontask", action="store_true", help="Perform the command without asking for confirmation.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")
parser.add_argument("-d", "--dryrun", action="store_true", help="Simulate only, no renaming done.")

#Processing the arguments
args = parser.parse_args()

#Defaults:
#path = args.path
owner= None
verbose=False
dryrun=False


#Check for verbose mode
if args.verbose:
    verbose=True
    cf.verbose=True

#Check for dryrun mode
print(args.dryrun)
if args.dryrun:
    dryrun=True
    cf.dryrun=True

#Check source folder
if not (os.path.exists(args.path)):
    print("Ordner "+path+" existiert nicht")
    sys.exit(0)

#Check other params if in quiet mode:
if args.dontask and len(args.suffix)==0:
    print("No suffix set. Quitting")
    sys.exit(0)

#Check params in normal / verbose mode:
while len(args.suffix)<3:
    if args.suffix=="q":
        sys.exit(0)
    else:
        outp_text="Suffix hat nicht die korrekte Länge (min. 3 Buchstaben). Das Suffix solle den Bearbeitungsgrad/-typ anzeigen, z.B.\n\t-'ORI' für _ORI_ginal, wie aus der Kamera \n\t-'BEA' für _BEA_rbeitet, z.b. BEA_iphoto = mit iPhoto bearbeitet\n\t-'DMA' für _D_igitales _MA_ster, aus RAW entwickelte Masterdatei\n\t-'PRN' für eine Druckvorstufe, z.B. PRN_UT3D_MPWetzlar für ein für Ultrotone3D TInte auf Monoprint Wetzlar profiliertes und optimiertes Bild.\nBitte Suffix eingeben (q um zu beenden):"
        args.suffix = input( outp_text )

if not args.dontask:
    yn = input( "Bennenne um nach Schema YYYYMMDD_CameraSpecificCounter_"+args.suffix+".EXT\n Bitte bestätigen (j/n)" )
    if not yn == "j":
        print("Abbruch.")
        sys.exit(0)
if verbose:
    print("Starte Umbenennen...")

print(args.force)
procopts=[]
procargs={ 'suffix':args.suffix, 'force':args.force}

#If folder
if os.path.isdir(args.path):
    cf.process_folder(args.path, cf.rename, procopts, procargs)
#If file
elif os.path.isfile(args.path):
    cf.rename(args.path, *procopts, **procargs)

if verbose:
    print("Umbenennen abgeschlossen.")
sys.exit(0)
