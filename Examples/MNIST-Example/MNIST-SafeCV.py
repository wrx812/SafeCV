# coding: utf-8

# In[1]:


import sys

from keras.models import load_model

sys.path.append('/usr/local/lib/python2.7/site-packages')

from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.datasets import mnist
import keras.utils
from keras.utils import np_utils
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from keras.optimizers import SGD
from keras.utils import np_utils

import keras
from keras import applications
from tqdm import tqdm
import math
import tensorflow as tf

import copy

from keras.datasets import mnist


def fn(correct, predicted):
    return tf.nn.softmax_cross_entropy_with_logits(labels=correct,
                                                   logits=predicted / 1)


size_var = 28
rows = 28
cols = 28
epochs = 20

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# load model
# model = Sequential()
#
# model.add(Conv2D(32, 3, 3, input_shape=(1, 28, 28), dim_ordering="th"))
# model.add(Activation('relu'))
# model.add(Conv2D(32, 3, 3))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Conv2D(64, 3, 3))
# model.add(Activation('relu'))
# model.add(Conv2D(64, 3, 3))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Flatten())
# model.add(Dense(200))
# model.add(Activation('relu'))
# model.add(Dense(200))
# model.add(Activation('relu'))
# model.add(Dense(10))
# model.add(Activation("softmax"))
#
# batch_size = 128
# num_epochs = 7
# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#
# model.compile(loss=fn, optimizer=sgd, metrics=['accuracy'])

# model.load_weights("cw-attacks-mnist.weights")

# In[2]:
model = load_model("./model/model_mnist.hdf5")
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import os
import cv2
import numpy as np
import keras
from keras import applications
from SafeCV import *


def max_manip(p, e):
    w = 255 - p
    if (p < w):
        return 255
    else:
        return 0


(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(y_train.shape)
shape = (1, 28, 28, 1)
image_arr = []
label_arr = []
for imnum in range(len(x_test)):  # 都生成一次看看
    # for imnum in range(3):
    # imnum = 2567

    # params_for_run = MCTS_Parameters(x_test[imnum], y_test[imnum], model, predshape=(1, 1, 28, 28))
    params_for_run = MCTS_Parameters(x_test[imnum], y_test[imnum], model, predshape=shape)
    params_for_run.X_SHAPE = 28
    params_for_run.Y_SHAPE = 28
    params_for_run.small_image = True
    params_for_run.verbose = False  # False
    params_for_run.MANIP = max_manip
    params_for_run.VISIT_CONSTANT = 1
    params_for_run.VISIT_CONSTANT = 6
    params_for_run.simulations_cutoff = 100
    params_for_run.backtracking_constant = 10

    best_image, sev, prob, statistics = MCTS(params_for_run)
    # print(prob)
    # In[3]:
    image_arr.append(best_image)
    label_arr.append(y_test[imnum])

    print("BEST ADVERSARIAL EXAMPLE:")
    plt.imshow(best_image)
    print("model....................")
    # print(model)
    prob = model.predict(best_image.reshape(shape))

    # prob2 = model(best_image.reshape(shape))
    print(prob)
    #  print(prob2)
    metrics = 1 - np.sum(prob ** 2, axis=1)
    new_class = np.argmax(prob[0])
    new_prob = prob[0][np.argmax(prob)]

    print("True class: %s; Predicted as: %s with confidence: %s; After %s manipulations" % (
        y_test[imnum], new_class, new_prob, sev))
    plt.axis('off')
    plt.title("True class {} ,Predicted as {} ".format(y_test[imnum], new_class, ))
    plt.show()
    plt.savefig("./image/{}.png".format(imnum))
    print("add {}".format(imnum))
    plt.clf()
    # print("MCTS Run analysis:")
    # a, = plt.plot(statistics[0], label="Min Severity Found")
    # b, = plt.plot(statistics[1], label="Severity per Iteration")
    # c, = plt.plot(statistics[2], label="Rolling Average Severity")
    # plt.legend(handles=[a, b, c], loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.title("Single Run MCTS Statisitcs")
    # plt.xlabel("Iteration")
    # plt.ylabel("L_0 Severity")
    # plt.show()
print(np.array(image_arr).shape)
print(np.array(label_arr).shape)
attack = "safe"
dataset = "mnist"
np.save('./adv_image/{}_{}_image'.format(attack, dataset), image_arr)
np.save('./adv_image/{}_{}_label'.format(attack, dataset), label_arr)
