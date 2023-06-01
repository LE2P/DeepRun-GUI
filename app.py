from flask import Flask, render_template
import os
import logging
from settings.paths import Paths

app = Flask(__name__)
app.logger.setLevel(logging.ERROR)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/config')
def config():
    return render_template("config.html")
# Import routes for config buttons checking
from routes.routes_config import *

@app.route('/modeling')
def modeling():
    return render_template("modeling.html")
#  Import routes for modeling phase
from routes.routes_modeling import *

@app.route('/training')
def training():
    return render_template("training.html")
# Import routes for training phase
from routes.routes_training import *

@app.route('/metadata')
def metadata():
    return render_template("metadata.html")
# Import routes for metadata tiff checking
from routes.routes_metadata import *

@app.route('/inference')
def inference():
    return render_template("inference.html")
# Import routes for inference phase
from routes.routes_inference import *

@app.route('/inference_plot')
def inference_plot():
    return render_template("inference_plot.html")
# Import routes for inference phase
from routes.routes_inference_plot import *

if __name__ == '__main__':
    app.run(debug=True)