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
    document.getElementById('yesRadio-record').checked=true;
    $('#select-genre-upload').hide();
    $('#response-form-uplaod').hide();
    $('#thanks-text-upload').hide();
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
                $('#features-input-record').val(response['features']);
                $('#features-genre-record').val(response['genres'][0][0]);
                var genreObject=document.getElementById("genre-selector-record")
                for (var i=0; i<genreObject.length; i++){
                    if (genreObject.options[i].value == response['genres'][0][0]){
                        if(deletedOption != ""){
                            var opt = document.createElement('option');
                            opt.value = deletedOption;
                            opt.innerHTML = deletedOption.charAt(0).toUpperCase()+deletedOption.slice(1);
                            genreObject.appendChild(opt);
                            deletedOption = genreObject.options[i].value
                            genreObject.remove(i);
                        } else{
                            deletedOption = genreObject.options[i].value;
                            genreObject.remove(i);  
                        }
                    }
                }
                $('#response-form-record').show();
                $('#isUploaded').text(response['genres'][0][0] + " : " + response['genres'][0][1]+"%, " + response['genres'][1][0] +" : "+ response['genres'][1][1] + "%, " + response['genres'][2][0] + " : " + response['genres'][2][1] + "%");
                var ul = document.getElementById('recordedPlaylist');
                if (ul){
                    while (ul.firstChild) {
                        ul.removeChild(ul.firstChild);
                    }
                }
                response['songs'].forEach(function (song, index) {
                    $('#recordedPlaylist').append("<li>" + song['artist_name'] + " - " + song['title'] + "</li>");
                });
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