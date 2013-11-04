#!/bin/bash

#The first and only argument, the file pattern, must be in double quotes.
#Example: ./fisbadat2fits.sh "./newdata/*.dat"

input_patt=$1 

for f in $input_patt;
do
	./fisba2fits "$f";
done
