"""
Reference from https://towardsdatascience.com/transfer-learning-for-image-classification-using-keras-c47ccf09c8c8

1. Loading things up
For image classification in Keras,
the easiest way to do this is to separate your data into folders for each class.

>>  select the model that we want to perform transfer learning on.
As of today’s writing, MobileNet is the fastest and NASNetLarge is the most accurate.
https://keras.io/applications/#models-for-image-classification-with-weights-trained-on-imagenet

2.Flowing data
Now we’ll need to create a data generator to actually get our data from
our folders and into Keras in an automated way.

 >> ImageDataGenerator()
 >> flow_from_directory()

3.Popping layers


4. Train it

"""

from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.models import Sequential, Model
from keras.optimizers import SGD, Adam
import matplotlib.pyplot as plt

TRAIN_DIR = "food_dataset"
HEIGHT = 300
WIDTH = 300
BATCH_SIZE = 8

# include_top=False . it means that
# we won’t be keeping the Fully-Connected (FC) layers at the end of the model
base_model = ResNet50(weights='imagenet',
                      include_top=False,
                      input_shape=(HEIGHT, WIDTH, 3))


# 1> create a data generator to actually get our data from
#    our folders and into Keras in an automated way.
# 2> add some additional data augmentation to our generator,
#    flipping and rotations, to try and boost our model’s accuracy.
train_datagen = ImageDataGenerator(
      preprocessing_function=preprocess_input,
      rotation_range=90,
      horizontal_flip=True,
      vertical_flip=True
    )

# 1> flow_from_directory : will use a queue to maintain
#    a continuous flow of loading and preparing our images!
# 2> define the image dimensions and batch size : the Keras generator will automatically
#    resize all loaded images to the size of target_size using bilinear interpolation.
train_generator = train_datagen.flow_from_directory(TRAIN_DIR,
                                                    target_size=(HEIGHT, WIDTH),
                                                    batch_size=BATCH_SIZE)


def build_finetune_model(base_model, dropout, fc_layers, num_classes):
    """
    set up our final model for transfer learning.
    :param base_model:
    :param dropout:
    :param fc_layers:
    :param num_classes:
    :return:
    """
    # freezing all of the base model’s layers.
    # telling Keras not to update those weights during training
    for layer in base_model.layers:
        layer.trainable = False

    #  add on our FC layers. We do this in a loop since many networks have multiple FC layers
    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        # New FC layer, random init
        x = Dense(fc, activation='relu')(x)
        x = Dropout(dropout)(x)

    # New softmax layer
    predictions = Dense(num_classes, activation='softmax')(x)
    return Model(inputs=base_model.input, outputs=predictions)


class_list = ["Pizza", "Burger", "Taco"]
FC_LAYERS = [1024, 1024]
dropout = 0.5

finetune_model = build_finetune_model(base_model,
                                      dropout=dropout,
                                      fc_layers=FC_LAYERS,
                                      num_classes=len(class_list))

# train
NUM_EPOCHS = 10
BATCH_SIZE = 8
num_train_images = 10000

# 1> choose Adam because it’s super quick and easy to use vs SGD.
# 2> We set the learning rate to be small because we are only fine tuning our model here,
# specifically the FC layers; we aren’t looking for any massive changes, just tweaks.
adam = Adam(lr=0.00001)
finetune_model.compile(adam, loss='categorical_crossentropy', metrics=['accuracy'])

# set up some checkpoints to save the weights for later
filepath="./checkpoints/" + "ResNet50" + "_model_weights.h5"
checkpoint = ModelCheckpoint(filepath, monitor=["acc"], verbose=1, mode='max')
callbacks_list = [checkpoint]

# 1> Applying the fit_generator functions runs the entire training regiment
# with optional number of epochs, batch size, and data shuffling
# 2> history:  use the history output to plot our training results.
history = finetune_model.fit_generator(train_generator,
                                       epochs=NUM_EPOCHS,
                                       workers=8,
                                       steps_per_epoch=num_train_images // BATCH_SIZE,
                                       shuffle=True,
                                       callbacks=callbacks_list)


def plot_training(history):
    """
    Plot the training and validation loss + accuracy
    :param history:
    :return:
    """
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r.')
    plt.plot(epochs, val_acc, 'r')
    plt.title('Training and validation accuracy')

    # plt.figure()
    # plt.plot(epochs, loss, 'r.')
    # plt.plot(epochs, val_loss, 'r-')
    # plt.title('Training and validation loss')
    plt.show()
    plt.savefig('acc_vs_epochs.png')


plot_training(history)