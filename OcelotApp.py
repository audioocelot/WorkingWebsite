from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask.ext.uploads import UploadSet, AUDIO, configure_uploads

import ExtractData


app = Flask(__name__)
# mongo = PyMongo(app)

app.config['MONGO_DBNAME'] = 'audio'
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
audio = UploadSet('audio', AUDIO)
configure_uploads(app, (audio,))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        url = audio.url(filename)  # URL of the uploaded file, need to save this in a database
        # Create a template to show the audio clip and let the user play it so they know that it has been uploaded
        # this will be a temporary feature
        # acutally just used javascript to create an <audio> tag with the url as the src so they can play the file
        # just for
        data = ExtractData.getData('/uploads/audio/' + filename)
        # mongo.db.extracted.insert(data)
        return jsonify({"success": data})
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html",
                           title="Home")


if __name__ == "__main__":
    app.secret_key = 'ocelot key'
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
