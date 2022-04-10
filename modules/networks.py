import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications import vgg16
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications import inception_v3
from tensorflow.keras.applications.inception_v3 import InceptionV3

from abc import ABC, abstractmethod

class Network(ABC):
    def __init__(self, img_width, img_height):      
        self.red = None
        self.img_width = img_width
        self.img_height = img_height

    
    @abstractmethod
    def create_network(self):
        pass
    @abstractmethod
    def summary(self):
        pass


class Resnet(Network):
    def create_network(self):

        # Pre-Trained Model
        base_model = ResNet50(weights='imagenet', 
                            include_top=False, 
                            input_shape = (self.img_width, self.img_height, 3))
        base_model.trainable = False

        # Add Layer Embedding
        self.red = tf.keras.Sequential([
            base_model,
            GlobalMaxPooling2D()
        ])

    def summary(self):
        self.red.summary()


class VGG(Network):
    def create_network(self):

        # Pre-Trained Model
        base_model = VGG16(weights='imagenet', include_top=False, input_shape= (self.img_width, self.img_height, 3))
        base_model.trainable = False

        # Add Layer Embedding
        self.red = tf.keras.Sequential([
            base_model,
            GlobalMaxPooling2D()
        ])

    def summary(self):
        self.red.summary()

class Inception(Network):
    def create_network(self):

        # Pre-Trained Model
        base_model = InceptionV3(weights='imagenet', 
                            include_top=False, 
                            input_shape = (self.img_width, self.img_height, 3))
        base_model.trainable = False

        # Add Layer Embedding
        self.red = tf.keras.Sequential([
            base_model,
            GlobalMaxPooling2D()
        ])

    def summary(self):
        self.red.summary()
