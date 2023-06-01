import tensorflow as tf
import zipfile
import os
from settings.paths import paths


class ModelLoader:
    def __init__(self, config_file_path):
        """
        Constructor of the ModelLoader class.

        Args:
            config_file_path (str): Path to the configuration file.
        """
        self.config_file_path = config_file_path
        self.model = None

    def load_model(self):
        """
        Load the model from the configuration file.
        """
        # Check if the file is a zip file, so it can be unzipped
        if self.config_file_path.endswith('.zip'):
            # Unzip the file
            with zipfile.ZipFile(self.config_file_path, 'r') as zip_ref:
                zip_ref.extractall(paths.base_path)
            # Get the name of the unzipped file
            self.config_file_path = os.path.join(paths.base_path, os.path.splitext(os.path.basename(self.config_file_path))[0])
            self.model = tf.keras.models.load_model(self.config_file_path)
        # Check the extension of the file
        if self.config_file_path.endswith('.json'):
            # Reading the model from the JSON configuration file
            with open(self.config_file_path, 'r', encoding='latin-1') as file:
                model_json = file.read()
            self.model = tf.keras.models.model_from_json(model_json)
        elif self.config_file_path.endswith('.yaml'):
            # Reading the model from the YAML configuration file
            with open(self.config_file_path, 'r', encoding='latin-1') as file:
                model_yaml = file.read()
            # Uses the json function because model_from_yaml is deprecated
            self.model = tf.keras.models.model_from_json(model_yaml)
        elif self.config_file_path.endswith(('.hdf5', '.h5', '.hdf', '.hdf4', '.h4', '.he5', '.he4', '.hdfEOS', '.hdfEOS2')):
            # Reading the model from the HDF5 configuration file
            self.model = tf.keras.models.load_model(self.config_file_path)
        elif self.config_file_path.endswith(('.pb', '.pbtxt', '.pbtxt.ascii', '.pbtxt.txt', '.pbtxt.ascii.txt')):
            # Reading the model from the Protobuf configuration file
            self.model = tf.keras.models.load_model(self.config_file_path)
        elif self.config_file_path.endswith(('.ckpt', '.ckpt.index', '.ckpt.data-00000-of-00001', '.index', '.meta')):
            # Reading the model from the TensorFlow checkpoint configuration file
            self.model = tf.keras.models.load_model(self.config_file_path)
        elif self.config_file_path.endswith(('.py', '.pyc')):
            # Reading the model from the Python configuration file
            self.model = tf.keras.models.load_model(self.config_file_path)
        elif self.config_file_path.endswith(('.tflite', '.lite')):
            # Reading the model from the TensorFlow Lite configuration file
            self.model = tf.keras.models.load_model(self.config_file_path)
        elif self.config_file_path.endswith('/'):
            self.model = tf.keras.models.load_model(self.config_file_path)

    def get_model(self):
        """
        Returns the loaded model.

        Returns:
            tf.keras.Model: The loaded model.
        """
        return self.model
    
    def get_model_summary(self):
        """
        Returns the summary of the loaded model.

        Returns:
            str: The summary of the loaded model.
        """
        if self.model is not None:
            return self.model.summary()
        else:
            return "No model loaded"
    
    def get_model_input_shape(self):
        """
        Returns the shape of the input of the loaded model.

        Returns:
            tuple: The shape of the input of the loaded model.
        """
        if self.model is not None:
            return self.model.input_shape
        else:
            return "No model loaded"
    
    def get_model_output_shape(self):
        """
        Returns the shape of the output of the loaded model.

        Returns:
            tuple: The shape of the output of the loaded model.
        """
        if self.model is not None:
            return self.model.output_shape
        else:
            return "No model loaded"
    
    def get_number_of_trainable_parameters(self):
        """
        Returns the number of trainable parameters of the loaded model.

        Returns:
            int: The number of trainable parameters of the loaded model.
        """
        if self.model is not None:
            return self.model.count_params()
        else:
            return "No model loaded"
