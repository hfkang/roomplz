#!/bin/bash
LOG=~/roomplz/update.log
#This executes the osm download script for BA only sofar
cd ~/roomplz
python3 osm.py -engineering 
cp -f {*_organized,*_fulldata} /var/www/html



