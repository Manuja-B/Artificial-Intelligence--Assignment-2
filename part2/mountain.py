#!/usr/local/bin/python3
#
# Authors: Austin Zebrowski
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

# main program
#

if __name__ == "__main__":

    (input_filename, gt_row, gt_col) = sys.argv[1:]

    # load in image
    input_image = Image.open(input_filename)

    # compute edge strength mask
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create a horizontal centered line.

    # output simple begin

    t = transpose(edge_strength)
    max_values = list(map(max, t))
    count = 0
    ridge = []

    for x in max_values:
       ridge.append(t[count].tolist().index(x))
       count += 1

    blue = (0, 0, 255)
    imageio.imwrite("output_simple.jpg", array(draw_edge(input_image, ridge, blue, 5)))

    # output simple end

