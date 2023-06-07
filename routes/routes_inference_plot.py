from app import app
import os
from flask import jsonify, request
from settings.paths import paths
from osgeo import gdal
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tools.cirad_legend import CiradLegend

@app.route('/get_subfolders')
def get_subfolders():
    # Give the path of the folder containing the subfolders
    folder_path = paths.inference_path+"output/"

    # Get the list of all files and directories
    subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

    return jsonify(subfolders)

@app.route('/get_subfolder_info', methods=['POST'])
def get_subfolder_info():
    folder = request.form['folder']
    folder_path = os.path.join(paths.inference_path+"output/", folder)  # Update folder path

    num_items = 0
    total_size = 0

    for root, dirs, files in os.walk(folder_path):
        num_items += len(dirs) + len(files)
        total_size += sum(os.path.getsize(os.path.join(root, name)) for name in files)

    response = {
        'numItems': num_items,
        'totalSize': total_size
    }

    return jsonify(response)

@app.route('/get_all_tiff_files', methods=['POST'])
def get_all_tiff_files():
    tiff_files = []
    folder_path = paths.inference_path

    for file in os.listdir(folder_path):
        if file.endswith('.tiff') or file.endswith('.tif'):
            tiff_files.append(file)
    return jsonify(tiff_files)

@app.route('/get_image_metadata', methods=['POST'])
def get_image_metadata():
    image = request.form.get('image')
    print('Image: ', image)
    image_path = os.path.join(paths.inference_path, image)
    # Get tiff image metadata
    dataset = gdal.Open(image_path)
    origin_x = dataset.GetGeoTransform()[0]
    origin_y = dataset.GetGeoTransform()[3]
    crs = dataset.GetProjection()
    return jsonify({'origins': f'({origin_x}, {origin_y})', 'crs': crs})

@app.route('/save_image', methods=['POST'])
def save_image():
    subfolder = request.form.get('folder')
    filename = request.form.get('image')
    fileformat = request.form.get('format')
    img_width = int(request.form.get('imgWidth'))
    img_height = int(request.form.get('imgHeight'))
    pixelRes = float(request.form.get('pixelRes'))
    # img_width = 25; img_height = 25; pixelRes = 0.5; filename = 'ptile.tif'
    print('Subfolder: ', subfolder)
    print('Filename: ', filename)
    print('Fileformat: ', fileformat)
    print('Image width: ', img_width)
    print('Image height: ', img_height)
    print('Pixel resolution: ', pixelRes)

    # Check if filename and subfolder have the same name, if not probably the src will be wrong, so stop the process
    print(filename)
    print(subfolder)
    if filename != subfolder:
        return jsonify({'message': 'The filename and subfolder must have the same src. Please check the name of the subfolder and the name of the file.'})
    else:
        output_path = os.path.join(paths.inference_path+"output/", subfolder+'/')  # Update folder path
        raster_path = os.path.join(paths.inference_path, filename)  # Update image path
        # output_path = 'tmp/inference/output/ptile.tif/'; raster_path = 'tmp/inference/ptile.tif'
        print('Output path: ', output_path)
        print('Raster path: ', raster_path)

        #Sort files
        numbers = re.compile(r'(\d+)')
        def numericalSort(value):
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts

        # Get pwd
        pwd = os.getcwd()
        print('PWD: ', pwd)
        os.chdir(output_path)
        print('PWD: ', os.getcwd())
        classif = []

        #Load numpy file
        for infile in sorted(glob.glob('*.np[yz]'), key=numericalSort):
            print("Current File Being Processed is: " + infile)
            brut = np.load(infile,allow_pickle=True).astype(int)
            classif.append(brut+1)
        data_plot = np.vstack(classif)
        del classif

        # Return to pwd
        os.chdir(pwd)
        print('PWD: ', os.getcwd())

        if fileformat == 'tiff' or fileformat == 'tif':
            
            #Load raster to get emprise
            raster = gdal.Open(raster_path)
            print('Raster: ', raster_path)
            #Recuperer emprise du raster complet
            gt     = raster.GetGeoTransform()
            print('GeoTransform: ', gt)
            sr     = raster.GetProjection()
            print('Projection: ', sr)
            origin = [gt[0],gt[3]]
            print('Origin: ', origin)

            #Make geotransform
            xmin,ymax = [origin[0]+(((img_width/2))*pixelRes),origin[1]-(((img_height/2))*pixelRes)]
            raster_size = np.shape(data_plot)
            nrows,ncols = raster_size
            xres = pixelRes
            yres = pixelRes
            geotransform = (xmin,xres,0,ymax,0, -yres)

            #Write output
            driver = gdal.GetDriverByName('Gtiff')
            dataset = driver.Create(output_path+'inference_'+filename.split('.')[0]+".tiff", ncols, nrows, 1, gdal.GDT_Byte)
            dataset.SetGeoTransform(geotransform)
            dataset.SetProjection(sr)
            dataset.GetRasterBand(1).WriteArray(data_plot)
            dataset = None

        elif fileformat == 'png':

            # Définir les étiquettes et les couleurs
            cirad = CiradLegend()
            labels, colors = cirad.get_color_legend()
            patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]

            # Save png plot
            plt.imshow(data_plot)
            # add a custom legend
            plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.2, 1), ncol=1, fontsize='small')
            plt.savefig(output_path+'inference_'+filename.split('.')[0]+".png")
            
        # Return success message and imagePath
        return jsonify({'message': 'Image saved successfully! Location of the assembled image: '+output_path+'inference_'+filename+".tiff"})






