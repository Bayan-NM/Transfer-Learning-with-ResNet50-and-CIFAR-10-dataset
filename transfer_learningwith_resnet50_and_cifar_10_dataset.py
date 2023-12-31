# -*- coding: utf-8 -*-
"""Transfer -Learningwith ResNet50 and CIFAR-10 dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PXjK2VqfjQGl-ODYG_jscJPiwQGc3TYb

Transfer Learning with ResNet50 and CIFAR-10 dataset

1. Prepare & Explore Dataset
"""

# import pachages
from tensorflow import keras
from keras.datasets import cifar10
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical

from keras.applications import ResNet50

from keras.optimizers import SGD,Adam

# load data.
(x_train,y_train),(x_test,y_test) = cifar10.load_data()

from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=.3)

print((x_train.shape,y_train.shape))
print((x_val.shape,y_val.shape))
print((x_test.shape,y_test.shape))

# We have 10 classes, so, our network will have 10 output neurons
y_train = to_categorical(y_train)
y_val = to_categorical(y_val)
y_test = to_categorical(y_test)

print((x_train.shape,y_train.shape))
print((x_val.shape,y_val.shape))
print((x_test.shape,y_test.shape))

#Data Augmentation Function: Let's define an instance of the ImageDataGenerator class and set the parameters.
#We have to instantiate for the Train,Validation and Test datasets
train_generator = ImageDataGenerator(
                                    rotation_range=2,
                                    horizontal_flip=True,
                                    zoom_range=.1 )

val_generator = ImageDataGenerator(
                                    rotation_range=2,
                                    horizontal_flip=True,
                                    zoom_range=.1)

train_generator.fit(x_train)
val_generator.fit(x_val)

"""2. Define the neural network architecture"""

# define the CNN model
'For the 2nd base model we will use Resnet 50 and compare the performance against the previous one'
'The hypothesis is that Resnet 50 should perform better because of its deeper architecture'
base_model_2 = ResNet50(include_top=False, weights='imagenet', input_shape=(32,32,3), classes=y_train.shape[1])

#Lets add the final layers to these base models where the actual classification is done in the dense layers
#Since we have already defined Resnet50 as base_model_2, let us build the sequential model.
model_2 = Sequential()
#Add the Dense layers along with activation and batch normalization
model_2.add(base_model_2)
model_2.add(Flatten())

#Add the Dense layers along with activation and batch normalization
model_2.add(Dense(1024,activation=('relu'),input_dim=512))
model_2.add(Dense(512,activation=('relu')))
model_2.add(Dense(256,activation=('relu')))
model_2.add(Dropout(.3))#Adding a dropout layer that will randomly drop 30% of the weights
model_2.add(Dense(128,activation=('relu')))
model_2.add(Dropout(.2))
model_2.add(Dense(10,activation=('softmax'))) #This is the classification layer

'''model_2.add(Dense(4000,activation=('relu'),input_dim=512))
model_2.add(Dense(2000,activation=('relu')))
model_2.add(Dropout(.4))
model_2.add(Dense(1000,activation=('relu')))
model_2.add(Dropout(.3))#Adding a dropout layer that will randomly drop 30% of the weights
model_2.add(Dense(500,activation=('relu')))
model_2.add(Dropout(.2))
model_2.add(Dense(10,activation=('softmax'))) #This is the classification layer'''

print(model_2.summary())

"""3. Compile the neural net"""

# compile your model
model_2.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

4. Fit / train the neural net

model_2.fit(x_train, y_train, batch_size=32, epochs=5, validation_data=(x_val, y_val), verbose=1)

"""5. Evaluate the neural net"""

score = model_2.evaluate(x_val, y_val, verbose=1)
print('Test accuracy:', score[1])

"""6. Make predictions / classifications for unseen data"""

#not yet until we enhanced the results
predictions = model_2.predict(x_test)
predictions