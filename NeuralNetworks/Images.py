from PIL import Image
import glob
#{\tt <userid>\_<pose>\_<expression>\_<eyes>\_<scale>.pgm}

#import images as training set etc

import NeuralNetwork

#net = NeuralNetwork.Network([960,100,4])

#net.SGD(training_data, 100, 4, 0.001, test_data = test_data)



#def load_data():
#loads files

#def load_data_wrapper():


#def vectorized_result(j):


#im = Image.open(file)

#pixels = list(im.getdata())

#width, height = im.size

import Numbers

numbers = Numbers
training_data, validation_data, test_data = numbers.load_data_wrapper()

net = NeuralNetwork.Network([784,30,10])

net.SGD(training_data, 30, 10, 3.0, test_data=test_data)