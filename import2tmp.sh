#!/bin/bash

tmpdir=/tmp/import/
destdir=/home/jan/Bilder/tmp
EXTENSION=("NEF", "JPG", "jpg", "png")

if [ ! -d $tmpdir ]; then
	mkdir $tmpdir
    echo "Erzeuge temporäres Verzeichnis"
fi



if [ $# == 1 ]; then
    if [ -d "${1}" ]; then
        tmpdir="${1}"
        echo "Importiere Bilder aus Verzeichnis ${1}"
        cd "${tmpdir}"
    else
        echo "Der angegebene Pfad existiert nicht."
        exit
    fi
else
    echo "Importiere Bilder in temporäres Verzeichnis"
    cd "${tmpdir}"
    gphoto2 --get-all-files
fi


echo "Bewege Dateien ans Ziel"

for i in *$extension; do
    if [ -d "${i}" ]; then
        echo "${i} is a directory"
    else
        date_stamp=`exiftool -DateTimeOriginal -d "%Y%m%d" "${i}"`
        year=$(expr substr "`echo $date_stamp`" 22 4)
        month=$(expr substr "`echo $date_stamp`" 26 2)
        day=$(expr substr "`echo $date_stamp`" 28 2)

        if [ ! -d $destdir/$year ]; then
            mkdir $destdir/$year
            echo $destdir/$year
        fi
        if [ ! -d $destdir/$year/$month ]; then
            mkdir $destdir/$year/$month
            echo $destdir/$year/$month
        fi
        if [ ! -d $destdir/$year/$month/$year-$month-$day ]; then
            mkdir $destdir/$year/$month/$year-$month-$day
            echo $destdir/$year/$month/$year-$month-$day
        fi

        new_path=$destdir/$year/$month/$year-$month-$day/$i
    
        mv "${i}" "${new_path}"
    
        echo "Verschiebe $i > $new_path"
    fi
done
