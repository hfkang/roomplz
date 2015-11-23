#!/bin/bash

cd ~/roomplz
python3 osm.py -d
cp -f BA_organized /var/www/html
