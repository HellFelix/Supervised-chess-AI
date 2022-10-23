import numpy as np
from keras import models, layers, utils, optimizers, callbacks
import pydot

positions = np.load("positions.npy", allow_pickle=True)
evaluations = np.load("evaluations.npy", allow_pickle=True)

n_positions = len(positions)
n_training = np.round(int(n_positions*0.7)) # Determine how many positions will be used to train

# Using all positions up to n_training
training_positions = positions[:n_training]
training_evaluations = evaluations[:n_training]

# Using all positions after n_training
test_positions = positions[n_training:]
test_evaluations = evaluations[n_training:]


# Building the actual model
def build_model(conv_size, conv_depth):
    model = models.Sequential()
    model.add(layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', input_shape=(14, 8, 8), name="Conv_layer1"))
    for n in range(conv_depth-1):
        name = "Conv_layer" + str(n+2)
        model.add(layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', name=name))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    return model

model = build_model(32, 4)

utils.plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
model.summary()

model.fit(training_positions, training_evaluations, epochs=10, validation_data=(test_positions, test_evaluations))


model.save('Chess_AI.model', overwrite=True)