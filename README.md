# roomplz
Scrape the U of T OSM website and provide a list of free rooms at any
given moment. 

The application is built with flask, and downloads the scraped table to
a pickle file. The actual download component is in osm.py, but can be
set up as part of a weekly cronjob on Sundays. Just execute update.sh
and it'll update the files for the upcoming week. 

There *is* search functionality, but it's only half implemented and is 
unlikely to ever be completed as it was never identified to be a useful
feature. 