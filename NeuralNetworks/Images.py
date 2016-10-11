from PIL import Image
import glob
import numpy as np
#{\tt <userid>\_<pose>\_<expression>\_<eyes>\_<scale>.pgm}

#import images as training set etc

import NeuralNetwork


def imagedata(file):

    im = Image.open(file)
    pixels = list(im.getdata())

    if "left" in file:
        return pixels,0#vectorized_result(0)
    elif "right" in file:
        return pixels,1#vectorized_result(1)
    elif "straight" in file:
        return pixels,2#vectorized_result(2)
    elif "up" in file:
        return pixels,3#vectorized_result(3)

def loadImages():
    # folders = glob.glob('faces_4\\faces_4\\*')
    # for folder in folders:
    #     images += glob.glob(folder + '\\*')

    pixels_direction = [[],[]]
    images = glob.glob('faces_4\\*\\*\\*')
    for image in images:
        px, direction = imagedata(image)
        pixels_direction[0].append(px)
        pixels_direction[1].append(direction)
    return pixels_direction#sets(pixels_direction)
#
# def sets(pixels_direction):
#     n = int(len(pixels_direction)*0.8)
#     for i in xrange(0, len(pixels_direction),n):
#         yield pixels_direction[i:i+n]

def vectorized_result(j):
    e = np.zeros((4, 1))
    e[j] = 1.0
    return e

total_d = loadImages()#, te_d = loadImages()

#print len(tr_d[0][0])
tr_d = [[],[]]
te_d = [[],[]]
for i in range(0, len(total_d[1])):
    if i < int(len(total_d[1])*0.2):
        te_d[0].append(total_d[0][i])
        te_d[1].append(total_d[1][i])
    else:
        tr_d[0].append(total_d[0][i])
        tr_d[1].append(total_d[1][i])





training_inputs = [np.reshape(x, (960, 1)) for x in tr_d[0]]
training_results = [vectorized_result(y) for y in tr_d[1]]
training_data = zip(training_inputs, training_results)
test_inputs = [np.reshape(x, (960, 1)) for x in te_d[0]]
test_data = zip(test_inputs, te_d[1])

#print training_data[1]

net = NeuralNetwork.Network([960,3,4])

net.SGD(training_data, 100, 50, 0.01, test_data = test_data)





