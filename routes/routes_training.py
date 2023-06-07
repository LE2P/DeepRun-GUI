from app import app
from flask import jsonify, request
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from settings.paths import paths
from tools.model_tf import ModelLoader
from tools.cirad_legend import CiradLegend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import math

randomID = None

@app.route('/check-model')
def check_model():
    path_model = paths.modeling_path + 'model/'
    print(path_model)
    #Check if the folder exists, if not send a message
    try:
        if not os.path.exists(path_model):
            return jsonify({'message': 'No model found. Please generate a model first.'})
        else:
            return jsonify({'message': 'Model "'+str(path_model)+'" found.'})
    except ImportError:
        pass

@app.route('/upload_x', methods=['POST'])
def upload_x():
    global randomID
    file = request.files['x_file']
    file.save(paths.train_path+'X.npy')  # Save the file to the path

    # Load the data from the NPY file
    data = np.load(paths.train_path+'X.npy')

    # Get a global random value
    array_size = data.shape[0]
    randomID = random.randint(0, array_size - 1)

    # Generate a plot of the image (assuming grayscale image)
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.imshow(data[randomID])
    ax.axis('off')

    # Save the plot as an image file
    img_path = paths.routes_path + 'sample_plot-x.png'
    canvas.print_figure(img_path, dpi=80)

    return jsonify({'message': 'X uploaded successfully.'})

@app.route('/upload_y', methods=['POST'])
def upload_y():
    file = request.files['y_file']
    file.save(paths.train_path+'Y.npy')

    # Load the data from the NPY file
    data = np.load(paths.train_path+'Y.npy')
    if data.shape[1] > 3:
        #keep last 3 columns
        data = data[:,-3:]
    # Get labels from CIRAD legend
    cirad = CiradLegend()
    classes = data[randomID]
    print(classes)
    legend = cirad.get_legend(classes)
    print(legend)

    return jsonify({'message': 'Y uploaded successfully.', 'label': legend})

@app.route('/replot', methods=['GET'])
def replot():
    # Reload dataset
    data_x = np.load(paths.train_path+'X.npy')
    data_y = np.load(paths.train_path+'Y.npy')
    if data_y.shape[1] > 3:
        #keep last 3 columns
        data_y = data_y[:,-3:]
    print(data_x.shape)
    print(data_y.shape)

    # Get a global random value
    array_size = data_x.shape[0]
    randomID = random.randint(0, array_size - 1)
    print(randomID)

    # Get labels from CIRAD legend
    cirad = CiradLegend()
    classes = data_y[randomID]
    print(classes)
    legend = cirad.get_legend(classes)
    print(legend)

    # Generate a plot of the image (assuming grayscale image)
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.imshow(data_x[randomID])
    ax.axis('off')

    # Save the plot as an image file
    img_path = paths.routes_path + 'sample_plot-x.png'
    print(img_path)
    canvas.print_figure(img_path, dpi=80)

    response = {
        'label': legend,  # Mettez à jour avec le nouveau label
        'image_url': paths.routes_path+'sample_plot-x.png'  # Mettez à jour avec le nouvel emplacement de l'imagette
    }
    
    print(response)

    return jsonify(response)

@app.route('/train', methods=['POST'])
def train_model():
    # Vérifier si les fichiers X et Y existent
    if not os.path.exists(paths.train_path + 'X.npy') or not os.path.exists(paths.train_path + 'Y.npy'):
        print('Please upload input files X and Y.')
    
    epoch = int(request.json['epochs'])
    batch_size = int(request.json['batch_size'])
    train_split = float(request.json['train_split'])
    val_split = float(request.json['validation_split'])
    optimizer = request.json['optimizer']
    learning_rate = float(request.json['learning_rate'])
    data_used = float(request.json['data_use'])

    print('optimizer : '+str(optimizer))

    train_size = train_split
    val_size = val_split/train_split

    # Charger les fichiers d'entrée X et Y
    X = np.load(paths.train_path + 'X.npy')
    Y = np.load(paths.train_path + 'Y.npy')
    print('[1/6] Data correctly loaded.')

    # Check if y is superior to 3 columns
    if Y.shape[1] > 3:
        #keep last 3 columns
        Y = Y[:,-3:]

    X, XX, Y, YY = train_test_split(X, Y, train_size=data_used, shuffle=True)
    del XX, YY
    Xtrain, Xrem, Ytrain, Yrem = train_test_split(X, Y, train_size=train_size, shuffle=True)
    Xval, Xtest, Yval, Ytest = train_test_split(Xrem, Yrem, train_size=val_size, shuffle=True)

    print("X shape :"+str(X.shape))
    print("Y shape :"+str(Y.shape))
    print("Xtrain shape :"+str(Xtrain.shape))
    print("Ytrain shape :"+str(Ytrain.shape))
    print("Xval shape :"+str(Xval.shape))
    print("Yval shape :"+str(Yval.shape))
    print("Xtest shape :"+str(Xtest.shape))
    print("Ytest shape :"+str(Ytest.shape))

    Ytrain_cat = [tf.keras.utils.to_categorical(Ytrain[:,a]-1, dtype='uint8') for a in range(Ytrain.shape[1])]
    Yval_cat = [tf.keras.utils.to_categorical(Yval[:,a]-1, dtype='uint8') for a in range(Yval.shape[1])]
    Ytest_cat = [tf.keras.utils.to_categorical(Ytest[:,a]-1, dtype='uint8') for a in range(Ytest.shape[1])]

    print("Ytrain_cat level 1 shape :"+str(Ytrain_cat[0].shape))
    print("Yval_cat level 2 shape :"+str(Yval_cat[1].shape))
    print("Ytest_cat level 3 shape :"+str(Ytest_cat[2].shape))

    # Load the model
    model_path = paths.modeling_path + 'model/'
    model = tf.keras.models.load_model(model_path)
    print(model)
    print('[2/6] Model correctly loaded.')

    # Change optimizer adam, sgd, rmsprop, adagrad, adadelta, adamax, nadam, ftrl
    if optimizer == 'adam':
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate,
                                                beta_1=0.9, beta_2=0.999, epsilon=1e-07)
    elif optimizer == 'sgd':
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, 
                                            momentum=0.0, nesterov=False)
    elif optimizer == 'rmsprop':   
        optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
    elif optimizer == 'adagrad':
        optimizer = tf.keras.optimizers.Adagrad(learning_rate=learning_rate, 
                                                initial_accumulator_value=0.1, epsilon=1e-07)
    elif optimizer == 'adadelta':
        optimizer = tf.keras.optimizers.Adadelta(learning_rate=learning_rate, 
                                                    rho=0.95, epsilon=1e-07)
    elif optimizer == 'adamax':
        optimizer = tf.keras.optimizers.Adamax(learning_rate=learning_rate, 
                                                beta_1=0.9, beta_2=0.999, epsilon=1e-07)
    elif optimizer == 'nadam':
        optimizer = tf.keras.optimizers.Nadam(learning_rate=learning_rate, 
                                                beta_1=0.9, beta_2=0.999, epsilon=1e-07)
    elif optimizer == 'ftrl':
        optimizer = tf.keras.optimizers.Ftrl(learning_rate=learning_rate, 
                                                learning_rate_power=-0.5, 
                                                initial_accumulator_value=0.1, 
                                                l1_regularization_strength=0.0, 
                                                l2_regularization_strength=0.0, 
                                                l2_shrinkage_regularization_strength=0.0)
    else:
        pass
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics='accuracy')
    print('[3/6] Model correctly loaded.')

    # Define callbacks early stopping and model checkpoint
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_lvl3_accuracy', patience=int(epoch/10), restore_best_weights=True)
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=paths.train_path+'/model_checkpoint/'+'model_'+'checkpoint-epoch-{epoch:02d}', 
                                                            save_freq='epoch',  # Fréquence de sauvegarde (à chaque époque)
                                                            save_best_only=False,  # Sauvegarder uniquement le meilleur modèle
                                                            save_weights_only=False)  # Sauvegarder le modèle complet (architecture + poids))
    print('[4/6] Callbacks defined.')

    # Train the model with callbacks
    model.fit(Xtrain, 
                {'lvl1':Ytrain_cat[0],'lvl2':Ytrain_cat[1],'lvl3':Ytrain_cat[2]},
                epochs=epoch, 
                batch_size=batch_size, 
                validation_data=(Xval, Yval_cat),
                callbacks=[early_stopping, model_checkpoint],
                verbose=1)
    print('[5/6] Model trained.')

    # Save the best model
    model.save(paths.train_path+"/best_model")
    print('[6/6] Best model saved.')

    # Test the model
    perfs = model.evaluate(Xtest, Ytest_cat, verbose=1)
    print(perfs)
    loss1 = perfs[1]
    loss2 = perfs[2]
    loss3 = perfs[3]
    acc1 = perfs[4]
    acc2 = perfs[5]
    acc3 = perfs[6]

    round_acc3 = round(acc3, 2)

    return jsonify({'message': 'Training completed successfully.'+ 
                    ' Accuracy of the last level: '+str(round_acc3)+', with '+
                    str(epoch)+' epochs and '+
                    str(data_used*100)+'% of data'})

    