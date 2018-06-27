#!/bin/bash


SECONDS=0
INPUT=../rootdirpath/jvdofs/Fall2016/wdfiles/cats4minecore.csv
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read rcat pcat 
do
	cd ../rootdirpath/jvdofs/Fall2016/runlogs/FullCol/
	rm tempfile.log
	grep 'RESULTVALUE' FullColRun-$rcat-$pcat-DL-eruns-toismodel.log >> tempfile.log
	cd ../rootdirpath/jvdofs/Fall2016/scripts
	python writeResults.py
done < $INPUT
IFS=$OLDIFS
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
