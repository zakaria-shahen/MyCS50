#!/bin/bash

#list=("random5000", "random10000", "random50000", "reversed5000", "reversed10000", "reversed50000", "sorted5000", "sorted10000", "sorted50000")
#declare -a list=("random5000", "random10000", "random50000", "reversed5000", "reversed10000", "reversed50000", "sorted5000", "sorted10000", "sorted50000")
declare -a list=("random5000" "random10000" "random50000" "reversed5000" "reversed10000" "reversed50000" "sorted5000" "sorted10000" "sorted50000")
# $list[0]:1
#  ${list[2]}.txt
for i in 1 2 3
do
    for n in  0 1 2 3 4 5 6 7 8
    do
        (time ./sort$i ${list[$n]}.txt) 2>> time2.txt
        echo "==================== Sort$i output=> ${list[$n]}.txt ====================" >> time1.txt
    done
done