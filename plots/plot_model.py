from keras.utils import plot_model

from training.models import models

model_name = 'basic_lstm'
model = models[model_name]()
plot_model(model, to_file='../fig/' + model_name + '.png',show_shapes=True)
