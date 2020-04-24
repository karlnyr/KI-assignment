#!/bin/bash

CONF=$1
INPUT_FILE_1=$2
INPUT_FILE_2=$3
CUTOFF=$4

if [ "$CONF" == "calc_summary" ]
then
    # The number of features in each file
    groupBy -i <(sort -k1,1 -k2,2n -k3,3n $INPUT_FILE_1) -c 1 -ops count | wc -l
    # The total number of, non-overlapping, bases covered by the features
    mergeBed -i <(sort -k1,1 -k2,2n $INPUT_FILE_1) | awk -F '\t' '$2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {s+=$3-($2+1)} END {print s}'
    # The length and the name of the longest feature in file. Add +1 to counter 1 vs 0 indexing
    awk -F '\t' '$2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {print $4,$3-($2+1)}' $INPUT_FILE_1 | sort -k2,2n | tail -n 1
elif [ "$CONF" == "feature_overlap" ]
then
    # Number of overlapping features in two files. Cutoff on minimum overlapping basepairs, default = 0
    intersectBed -wo -a $INPUT_FILE_1 -b $INPUT_FILE_2 | awk -v c=$CUTOFF -F '\t' '$NF > c {print $NF}' | wc -l
fi
