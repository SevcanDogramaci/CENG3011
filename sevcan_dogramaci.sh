#!/bin/bash

# This script does the followings:
# It takes only one file url as an input
# It downloads zipped file from url and extracts it 
#
# Forms a new file "SV_del.bed" with rows including :
# => <DEL> in column 5
# => RPSUP>10 inside column 8
# => |START-END|>1000 and END>START => END-START>1000
# where START in column 2, END in column 8 from extracted file
# Sorts it based on first column 1 then column 2 
#
# Removes extracted file
#
# Forms a new file "size_distribution.txt" from "SV_del.bed" by 
# => finding occurrences of each SV size, SV size = END-START
# => storing # of occurrences in an array called SV_sizes
# => printing SV size and its occurrence number 
# => sorting based on SV size


file_url="$1"
zipped_file_name=$(basename "$file_url")
extracted_file_name="${zipped_file_name%.*}"
del_file_name="SV_del.bed"
size_file_name="size_distribution.txt"

exit_with_error()
{
    echo "$1" 1>&2
    exit 1
}


#check exactly one input file name with .gz extension taken 
if [[ "$#" -ne "1" || ${file_url##*.} != "gz" ]];then
    exit_with_error "Invalid input !"
else
    echo "$file_url"
fi


#download and extract file
wget "$file_url"

if [ -e "$zipped_file_name" ];then
    echo "Extracting $extracted_file_name..."
    gunzip  $zipped_file_name
else 
    exit_with_error "$zipped_file_name not found in current directory !"
fi


#check if extraction is successful
if [ $? -eq 0 ];then
    echo "Extraction successful !"
else
    exit_with_error "Extraction failed !"
fi


#form $del_file_name 
# => including <DEL>
# => RPSUP>10
# => |START-END|>1000 and END>START => rows with END-START>1000
awk '{
split($8,INFO,";"); 
split(INFO[1],END_COOR,"="); 
split(INFO[3],RPSUP,"="); 

if($5 == "<DEL>" && RPSUP[2]>10 && (END_COOR[2]-$2>1000)) 
    print $1, $2, END_COOR[2]
}' $extracted_file_name | sort -k1,1 -k2,2n -V > $del_file_name 



#form $size_file_name and remove extracted file
declare -A SV_sizes 

if [ $? -eq 0 ];then
    echo "$del_file_name is created succesfully !"
    rm $extracted_file_name
    awk '{
    if(($3-$2) in SV_sizes) 
    	SV_sizes[$3-$2]+=1; 
    else 
	SV_sizes[$3-$2]=1
    } END {
    for(i in SV_sizes) 
	print i "\t" SV_sizes[i] 
    }' $del_file_name | sort -n -k1 > $size_file_name
else
    exit_with_error "$del_file_name could not created !"
fi


if [ $? -eq 0 ];then
    echo "$size_file_name is created succesfully"
else
    exit_with_error "$size_file_name could not created !"
fi
