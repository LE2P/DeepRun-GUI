from app import app
from flask import jsonify

# Check tensorrt
@app.route('/check-tensorrt')
def check_tensorrt():
    installed_tensorrt = False
    version_tensorrt = None
    try:
        def import_tensorrt():
            import tensorrt
            installed_tensorrt = True
            version_tensorrt = tensorrt.__version__
            return installed_tensorrt, version_tensorrt
        installed_tensorrt, version_tensorrt = import_tensorrt()
    except ImportError:
        pass

    return jsonify({'installed': installed_tensorrt, 'version': version_tensorrt})

# Check tensorflow
@app.route('/check-tensorflow')
def check_tensorflow():
    installed_tf = False
    version_tf = None
    gpu = False
    name_gpu = ''
    try:
        def import_tf():
            import tensorflow as tf
            installed_tf = True
            version_tf = tf.__version__
            gpu = False
            name_gpu = ''
            if tf.config.list_physical_devices('GPU'):
                gpu = True
                name_gpu = tf.test.gpu_device_name()
            return installed_tf, version_tf, gpu, name_gpu
        installed_tf, version_tf, gpu, name_gpu = import_tf()
    except ImportError:
        pass

    return jsonify({'installed': installed_tf, 'version': version_tf, 'gpu': gpu, 'name_gpu': name_gpu}) 

# Check torch
@app.route('/check-torch')
def check_torch():
    installed_torch = False
    version_torch = None
    gpu = False
    name_gpu = ''
    try:
        def import_torch():
            import torch
            installed_torch = True
            version_torch = torch.__version__
            gpu = False
            name_gpu = ''
            if torch.cuda.is_available():
                gpu = True
                name_gpu = torch.cuda.get_device_name(0)
            return installed_torch, version_torch, gpu, name_gpu
        installed_torch, version_torch, gpu, name_gpu = import_torch()
    except ImportError:
        pass

    return jsonify({'installed': installed_torch, 'version': version_torch, 'gpu': gpu, 'name_gpu': name_gpu})

# Check osgeo
@app.route('/check-gdal')
def check_gdal():
    installed_gdal = False
    version_gdal = None
    try:
        from osgeo import gdal, ogr
        installed_gdal = True
        version_gdal = gdal.__version__
    except ImportError:
        pass

    return jsonify({'installed': installed_gdal, 'version': version_gdal})

# Check geopandas
@app.route('/check-geopandas')
def check_geopandas():
    installed_geopandas = False
    version_geopandas = None
    try:
        import geopandas as gpd
        installed_geopandas = True
        version_geopandas = gpd.__version__
    except ImportError:
        pass

    return jsonify({'installed': installed_geopandas, 'version': version_geopandas})

# Check rasterio
@app.route('/check-rasterio')
def check_rasterio():
    installed_rasterio = False
    version_rasterio = None
    try:
        import rasterio
        installed_rasterio = True
        version_rasterio = rasterio.__version__
    except ImportError:
        pass

    return jsonify({'installed': installed_rasterio, 'version': version_rasterio})

# Check scikit-learn
@app.route('/check-sklearn')
def check_sklearn():
    installed_sklearn = False
    version_sklearn = None
    try:
        import sklearn
        installed_sklearn = True
        version_sklearn = sklearn.__version__
    except ImportError:
        pass

    return jsonify({'installed': installed_sklearn, 'version': version_sklearn})
