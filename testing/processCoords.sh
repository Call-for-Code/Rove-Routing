#!/bin/bash

coords=`cat data.txt | tr -d " \[\"\]"`

i=0
for line in $coords
do
   i=$(($i+1))
   echo $line,$i,#FF0000
done