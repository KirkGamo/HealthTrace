import os
from tensorflow import keras

models = ['dengue', 'typhoid', 'cholera']
print('Current Model Input Shapes:')
for m in models:
    path = f'app/models/{m}_forecast_model.h5'
    if os.path.exists(path):
        model = keras.models.load_model(path, compile=False)
        print(f'{m}: {model.input_shape}')
