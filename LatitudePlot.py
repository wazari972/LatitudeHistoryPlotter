#!/usr/bin/env python3

# LatitudePlot.py
# Created 30 July 2013
# Created by snowdonjames@googlemail.com

import os, time, math
from datetime import datetime
from time import mktime
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import functools

DATA_DIR = "."


GPX_ENABLED = True
try:
    import gpxpy
    import gpxpy.gpx
except:
    GPX_ENABLED = False
    print ("""Couldn't import gpxpy, 
run "pip install gpxpy"
or go to https://github.com/tkrajina/gpxpy
""")
    

def GetFiles():
    """Locates and reads local .<ext> files, returns a list of <ext> dictionary data""" 
    gpsData = []
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            sp = filename.split('.')
            if sp[len(sp)-1]== "kml": #locate kml files
                print ("Reading kml file {}".format(filename))
                gpsData.append(ReadKmlFile(dirname, filename))
                
            elif GPX_ENABLED and filename.endswith(".gpx"):
                print ("Reading gpx file {}".format(filename))
                try:
                    gpsData.append(ReadGpxFile(dirname, filename))
                except FileNotFoundError:
                    pass
                
    return gpsData

def ReadKmlFile(dirname, filename):
    """Parses a single kml file, returns a dict of format {time: [lat, long]}"""
    KmlData = {}
    kmltime = datetime.time
    latlist = []
    longlist = []
    timelist = []
    cnt = 0
    with open(filename) as f:
        line = f.readline()
        for line in f.readlines():
            if 'when' in line:
                timelist.append(time.strptime(ET.fromstring(line)[0].text,"%Y-%m-%dT%H:%M:%SZ"))
                if 'coordinates' in line:
                    latlist.append(float(ET.fromstring(line)[0].text.split(',')[0]))
                    longlist.append(float(ET.fromstring(line)[0].text.split(',')[1]))
                    cnt+=1
                    if cnt % 5000 ==0:
                        print ("Parsing " + filename + ": points found: " + str(cnt))

    return [latlist, longlist, timelist]

def ReadGpxFile(dirname, filename):
    latlist = []
    longlist = []
    timelist = []
    
    with open(filename) as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for cnt, point in enumerate(segment.points):
                    latlist.append(point.latitude)
                    longlist.append(point.longitude)
                    timelist.append(point.time)
                print ("Parsing {}: points found: {}".format(filename, cnt))

    return [latlist, longlist, timelist]

def DrawMapData(KmlData,InputImage, OutputImage, itop, ibottom, ileft, iright,xnudge,ynudge):
    """Draws kml line data on top of the specified image"""
    im = Image.open(InputImage)
    draw = ImageDraw.Draw(im)
    cnt = 0
    
    LongToX_ = functools.partial(LongToX, LeftLong=ileft, RightLong=iright, ImWidth=im.size[0])
    LatToY_ = functools.partial(LatToY, TopLat=itop, BottomLat=ibottom, ImHeight=im.size[1])
    for KmlD in KmlData:
        for d in range(len(KmlD[0])-1):
            #Get points x and y coordinates and draw line
            x1 = LongToX_(KmlD[1][d]) + xnudge
            y1 = LatToY_(KmlD[0][d]) + ynudge
            x2 = LongToX_(KmlD[1][d+1]) + xnudge
            y2 = LatToY_(KmlD[0][d+1]) + ynudge
            
            if EuclidDistance(x1,y1,x2,y2) < 10000:
                #setting this around 80 works okay. Attempts to remove some noise
                draw.line((x1,y1, x2,y2), fill=80)

            cnt += 1
            if cnt % 10000 == 0:
                print ("Drawing point number " + str(cnt))
    im.save(OutputImage)
        
def LongToX(InputLong, LeftLong, RightLong, ImWidth):
    """Converts a longitude value in to an x coordinate"""
    return ScalingFunc(InputLong+360, LeftLong+360, RightLong+360, ImWidth);

def LatToY(InputLat, TopLat, BottomLat, ImHeight):
    """Converts a latitude value in to a y coordinate"""
    return ScalingFunc(InputLat+360, TopLat+360, BottomLat+360, ImHeight);

def EuclidDistance(x1, y1, x2, y2):
    """Calculates the euclidean distance between two points"""
    return math.sqrt((x1 - x2)**2+(y1 - y2)**2)

def ScalingFunc(inputv, minv, maxv, size):
    """Helps convert latitudes and longitudes to x and y"""
    if((float(maxv) -float(minv)) ==0):
       return 0
    return ((((float(inputv) - float(minv)) / (float(maxv) -float(minv))) * float(size)));

def ParseImageFile():
    """Reads SatelliteImageData.csv containing:
    <File name of image to draw data on>,
    <image top latitude>,
    <image bottom lattitude>,
    <image left longitude>,
    <image right longitude>,
    (optional) <x value nudge>,
    (optional) <y value nudge>"""
    try:
        with open('ImageData.csv', 'r') as f:
            read_data = f.read().split(',')
    except FileNotFoundError:
        read_data = "/home/kevin/Downloads/gpx/france_map.gif,50.745377,42.783845,-4.279175,8.638000,45,-25".split(",")
        
    while 5 <= len(read_data) < 7:
        read_data.append(0)
    ReturnData = [0]*7
    ReturnData[0]=read_data[0]
    for i in range(1,7):
        ReturnData[i] = float(read_data[i])
    print (ReturnData)
    return ReturnData

if __name__ == "__main__":
    ImageData = ParseImageFile()
    DrawMapData(GetFiles(),ImageData[0], "LatitudeData.png", ImageData[1], ImageData[2], ImageData[3], ImageData[4],ImageData[5],ImageData[6])
