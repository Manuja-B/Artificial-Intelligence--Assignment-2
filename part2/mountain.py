#!/usr/local/bin/python3
#
# Authors: Authors: Austin Zebrowski:azebrows, Manuja Bandal: msbandal,  Divyanshu Jhawar: djhawar
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
from itertools import groupby

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


# populate emission probability matrix
# increase probability linearly with strength
# numbers multiplied by 100 to prevent numbers from becoming too small
def get_emission_matrix(max_values, LS):

    max_strength = max(max_values)

    emissionValues = linspace(0, 100/(int(max_strength)/2), int(max_strength))
    LE = len(emissionValues)

    xc = 0
    yc = 0
    emissionProbability = zeros((LS, LE))
    for x in states:
        for y in emissionValues:
            emissionProbability[xc][yc] = emissionValues[yc]
            yc += 1
        yc = 0
        xc += 1
    return emissionProbability


# populate transition probability matrix
# assign low probability to pixels farther away
# percentages multiplied by 100 to prevent numbers from becoming too small
def get_transition_matrix(LS, runtype, gt_row, gt_col):

    samePixelPercent = 40
    nearestPixelPercent = 40
    otherPixelPercent = 20 #/ LS

    transitionProbability = zeros((LS+1, LS+1))

    xc = 0
    yc = 0
    for x in states:
        for y in states:
            if runtype == "human":
                if xc == int(gt_row) and yc == int(gt_col):
                    transitionProbability[xc][yc] = 41
                elif x == y:
                    transitionProbability[xc][yc] = samePixelPercent
                elif x+1 == y or x-1 == y:
                    transitionProbability[xc][yc] = nearestPixelPercent
                else:
                    transitionProbability[xc][yc] = otherPixelPercent
            else:
                if x == y:
                    transitionProbability[xc][yc] = samePixelPercent
                elif x+1 == y or x-1 == y:
                    transitionProbability[xc][yc] = nearestPixelPercent
                else:
                    transitionProbability[xc][yc] = otherPixelPercent
            yc += 1
        yc = 0
        xc += 1
    return transitionProbability


def viterbi(transitionProbability, emissionProbability, edge_strength, observations):
    tps = transitionProbability.shape[0]
    L = len(observations)

    bestPath = zeros((L, tps))
    position = zeros((L, tps))

    # set initial probability

    prob = []
    for x in edge_strength[:, 0]:
        prob.append(max(emissionProbability[:, int(x)]))

    bestPath[0] = prob

    # get the remaining probabilities

    for x in range(1, L):
        for y in range(tps - 1):
            bestPath[x, y] = max(bestPath[x - 1] * transitionProbability[:, y]) * emissionProbability[y, ridge[x]]
            position[x, y] = argmax(bestPath[x - 1] * transitionProbability[:, y])

    # rewind the states

    states = zeros(L, dtype=int32)
    states[L - 1] = argmax(position[L - 1])
    for t in range(L - 2, -1, -1):
        states[t] = position[t + 1, states[t + 1]]

    #print(states)
    return states


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


    # output map begin

    # get the valid states

    states = []
    s = 1
    while s < len(edge_strength):
        states.append(s)
        s += 1

    LS = len(states)

    # get the probability matrices

    transitionProbability = get_transition_matrix(LS, "none", gt_row, gt_col)
    emissionProbability = get_emission_matrix(max_values, LS)

    # run the viterbi algorithm

    states = viterbi(transitionProbability, emissionProbability, edge_strength, ridge)

    red = (255, 0, 0)
    imageio.imwrite("output_map.jpg", array(draw_edge(input_image, states, red, 5)))

    # output map end

    # human input begin

    states = []
    s = 1
    while s < len(edge_strength):
        states.append(s)
        s += 1

    LS = len(states)

    transitionProbability = get_transition_matrix(LS, "human", gt_row, gt_col)
    emissionProbability = get_emission_matrix(max_values, LS)

    # run the viterbi algorithm

    states = viterbi(transitionProbability, emissionProbability, edge_strength, ridge)

    green = (0, 255, 0)
    imageio.imwrite("output_human.jpg", array(draw_edge(input_image, states, green, 5)))

    # human input end
