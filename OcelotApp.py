from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask.ext.uploads import UploadSet, AUDIO, configure_uploads
import pickle
import subprocess
import time

import ExtractDataSingle
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config['UPLOADS_DEFAULT_DEST'] = app.root_path + '/uploads'
audio = UploadSet('audio', ('wav', 'mp3'))
configure_uploads(app, (audio,))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        if filename.endswith('mp3'):
            filename = convert_mp3(filename)
        # url = audio.url(filename)  # URL of the uploaded file, need to save this in a database
        data = ExtractDataSingle.getData(app.root_path + '/uploads/audio/' + filename)
        network_file = open('NN.pybrain.net', 'r')
        net = pickle.load(network_file)
        result = net.activate(data)
        network_file.close()
        categories_sorted = category_sorted(result)
        return str(categories_sorted)
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html",
                           title="Home")


def convert_mp3(f):
    prefix = 'uploads/audio/'
    filename = str(time.time()) + '.wav'
    original = app.root_path + '/uploads/audio/' + f
    s = ['sox', original, prefix + filename, 'trim', '30', '20']
    subprocess.call(s)
    return filename


def category_sorted(results):
    result_tuples = [['Hip Hop', 0],['Jazz', 0],['Classical', 0],['Country', 0],['Dance', 0],['Metal', 0],['Reggae', 0],['Rock', 0]]
    for i in range(8):
        result_tuples[i][1] = "{:2.0f}".format(results[i] * 100)
    result_tuples = sorted(result_tuples, key=lambda l: l[1], reverse=True)
    categories_in_order = list()
    for category, value in result_tuples:
        categories_in_order.append(category)
    return result_tuples

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    app.secret_key = 'ocelot key'
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
