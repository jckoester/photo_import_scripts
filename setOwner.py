#!/usr/bin/python
# -*- coding: utf-8 -*-

# DESCRIPTION ==================================================================
# A python script to set owner/creator related metadata for photos based on
# a configuration file. Multiple options can be configured and selected.
# The script will the write any option of the selected section into the image
# file(s). It is intended to be used for creator related information (hence
# the name) but not limited to those. Basically you can use it write any set of
# metadata to your image file(s) you like.

# USAGE ========================================================================
# Use the script on a single file or a directory:
# setOwner.py <FILE>
# you will be asked whih value from the config file you want to use
# (if there are multiple)
# OR
# setOwner.py -section SECT <FILE>
# to specify the section from the config file.

# CHANGELOG ====================================================================
# 0.5 (27th Dec 2015) partly rewritten, support for config files added

# TODO =========================================================================
# - Try interpolating options (references in the config file)
# - Rename, as not only owner data can be written
# - Add a license to the file
# - Write documentation


#System environment
import sys
import os
import datetime
import subprocess
import argparse
import configparser

#exiftool bindings for python (git://github.com/smarnach/pyexiftool.git)
#from lib.pyexiftool_settags import exiftool
from lib import commonfunc as cf

# Procedure for writing the metadata
def set_owner(path, *args, **kwargs):
    try:
        #subprocess.check_call(["exiftool", "-overwrite_original", "-Creator="+kwargs['Creator'], "-CreatorWorkEmail="+kwargs['CreatorWorkEmail'], "-CreatorWorkURL="+kwargs['CreatorWorkURL'], "-Copyright="+kwargs['Copyright'], path])
        subprocess.check_call(["exiftool", "-overwrite_original", *args, path])
    except subprocess.CalledProcessError:
        print("Exiftool meldete einen Fehler beim Verarbeiten von '"+path+"'.")
    return

# Read the configuration file:
#config = configparser.ConfigParser()
config = configparser.RawConfigParser()
config.optionxform = lambda option: option
if (os.path.exists(os.path.join(os.path.dirname(__file__), 'owner.cfg'))):
    config.read(os.path.join(os.path.dirname(__file__), 'owner.cfg'))
else:
    config.read(os.path.join(os.path.dirname(__file__), 'owner_example.cfg'))
# Defining the options:
parser = argparse.ArgumentParser(description='Set owner and copyright information for all images in a folder or a single image file.')
parser.add_argument("file", help="Path of the folder containing the images")
parser.add_argument("-section", help="Name of the copyright owner, has to be defined as a section in the config file")

#Processing the arguments
args = parser.parse_args()

# Checking if file exists
if not (os.path.exists(args.file)):
    print("Path "+args.file+" does not exist")
    sys.exit(0)

# Check if owner section is set, else print a selection
if args.section is None or len(args.section) <= 0:
    print("No owner selected. Please choose from the options below:")
    outp_text = ""
    for i,name in enumerate(config.sections()):
        outp_text+=str(i+1)+". "+name+" ("+str(i+1)+")\n"
    maxnum = i+2
    #outp_text+=str(maxnum)+". Beliebiger Urheber (Name eintippen)"
    # Printout text and read input
    section_string = input( outp_text )

    if '1' <= section_string <= str(maxnum):
        index = config.sections()[int(section_string)-1]
    else:
        print("The section you've selected does not exist")
        sys.exit(0)
else:
    print("Section selected. See data below:")
    index = args.section

# Print out the configured values and ask before writing:
print("Going to write the following metadata:")

data = []
for key,value in config.items(index):
    print(key+": "+value)
    data.append("-"+key+"="+value)

proceed = input("Proceed? (y/n)")
if proceed == 'y':
    procopts=data
    procargs={}

    if os.path.isdir(args.file):
        cf.process_folder(args.file, set_owner, procopts, procargs)
    elif os.path.isfile(args.file):
        set_owner(args.file, *procopts, **procargs)
    sys.exit(0)
else:
    print("Aborting")
    sys.exit(0)

sys.exit(0)
