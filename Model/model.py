# 1. Thêm các thư viện cần thiết
import numpy as np
# import cv2
# import PIL
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
# from tensorflow.keras.layers import Conv2D, MaxPooling2D
# from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.initializers import RandomNormal
# from tensorflow.keras.datasets import mnist
import glob as glob

class Model():
    def __init__(self):

        self.init_model()

    def init_model(self, random_normal = 0.01):

        baseModel = VGG16(weights='imagenet', include_top=False)
        base_model = Sequential()

        # Get the first 13 layer of VGG16
        for layer in baseModel.layers[:14]:
            base_model.add(layer)

        init = RandomNormal(stddev=random_normal)
        fcHead = base_model.output
        fcHead = Conv2D(512, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(512, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(512, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(256, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(128, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(64, (3, 3), activation='relu', dilation_rate = 2, kernel_initializer = init, padding = 'same')(fcHead)
        fcHead = Conv2D(1, (1, 1), activation='relu', dilation_rate = 1, kernel_initializer = init, padding = 'same')(fcHead)

        self.model = model = Model(inputs=base_model.input, outputs=fcHead)
        self.base_model = base_model

        model.summary()

    def run_freeze_time(self, x_train, y_train, 
                        x_val,y_val,
                        RMS= 0.001, epoch = 25, batch_size = 32, loss_function = 'categorical_crossentropy'):

        for layer in base_model.layers:
            layer.trainable = False
        opt = RMSprop(RMS)
        self.model.compile(opt,loss_function, ['accuracy'])
        numOfEpoch = epoch
        self.History = model.fit(x_train, y_train, batch_size=batch_size, validation_data=(x_val, y_val),epochs=numOfEpoch)

    def run_unfreeze_time(self, x_train, y_train, 
                        x_val,y_val,
                        SGD = 0.001, epoch = 35, batch_size = 32, loss_function = 'categorical_crossentropy'):

        for layer in baseModel.layers:
            layer.trainable = True
        numOfEpoch = epoch
        opt = SGD(SGD)
        self.model.compile(opt,loss_function, ['accuracy'])
        self.History = model.fit(x_train, y_train, batch_size=batch_size, validation_data=(x_val, y_val),epochs=numOfEpoch)

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = stf.keras.models.load_model(path)
    
    def loss_during_time(self, epoch = 25):

        fig = plt.figure()
        numOfEpoch = epoch
        H = self.History
        plt.plot(np.arange(0, numOfEpoch), H.history['loss'], label='training loss')
        plt.plot(np.arange(0, numOfEpoch), H.history['val_loss'], label='validation loss')
        plt.plot(np.arange(0, numOfEpoch), H.history['accuracy'], label='accuracy')
        plt.plot(np.arange(0, numOfEpoch), H.history['val_accuracy'], label='validation accuracy')
        plt.title('Accuracy and Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss|Accuracy')
        plt.legend()
