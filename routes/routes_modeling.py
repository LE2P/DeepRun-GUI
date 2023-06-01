from app import app
from flask import request, jsonify
#import tensorrt; assert tensorrt.Builder(tensorrt.Logger())
import tensorflow as tf
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os, sys, io
from settings.paths import paths
from tools.model_tf import ModelLoader

config_filename = None  # Variable to store the filename of the config file

@app.route('/upload_source', methods=['POST'])
def upload_config_source():
    global config_filename  # Use the global variable
    # Get the uploaded file
    config_file = request.files["config_file"]
    print('Upload source: '+config_file.filename)
    
    # Special case if the uploaded file is a h5 file because h5 file need to force the mimetype to application/octet-stream
    if config_file.filename.endswith('.h5'):
        config_file = FileStorage(config_file.stream, config_file.filename, 'application/octet-stream')

    # Save the uploaded file with a specific filename
    config_filename = secure_filename(config_file.filename)
    print('Upload source: '+paths.modeling_path + config_filename)
    config_file.save(paths.modeling_path + config_filename)
    app.logger.error("config_file : {}".format(str(config_file)))
    return jsonify(message='The config file "'+config_filename+'" is successfully uploaded.', color='green'), 200

@app.route('/generate_from_source', methods=['GET'])
def generate_model_source():
    global config_filename  # Use the global variable
    # Generate the TensorFlow model
    # Construct the full path to the config file
    config_file_path = os.path.join(paths.modeling_path, config_filename)
    print('Generate from source: '+config_file_path)
    # Load the config file and return a message if the config file is not supported
    try:
        loader = ModelLoader(config_file_path)
        loader.load_model()
    except Exception as e:
        return jsonify(message='The config file "'+config_filename+'" is not supported.', color='red'), 400

    model = loader.get_model()

    # Check if the model has been loaded successfully
    if model is not None:
        # Save the model to disk
        model.save(paths.modeling_path + 'model')
        # Capture the summary of the model
        buffer = io.StringIO()
        model.summary(print_fn=lambda x: buffer.write(x + "\n"))
        model_summary_string = buffer.getvalue()
        return jsonify(message='The model "'+config_filename+'" is successfully generated.', 
                       model_summary=model_summary_string, color='green'), 200
    else:
        return jsonify(message='Failed to load the model "'+config_filename+'".', color='red'), 400

@app.route('/generate_from_param', methods=['POST'])
def generate_model_param():
    height_image = int(request.json['height_image'])
    width_image = int(request.json['width_image'])
    channels_image = int(request.json['channels_image'])
    conv_layers = int(request.json['conv_layers'])
    dense_layers = int(request.json['dense_layers'])
    conv_kernels = int(request.json['conv_kernels'])
    dense_neurons = int(request.json['dense_neurons'])

    def generate_model_with_parameters(nUnit, nDense, nConvLayers, nDenseLayers, height, width, channels):
        inputs = tf.keras.Input(shape=(height, width, channels))
        x = inputs
        for _ in range(nConvLayers):
            x = tf.keras.layers.Conv2D(int(nUnit), (7, 7), padding='same', activation='relu')(x)
            x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(int(nUnit/2), (3, 3), padding='valid', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        conv2 = tf.keras.layers.Conv2D(int(nUnit/3), (3, 3), padding='same', activation='relu')(x)
        layer2 = tf.keras.layers.concatenate([x, conv2])
        conv3 = tf.keras.layers.Conv2D(int(nUnit/4), (1, 1), padding='valid', activation='relu')(layer2)
        layer3 = tf.keras.layers.BatchNormalization()(conv3)
        flatten = tf.keras.layers.GlobalAveragePooling2D()(layer3)
        for _ in range(nDenseLayers):
            flatten = tf.keras.layers.Dense(int(nDense), activation='relu')(flatten)
        fullylvl1 = tf.keras.layers.Dense(int(nDense), activation='relu')(flatten)
        fullylvl2 = tf.keras.layers.Dense(int(nDense), activation='relu')(flatten)
        fullylvl3 = tf.keras.layers.Dense(int(nDense), activation='relu')(flatten)
        outlvl1 = tf.keras.layers.Dense(4, activation='softmax', name='lvl1')(fullylvl1)
        outlvl2 = tf.keras.layers.Dense(11, activation='softmax', name='lvl2')(fullylvl2)
        outlvl3 = tf.keras.layers.Dense(27, activation='softmax', name='lvl3')(fullylvl3)

        model = tf.keras.Model(inputs=inputs, outputs=[outlvl1,outlvl2,outlvl3], name="generate_model_with_parameters")

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics='accuracy')
        return model

    # Générer le modèle TensorFlow avec les paramètres spécifiés
    model = generate_model_with_parameters(conv_kernels, dense_neurons, conv_layers, dense_layers, height_image, width_image, channels_image)

    model.save(paths.modeling_path+'model')  # Save the model to disk

    # Capturer le résumé du modèle sous forme de chaîne de caractères
    buffer = io.StringIO()
    model.summary(print_fn=lambda x: buffer.write(x + "\n"))
    model_summary_string = buffer.getvalue()

    return jsonify(message='<span style="color: green;">The custom model is successfully generated.</span>', model_summary=model_summary_string), 200

