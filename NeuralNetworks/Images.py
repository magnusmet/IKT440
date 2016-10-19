import glob
import random
import numpy as np
import NeuralNetwork
# {\tt <userid>\_<pose>\_<expression>\_<eyes>\_<scale>.pgm}

# import images as training set etc


def read_pgm(pgmf):
    """Return a raster of integers from a PGM as a list of lists."""
    assert pgmf.readline() == 'P5\n'
    (width, height) = [int(i) for i in pgmf.readline().split()]
    depth = float(pgmf.readline())
    assert depth <= 255

    raster = []
    for y in range(height):
        row = []
        for y in range(width):
            raster.append(float(ord(pgmf.read(1)))/depth)
    return raster


def image_data(image):
    directions = ["_left_", "_right_", "_straight_", "_up_"]
    pixels = read_pgm(open(image, 'rb'))

    for i in range(len(directions)):
        if directions[i] in image:
            return pixels, i


def load_images():
    pixels_direction = [[],[]]
    images = glob.glob('faces_4\\*\\*\\*')
    random.shuffle(images)
    for image in images:
        px, direction = image_data(image)
        pixels_direction[0].append(px)
        pixels_direction[1].append(direction)
    return pixels_direction


def vectorized_result(j):
    e = np.zeros((4, 1))
    for i in range(4):
        if i == j:
            e[i] = 0.9
        else:
            e[i] = 0.1
    return e

total_d = load_images()

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

acc = 0.0
eta = 0.25
mini_batches = 1
epochs = 50
for i in range(1, 10):
    net = NeuralNetwork.Network([960, 50, 4])
    acc += net.SGD(training_data, epochs, mini_batches, eta, test_data=test_data)
    print "i: {0}, eta: {1}, mb: {2}, epochs: {3}, acc: {4}".format(i, eta, mini_batches, epochs, acc / i)





