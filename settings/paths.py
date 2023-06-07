import os

# Routes
routes_path =     'static/img/'
# Base path
base_path =        'tmp/'
# Main folders
modeling_folder =  'modeling/'
train_folder =     'train/'
inference_folder = 'inference/output/'
# Tools folders
config_folder =    'config/'
metadata_folder =  'metadata/'

class Paths:
    def __init__(self, base_path):
        self.base_path = base_path
        self.routes_path = routes_path

        self.modeling_path = None
        self.train_path = None
        self.inference_path = None

        self.config_path = None
        self.metadata_path = None

    def create_directories(self):
        self.modeling_path = os.path.join(self.base_path, modeling_folder)
        self.train_path = os.path.join(self.base_path, train_folder)
        self.inference_path = os.path.join(self.base_path, inference_folder)
        
        self.config_path = os.path.join(self.base_path, config_folder)
        self.metadata_path = os.path.join(self.config_path, metadata_folder)

        os.makedirs(self.routes_path, exist_ok=True)

        os.makedirs(self.modeling_path, exist_ok=True)
        os.makedirs(self.train_path, exist_ok=True)
        os.makedirs(self.config_path, exist_ok=True)
        os.makedirs(self.inference_path, exist_ok=True)

        os.makedirs(self.metadata_path, exist_ok=True)


# Create directories
paths = Paths(base_path)
paths.create_directories()

# Create an empty log file at each start of the server, TODO: add a log file for each session or the whole server
log_file = os.path.join(paths.config_path, 'log.txt')
with open(log_file, 'w') as f:
    f.write('')


