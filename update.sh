#!/bin/bash

#This executes the osm download script for BA only sofar
cd ~/roomplz
python3 osm.py -d
cp -f BA_organized /var/www/html
