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
        success: function (response) {
            console.log(response);
            $('#fileIsUploaded').text(response['genres'][0] + ", " + response['genres'][1]);
            response['songs'].forEach(function(song, index) {
                $('#uploadedPlaylist').append("<li>" + song['artist_name'] + " - " + song['title'] + "</li>");
            });
        },
        error: function (response) {
            console.log(response);
        }
    })

}