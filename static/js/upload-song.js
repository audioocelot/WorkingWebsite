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
            $('#fileIsUploaded').text('Audio file is uploaded')
        },
        error: function () {
            console.log('fail');
        }
    })

}