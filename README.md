LatitudeHistoryPlotter
======================

> github.com/snowdonjames/LatitudeHistoryPlotter

This python script parses kml data file(s) ( http://en.wikipedia.org/wiki/Keyhole_Markup_Language ) and renders the resulting arcs over a user specified image. Although the choice of image is open, map and satellite data are recommended. 

This script is intended for use with latitude data obtained from [https://www.google.com/takeout/](https://www.google.com/takeout/)‎ and converted to kml using the [latitude-json-converter](https://github.com/Scarygami/latitude-json-converter) created by [Gerwin Sturm](https://github.com/Scarygami) and [Kyle Krafka](https://github.com/kjkjava).

## Usage

Simply run the LatitudePlot.py file inside of a directory containing:

- All kml files to be rendered
- An image file for the location data to be plotted on
- A csv file named ImageData.csv containing the following fields (in this order): image file name,top edge latitude,bottom edge latitude,left edge longitude,right edge longitude,(optional)x coordinate nudge,(optional)y coordinate nudge

Upon completion, an output file should be created in the directory named LatitudeData.png

## Example csv format:

For use with http://i.imgur.com/7pZFD7s.jpg

    7pZFD7s.jpg,52.939176, 49.031686, -5.894165, 0.453186,-30,-5
    
or

For use with http://i.imgur.com/CjyohmR.jpg

    CjyohmR.jpg,59.925110, 48.892321, -11.096191, 1.944580,-2,10
