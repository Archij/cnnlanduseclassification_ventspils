import keras
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers import Input
from keras.models import Model
from keras.regularizers import *


def get_model():
	aliases = {}
	Input_1 = Input(shape=(3, 224, 224), name='Input_1')
	Convolution2D_1 = Convolution2D(name='Convolution2D_1',nb_row= 2,nb_filter= 3,nb_col= 2,activation= 'relu' )(Input_1)
	Convolution2D_2 = Convolution2D(name='Convolution2D_2',nb_row= 2,nb_filter= 3,nb_col= 2,activation= 'relu' )(Convolution2D_1)
	MaxPooling2D_1 = MaxPooling2D(name='MaxPooling2D_1')(Convolution2D_2)
	Convolution2D_3 = Convolution2D(name='Convolution2D_3',nb_row= 2,nb_filter= 3,nb_col= 2,activation= 'relu' )(MaxPooling2D_1)
	Convolution2D_4 = Convolution2D(name='Convolution2D_4',nb_row= 2,nb_filter= 3,nb_col= 2)(Convolution2D_3)
	MaxPooling2D_2 = MaxPooling2D(name='MaxPooling2D_2')(Convolution2D_4)
	Convolution2D_5 = Convolution2D(name='Convolution2D_5',nb_row= 2,nb_filter= 3,nb_col= 2,activation= 'relu' )(MaxPooling2D_2)
	Convolution2D_6 = Convolution2D(name='Convolution2D_6',nb_row= 2,nb_filter= 3,nb_col= 2,activation= 'relu' )(Convolution2D_5)
	MaxPooling2D_3 = MaxPooling2D(name='MaxPooling2D_3')(Convolution2D_6)
	Flatten_1 = Flatten(name='Flatten_1')(MaxPooling2D_3)
	Dense_1 = Dense(name='Dense_1',output_dim= 2028,activation= 'relu' )(Flatten_1)
	Dropout_1 = Dropout(name='Dropout_1',p= 0.7)(Dense_1)
	Dense_2 = Dense(name='Dense_2',output_dim= 11,activation= 'sigmoid' )(Dropout_1)

	model = Model([Input_1],[Dense_2])
	return aliases, model


from keras.optimizers import *

def get_optimizer():
	return Adam()

def is_custom_loss_function():
	return False

def get_loss_function():
	return 'binary_crossentropy'

def get_batch_size():
	return 32

def get_num_epoch():
	return 10

def get_data_config():
	return '{"kfold": 1, "mapping": {"Image": {"type": "Image", "shape": "", "port": "InputPort0", "options": {"rotation_range": 0, "height_shift_range": 0, "Scaling": 1, "Height": 28, "width_shift_range": 0, "shear_range": 0, "Normalization": false, "vertical_flip": false, "Width": 28, "horizontal_flip": false, "Resize": false, "pretrained": "None", "Augmentation": false}}, "Rating": {"type": "Categorical", "shape": "", "port": "OutputPort0", "options": {"Scaling": 1, "Normalization": false}}}, "dataset": {"name": "LandUse", "samples": 25253, "type": "private"}, "datasetLoadOption": "batch", "shuffle": true, "samples": {"training": 17677, "test": 3787, "split": 3, "validation": 3787}, "numPorts": 1}'
