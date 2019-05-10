#!/usr/bin/python3
import urllib.request
from PIL import Image
import os
import math

class GMapDown:

    def __init__(self, lat, lng, zoom=12):
        self._lat = lat
        self._lng = lng
        self._zoom = zoom

    def getCoords(self):
        tile_size = 256
        numTiles = 1 << self._zoom
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size
        sin_y = math.sin(self._lat * (math.pi / 180.0))
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size
        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):
        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 30)
        tile_height = kwargs.get('tile_height', 30)

        if start_x == None or start_y == None:
            start_x, start_y = self.getCoords()

        width, height = 256 * tile_width, 256 * tile_height

        map_img = Image.new('RGB', (width, height))

        for x in range(0, tile_width):
            for y in range(0, tile_height):
                url = 'https://mt0.google.com/vt/lyrs=s&?x=' + str(start_x + x) + '&y=' + str(start_y + y) + '&z=' + str( self._zoom)
                print(url)
                current_tile = str(x) + '-' + str(y)
                urllib.request.urlretrieve(url, current_tile)

                im = Image.open(current_tile)
                map_img.paste(im, (x * 256, y * 256))

                os.remove(current_tile)

        return map_img


def main():
    zoom =  17
    listOfCoords = [[-25.430735, -54.302845]]
    count = 0
    for (lat,lng) in listOfCoords:
        gmd = GMapDown(lat,lng, zoom)
        try:
            img = gmd.generateImage()
        except IOError:
            print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            img.save(""+str(count)+".png")
            print("The map has successfully been created")
        count +=1
if __name__ == '__main__':  main()

