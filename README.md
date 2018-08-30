# roomplz
Scrape the U of T OSM website and provide a list of free rooms at any
given moment. 

The application is built with flask, and downloads the scraped table to
a pickle file. The actual download component is in osm.py, but can be
set up as part of a weekly cronjob on Sundays. Just execute update.sh
and it'll update the files for the upcoming week. 

## Installation Notes

The server is deployed with zappa, which may have locale issues when installing. `export LC_ALL="en_US.UTF-8"` at the end of .bashrc should resolve it. 

