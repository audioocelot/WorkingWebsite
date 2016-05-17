/*
    Script to upload audio file with ajax,
 */
$('#submit-audio-upload').on('click', function (event) {
    uploadAudioFile(event);
});


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
            console.log(response);
            $('#response-form').show();
            $('#fileIsUploaded').text(response['genres'][0][0] + " : " + response['genres'][0][1]+"%, " + response['genres'][1][0] +" : "+ response['genres'][1][1] + "%, " + response['genres'][2][0] + " : " + response['genres'][2][1] + "%");
            response['songs'].forEach(function(song, index) {
                $('#uploadedPlaylist').append("<li>" + song['artist_name'] + " - " + song['title'] + "</li>");
            });
        },
        error: function (response) {
            console.log(response);
        }
    })

}