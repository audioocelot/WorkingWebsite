from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask.ext.uploads import UploadSet, AUDIO, configure_uploads
from logging.handlers import RotatingFileHandler
import numpy as np
import csv
from subprocess import Popen, PIPE, call
import time
import logging
import pyen
import os
import json
import wave
import contextlib
from mutagen.mp3 import MP3

app = Flask(__name__)

app.config['UPLOADS_DEFAULT_DEST'] = app.root_path + '/uploads'
audio = UploadSet('audio', ('wav', 'mp3'))
configure_uploads(app, (audio,))

en = pyen.Pyen("QV529CKKM503STIOH")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        deleteMe = app.root_path + '/uploads/audio/' + filename[:-3]+'wav'
        if filename.endswith('mp3'):
            filename = process_mp3(filename)
        else:
            filename = process_wav(filename)
        # URL of the uploaded file, need to save this in a database
        url = audio.url(filename)
        p = Popen(
            [
                'python',
                '/home/ubuntu/OcelotApp/NewExtractAndTestDataSingle.py',
                "{}".format(filename)
            ], stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        output, err = p.communicate()
        genres = [x.split(':') for x in output.split(',')]
        print(genres)
        response = get_playlist(genres)
        response['genres'] = genres
        d = ['rm', deleteMe]
        # call(d)
        return jsonify(response)
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html",
                           title="Home")


def process_mp3(f):
    prefix = 'uploads/audio/'
    original = app.root_path + '/uploads/audio/' + f
    trimed = app.root_path + '/uploads/audio/' + 'temp.wav'
    audio = MP3(original)
    if audio.info.length > 20:
        s = ['sox', original, trimed, 'trim', '0', '20']
        call(s)
        c = ['sox', trimed, original[:-3]+'wav']
        call(c)
        d = ['rm', original]
        call(d)
        return f[:-3]+'wav'
    else:
        raise ValueError(
            'Song is too short, please make song at least 20 seconds'
        )


def process_wav(f):
    prefix = 'uploads/audio/'
    original = app.root_path + '/uploads/audio/' + f
    trimed = app.root_path + '/uploads/audio/' + 'temp.wav'
    delete = False
    with contextlib.closing(wave.open(original, 'r')) as ff:
        frames = ff.getnframes()
        rate = ff.getframerate()
        duration = frames / float(rate)
        if duration > 20:
            s = ['sox', original, trimed, 'trim', '0', '20']
            call(s)
            t = ['sox', trimed, original]
            call(t)
            return f
        else:
            delete = True
    if delete:
        d = ['rm', original]
        call(d)
        raise ValueError(
            'Song is too short, please make song at least 20 seconds'
        )


def GetFeatures(path):
    with open(path,
              'rb') as genreFile:
        genreSamples = csv.reader(genreFile)
        floatSample = []
        sample = next(genreSamples)
        for feature in sample[1:385]:
            floatSample.append(float(feature))
        return np.array(floatSample)


def get_playlist(categories):
    return en.get('playlist/static', type='genre-radio', genre=[categories[0][0], categories[1][0]], results=10)

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
    # app.debug = True
    app.run()
