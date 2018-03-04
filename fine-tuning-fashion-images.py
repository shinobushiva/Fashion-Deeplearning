import os
import shutil
import random

from fashionutils import to_file_path

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
from keras.optimizers import Adam

from keras import optimizers

from keras.models import Model
from keras.layers import Input
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model
from keras.callbacks \
    import TensorBoard, ModelCheckpoint, \
    Callback, CSVLogger, ReduceLROnPlateau, \
    EarlyStopping

from keras.datasets import cifar10
from keras.utils import np_utils


class LossHistory(Callback):
    def on_train_begin(self, logs=None):
        self.losses ={}

    def on_batch_end(self, batch, logs=None):
        self.losses.append(logs.get('loss'))


IN_DIR = 'images-299-categorized'
TRAIN_DIR = 'images-finetune/train_images'
TEST_DIR = 'images-finetune/test_images'


batch_size = 10

img_rows = 299
img_cols = 299

classes = ['accessory','bag','fashion-accessories','hat','jacket-outerwear',
'leg-wear','onepiece','pants','shoes','skirt','tops','wrist-watch']

nb_classes = len(classes)

train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
    directory=TRAIN_DIR,
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    classes = classes,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    directory=TEST_DIR,
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    classes=classes,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True
)

input_tensor = Input(shape=(img_rows, img_cols, 3))
vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

top_model = Sequential()
top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(nb_classes, activation='softmax'))

model = Model(input=vgg16.input, output=top_model(vgg16.output))

for layer in model.layers[:15]:
    layer.trainable = False

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

model.summary()
model.save('model.h5')

checkpointer = ModelCheckpoint(filepath='tmp/weights.hdf5', verbose=1, save_best_only=True)
# losshistory = LossHistory()
csvlogger = CSVLogger('training.log')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-5)
earlystopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='auto')

history = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_classes*190/batch_size,
    epochs=50,
    validation_data=test_generator,
    validation_steps=nb_classes*10/batch_size,
    callbacks=[checkpointer, csvlogger, reduce_lr, earlystopping]
)

model.save_weights('param.hdf5')