#!/bin/bash

#This executes the osm download script for BA only sofar
cd ~/roomplz
python3 osm.py -engineering
cp -f {BA_organized,GB_organized,SF_organized} /var/www/html
