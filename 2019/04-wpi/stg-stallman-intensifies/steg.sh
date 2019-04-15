#!/bin/bash

file_name=${file%.*}

file $1
read -p "Hit enter:"

exiftool $1
read -p "Hit enter:"

binwalk $1
read -p "Hit enter:"

steghide info $1 -p ""
echo pass: ${file_name}
steghide info $1 -p "${file_name}"
while read line
do
    echo pass: $line
    steghide info $1 -p "$line"
done < ./wordlist.txt
read -p "Hit enter:"

strings $1