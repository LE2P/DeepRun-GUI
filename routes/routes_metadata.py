from app import app
from flask import request, jsonify
from osgeo import gdal
import os
from settings.paths import paths

@app.route('/upload_image_metadata', methods=['POST'])
def upload_image_metadata():
    file = request.files['image']
    file.save(paths.metadata_path+'image_metadata.tif')  # Save the file to the path
    return jsonify({'message': 'Image uploaded successfully.'})

@app.route('/process_image_metadata', methods=['POST'])
def process_image_metadata():
    file = request.files['image']
    file_path = paths.metadata_path+'image_metadata.tif'  # Path of the uploaded file
    if file_path:
        try:
            dataset = gdal.Open(file_path)
            if dataset is None:
                return jsonify({'error': 'Unable to open the image file.'})

            # Récupérer les informations de géoréférencement
            metadata = {
                'File name': file.filename,
                'Width': dataset.RasterXSize,
                'Height': dataset.RasterYSize,
                'Number of bands': dataset.RasterCount,
                'Pixel width (resolution)': dataset.GetGeoTransform()[1],
                'Pixel height (resolution)': dataset.GetGeoTransform()[5],
                'Projection system': dataset.GetProjection(),
                'Geotransform coordinates': dataset.GetGeoTransform(),
                'Upper left x (reference)': dataset.GetGeoTransform()[0],
                'Upper left y (reference)': dataset.GetGeoTransform()[3],
                'Lower right x': dataset.GetGeoTransform()[0] + dataset.GetGeoTransform()[1] * dataset.RasterXSize,
                'Lower right y': dataset.GetGeoTransform()[3] + dataset.GetGeoTransform()[5] * dataset.RasterYSize,
                'Right-of-way area': (dataset.GetGeoTransform()[1] * dataset.RasterXSize) * (dataset.GetGeoTransform()[5] * dataset.RasterYSize)
            }               
            dataset = None  # Fermer le fichier
            return jsonify({'metadata': metadata})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'No file selected.'})