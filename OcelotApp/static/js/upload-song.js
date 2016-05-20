/*
    Script to upload audio file with ajax,
 */
$('#submit-audio-upload').on('click', function (event) {
    document.getElementById('yesRadio-upload').checked=true;
    $('#select-genre-upload').hide();
    $('#response-form-upload').hide();
    $('#thanks-text-upload').hide();
    uploadAudioFile(event);
});
var deletedOption = "";
function uploadAudioFile(event) {
    event.stopPropagation();
    event.preventDefault();
    $('#fileIsUploaded').text('');

    var data = new FormData($('#audio-upload')[0]);
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
            $('#features-input-upload').val(response['features']);
            $('#features-genre-upload').val(response['genres'][0][0]);
            var genreObject=document.getElementById("genre-selector-upload")
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
            $('#response-form-upload').show();
            $('#fileIsUploaded').text(response['genres'][0][0] + " : " + response['genres'][0][1]+"%, " + response['genres'][1][0] +" : "+ response['genres'][1][1] + "%, " + response['genres'][2][0] + " : " + response['genres'][2][1] + "%");
            var ul = document.getElementById('uploadedPlaylist');
            if (ul){
                while (ul.firstChild) {
                    ul.removeChild(ul.firstChild);
                }
            }
            response['songs'].forEach(function(song, index) {
                $('#uploadedPlaylist').append("<li>" + song['artist_name'] + " - " + song['title'] + "</li>");
            });
        },
        error: function (response) {
            console.log(response);
        }
    })

}