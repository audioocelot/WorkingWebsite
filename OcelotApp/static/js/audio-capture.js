/*
 Capture the audio input through the browser
 Uses recorder.js

 */
var audio_context;
var recorder;
var timeoutID;

function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    console.log('Media stream created.');

    recorder = new Recorder(input);
    console.log('Recorder initialised.');
}

function startRecording(button) {
    recorder && recorder.record();
    button.disabled = true;
    $('#isUploaded').text("");
    var i = 0;
    var counter = setInterval(function () {
        i++;
        if (i < 100) {
            $('.progress-bar').css('width', i + '%');
        } else {

            clearTimeout(counter);
        }
    }, 200);

    timeoutID = window.setTimeout(stopRecording, 20500, button);
    console.log('Recording...');
}

function cancelRecording() {
    window.clearTimeout(timeoutID);
}

function stopRecording(button) {
    recorder && recorder.stop();
    console.log('Stopped recording.');
    button.disabled = false;
    // create WAV download link using audio data blob
    createDownloadLink();
    recorder.clear();
}

function createDownloadLink() {
    recorder && recorder.exportWAV(function (blob) {
        var data = new FormData();

        var filename = $.now() + '.wav';

        data.append('audio', blob, filename);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: data,
            contentType: false,
            processData: false,
            beforeSend: function(){
                document.getElementsByClassName('loading')[0].style.visibility='visible';
            },
            complete: function(){
                document.getElementsByClassName('loading')[0].style.visibility='hidden';
            },
            success: function (response) {
                $('.progress-bar').css('width', '0%');
                console.log(response);
                $('#response-form').show();
                $('#fileIsUploaded').text(response['genres'][0][0] + " : " + response['genres'][0][1]+"%, " + response['genres'][1][0] +" : "+ response['genres'][1][1] + "%, " + response['genres'][2][0] + " : " + response['genres'][2][1] + "%");
                response['songs'].forEach(function (song, index) {
                    $('#recordedPlaylist').append("<li>" + song['artist_name'] + " - " + song['title'] + "</li>");
                });
                //var url = data;
                //var li = document.createElement('li');
                //var au = document.createElement('audio');
                //var hf = document.createElement('a');
                //
                //au.controls = true;
                //au.src = url;
                //hf.href = url;
                ////hf.download = new Date().toISOString() + '.wav';
                //hf.innerHTML = hf.download;
                //li.appendChild(au);
                //li.appendChild(hf);
                //$("#recordingsList").append(li)
            },
            error: function (response) {
                console.log(response);
            }
        });
    });
}

window.onload = function init() {
    try {
        // Get the user media
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
        console.log('Audio context set up.');
        console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
        alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function (e) {
        console.log('No live audio input: ' + e);
    });
};