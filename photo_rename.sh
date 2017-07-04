#!/bin/bash

# Owner short sign
own="$1"
# Folder containing the images
dir="$2"

# Check if parameters are complete
if [ -z "$1" ] || [ -z "$2" ] ; then
  echo "Please specify the required parameters."
  exit 1
fi

# Check if folder exists
if [ ! -d "$dir" ]; then
	echo $dir
	echo "Directory does not exist."
	exit 1
fi

# Change working dir
cd "${dir}";

# Extension fix:
rename "jpg" "JPG" *

# Rename all images according to the scheme YYYYMMDD_hhmmss_OW_Model_Shutter.ext
exiftool '-filename<${datetimeoriginal}_'${1}'_${model}_${ShutterCount}%-c_ORI.%e' -d "%Y%m%d_%H%M%S" -q .

# Replace Manufacturer Name in file names
rename 'NIKON ' '' *
# TODO: add other manufacturers here


# Walk through all the files ORI_ALT and BEA suffixes
for file in ./*
do
	#echo $file
	case "$file" in
		*.JPG)	
			#echo "Quite sure this is the original file"
			;;
		*.NEF)
			#echo "This might be an alternative file"
			#echo ${file//NEF/JPG} 
			if [ -f ${file/NEF/JPG} ]
			then
				#echo "Found original JPG, renaming"
				#echo ${file/ORI/ORI_ALT}
				mv $file ${file/ORI/ORI_ALT}
			#else
				#echo "No original JPG found."
			fi
			;;
		# better do not do this automatically
		# this might overwrite a second modfied file
		# Still work to do!
		# Also exiftool might have problems renaming modified files
		# At least give a warning:
		*.TIF)
			echo "WARNING: TIF-File found. Please double check if they are rename correctly.\n"
			#echo "This might be a modified file"
			#echo ${file//TIF/JPG} 
			if [ -f ${file/TIF/JPG} ]
			then
				#echo "Found original JPG, renaming"
				#echo ${file/ORI/BEA}
				mv $file ${file/ORI/BEA}
			#else
				#echo "No original JPG found."
			fi
			;;
		*.PNG)
			echo "WARNING: PNG-File found. Please double check if they are rename correctly.\n"
			#echo "This might be a modified file"
			#echo ${file//PNG/JPG} 
			if [ -f ${file/PNG/JPG} ]
			then
				#echo "Found original JPG, renaming"
				#echo ${file/ORI/BEA}
				mv $file ${file/ORI/BEA}
			#else
				#echo "No original JPG found."
			fi
			;;
		*)	echo "Probably not an image OR invalid extension" ;;
	esac
	
done;

# Output message in the end
printf "$msg"
