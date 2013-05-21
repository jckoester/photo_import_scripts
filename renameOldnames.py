#!/usr/bin/python
# -*- coding: utf-8 -*-

#=================DESCRIPTION IS MISSING!========================================#

#System environment
import sys
import os
import datetime
import subprocess
import argparse
import sqlite3
from lib import commonfunc as cf
from lib import oldnames_db as db

##defining the options:
parser = argparse.ArgumentParser(description='A script for renaming edited raws especially wehre the MakerNotes are missing in the TIF. The scan options scans through a folder for Original files and saves timestamp and shuttercount in a database. The rename option scnas through a folder and renames all files according to the shuttercount values saved in the database.')

parser.add_argument("path", help="Path of the folder containing the images / path to the image")

parser.add_argument("--scan", action="store_true", help="Perform a scan and save to database")
parser.add_argument("--check", action="store_true", help="Look for data in database")

parser.add_argument("-p", "--prefix", default="", help="2 letter prefix indicating the creator")
parser.add_argument("-s", "--suffix", default="", help="suffix indicating the type of image. Should be BEA or DMA for edited files (PRN for a printer optimzed file (please use PRN_profilename for profiled images))")

parser.add_argument("-y", "--dontask", action="store_true", help="Perform the command without asking for confirmation.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")

#Processing the arguments
args = parser.parse_args()


#Defaults:
verbose=False


#Check for verbose mode
if args.verbose:
    verbose=True
    cf.verbose=True
    db.verbose=True

#Check source folder
if not (os.path.exists(args.path)):
    print "Ordner "+path+" existiert nicht"
    sys.exit(0)

if not os.path.exists('oldnames.db'):
    #Create Database
    db.init()

if args.scan:
    procopts=[]
    procargs={}
    #If folder
    if os.path.isdir(args.path):
        cf.process_folder(args.path, db.scan, procopts, procargs)
    #If file
    elif os.path.isfile(args.path):
        db.scan(args.path, procopts, procargs)

if args.check:
    procopts=[]
    procargs={}
    #If folder
    if os.path.isdir(args.path):
        cf.process_folder(args.path, db.check, procopts, procargs)
    #If file
    elif os.path.isfile(args.path):
        db.check(args.path, procopts, procargs)

