from app import app
from flask import request, jsonify
from werkzeug.utils import secure_filename
from osgeo import gdal
import rasterio
import os
import re
from settings.paths import paths
import tensorflow as tf
from tools.model_tf import ModelLoader
from tools.multiLevel import MultiLevelPredictor
import math
from tqdm import tqdm
import time
import numpy as np

# Path to the static default model
model_static_path = 'sample/model/49_meso_noTopOfWAve_highHP_n2n3_0,9533_0,9290/bestModel.h5'

# Route for switch position, upload an external model or load a model or use the default model "DeepRun" or "Yolo"
@app.route('/switch_state', methods=['POST'])
def switch_state():
    state = request.json['state']  # Utilisez request.json pour accéder aux données JSON envoyées depuis la requête
    switch_message = ''

    if state == 'upload':
        switch_message = 'Upload selected. Please upload a model file to continue.'
    elif state == 'load':
        # Check if a best_model returned during training phase exists, else stop inference
        if os.path.exists(os.path.join(paths.train_path, 'best_model')):
            switch_message = 'Load selected. Loading best model "'+str(os.path.join(paths.train_path, 'best_model'))+'".'
        else:
            switch_message = 'No model found. Please generate a model first.'
    elif state == 'default':
        # Check if deeprun model is present
        print(model_static_path)
        if os.path.exists(model_static_path):
            # Insert model path into message
            switch_message = 'Default selected. Loading default model "'+str(model_static_path)+'".'
        else:
            switch_message = 'No DeepRun model found. Please contact the administrator.'

    return jsonify({'message': switch_message})

@app.route('/save_model', methods=['POST'])
def save_model():
    model_file = request.files['model-file-upload']
    filename = secure_filename(model_file.filename)
    print(paths.inference_path)
    file_path = os.path.join(paths.inference_path, filename)
    model_file.save(file_path)
    # Extract some parameters from the model to display them in the UI
    loader = ModelLoader(file_path)
    loader.load_model()
    metadata = (" Metada [input size: "+str(loader.get_model_input_shape())+
                " - output size: "+str(loader.get_model_output_shape())+
                " - number of parameters: "+str(loader.get_number_of_trainable_parameters())+"]")
    model_message = f"Model '{filename}' uploaded successfully."+metadata
    return jsonify({'message': model_message})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image_file = request.files['image-file-upload']
    filename = secure_filename(image_file.filename)
    file_path = os.path.join(paths.inference_path, filename)
    image_file.save(file_path)
    switch_message = f"Image '{filename}' uploaded successfully."
    return jsonify({'message': switch_message})

@app.route('/process_image', methods=['POST'])
def process_image():
    load_model_status = request.form.get('loadModelStatus')
    message_image = request.form.get('messageImage')
    state = request.form.get('state')
    print('Load model status is: '+str(load_model_status))
    print('Message image is: '+str(message_image))
    print('State is: '+str(state))
    concat = int(request.form.get('concat'))
    saving = int(request.form.get('saving'))
    pixelRes = float(request.form.get('pixelRes'))
    paddingShift = int(request.form.get('paddingShift'))
    print('Concat is: '+str(concat))
    print('Saving is: '+str(saving))
    print('Pixel resolution is: '+str(pixelRes))
    print('Padding shift is: '+str(paddingShift))

    def extract_text_between_single_quotes(text):
        pattern = r"'(.*?)'"
        matches = re.findall(pattern, text)
        return matches
    
    model_name = extract_text_between_single_quotes(load_model_status)
    image_name = extract_text_between_single_quotes(message_image)

    # 3 Cases, upload a model, load a model or use the default model
    if state == 'upload':
        model_path = os.path.join(paths.inference_path, model_name[0])
    elif state == 'load':
        # Check if best_model returned during training phase exists, else stop inference
        if os.path.exists(os.path.join(paths.training_path, 'best_model')):
            model_path = os.path.join(paths.training_path, 'best_model')
        else:
            return jsonify({'message': 'No model found. Please generate a model first.'})
    elif state == 'default':
        model_path = model_static_path
    print('Model path is: '+model_path)

    # Check if image exists
    if os.path.exists(os.path.join(paths.inference_path, image_name[0])):
        image_path = os.path.join(paths.inference_path, image_name[0])
    else:
        return jsonify({'message': 'No image found. Please upload an image first.'})
    print('Image path is: '+image_path)

    # Inference starts here
    # Load model
    loader = ModelLoader(model_path)
    loader.load_model()
    model = loader.get_model()
    print('Model loaded successfully.')
    print(model.summary())
    
    # Create a generator for prediction
    datagen_X = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    # Load image
    raster = gdal.Open(image_path)
    print('Image loaded successfully.')

    inputsize = loader.get_model_input_shape()
    print('Input size is: '+str(inputsize))
    img_width  = inputsize[1]
    img_height = inputsize[2]
    paddingShift = paddingShift
    print("Image size is %d x %d" %(img_width, img_height))

    # Get image size
    gt     = raster.GetGeoTransform()
    origin = [gt[0],gt[3]]
    raster_xSize = raster.GetRasterBand(1).XSize
    raster_ySize = raster.GetRasterBand(1).YSize
    print('Raster informations loaded')
    print("Xsize = %d and Ysize = %d" %(raster_xSize, raster_ySize))

    #Compute output size following raster size
    def human_format(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    if isinstance(img_height/2,int):
        #Case where tile size is odd - impair
        print("Tile size is odd")
    else:
        #Case where tile size is even - pair
        print("Tile size is even")

    Xout = math.ceil( ((raster_xSize-img_width)+1)/paddingShift )
    Yout = math.ceil( ((raster_ySize-img_height)+1)/paddingShift )
    matrixUnit = Xout * Yout
    print("Xin  = %d and Yin  = %d" %(raster_xSize, raster_ySize))
    print("Xout = %d and Yout = %d" %(Xout, Yout))
    print("Number of predictions:",human_format(matrixUnit))

    # Inference
    concat = concat
    saving = saving
    pixelRes = pixelRes
    start = 0
    predictor = MultiLevelPredictor()
    rasterArrays   = []
    outputAllPred  = []
    outputSavePred = []
    image_name_modified = image_name[0].replace(".", "_")
    # Create save folder specific to the image name
    save_path = paths.inference_path+'output/'+str(image_name[0])+'/'
    # Check if output folder exists, else create it
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print('Start inference at '+time.strftime("%Y-%m-%d %H:%M:%S"))
    start_Totaltime = time.time()
    for yy in tqdm(range(start,Yout)):
        start_time = time.time()
        #Dimensions in meter
        yMin = gt[3]-((paddingShift*pixelRes)*(yy))-(img_height*pixelRes)
        yMax = gt[3]-((paddingShift*pixelRes)*(yy))
        raster = gdal.Open(image_path)

        for xx in range(Xout):
            xMin = gt[0]+((paddingShift*pixelRes)*(xx))
            xMax = gt[0]+((paddingShift*pixelRes)*(xx))+(img_height*pixelRes)
            #Convert raster tile to array, meter to pixel number
            xo = int(round((xMin-gt[0])/pixelRes))
            yo = int(round((gt[3]-yMax)/pixelRes))
            arr = raster.ReadAsArray(xo,yo,img_width,img_height)
            rasterArrays.append(arr.transpose(1, 2, 0))
            
            #Generate tile tiff
            #tile = gdal.Warp(output_path+str(yy)+"_"+str(xx)+'.tiff', raster, format=rasterFormat, outputType=gdal.gdalconst.GDT_Byte,
            #                 outputBounds=[xMin, yMin, xMax, yMax],
            #                xRes=pixelRes, yRes=pixelRes,
            #               dstSRS='EPSG:32740', resampleAlg=None, options=['COMPRESS=NONE'])
        #Input and normalisation data
        if yy == start:
            #Initialize data generator
            X = np.array(rasterArrays).astype('float16')
            datagen_X.fit(X)
        if ((yy%concat==0) and (yy!=start)) | (yy==Yout-1):
            #Input and normalisation data
            X = np.array(rasterArrays).astype('float16')
            #print("X shape : ",X.shape)
            #Predict data with imported model
            outputPred = model.predict(datagen_X.flow(X,batch_size=16,shuffle=False),verbose=0)

            # Check if the output is more than 1 dimension
            if len(outputPred) > 1:
                hierarchical = predictor.predictlevel(outputPred)
                Yhat_format = np.reshape(hierarchical[2], (-1,Xout))
            else:
                Yhat_format = np.reshape(outputPred, (-1,Xout))
            tf.keras.backend.clear_session()
            #Concatenate for txt save
            outputSavePred.append(Yhat_format)
        
            if (yy%saving==0) and (yy!=start):
                #Write the Line Yhat_format
                np.save(save_path+str(int(yy/100))+'.npy',np.vstack(outputSavePred))
                #Clear output
                outputSavePred.clear()
            
            #Clear tiles data
            rasterArrays.clear()
            del X
        
            end_time = time.time()
            hours, rem = divmod(end_time-start_time,3600)
            minutes, seconds = divmod(rem,60)
            
        #     print("Iteration "+str(yy)+", "+
            #          "time computation "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)+", "+
            #         "remaining "+str(int((Yout/1)-yy))+" iterations, "+
            #        "estimated time "+ str( ((end_time-start_time)/3600) *((Yout/concat)-(yy/concat)) )+" hours.")

    np.save(save_path+str(int(Yout/saving)+1)+'.npy',np.vstack(outputSavePred))

    end_time = time.time()
    days, remd = divmod(end_time-start_Totaltime,86400)
    hours, remh = divmod(remd,3600)
    minutes, seconds = divmod(remh,60)
    print("Total time "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    print('[6/10] End inference at '+time.strftime("%Y-%m-%d %H:%M:%S"))

    inference_message = f"The inference process is complete. Inference parts are saved into this folder: {save_path}"
    return jsonify({'message': inference_message})
