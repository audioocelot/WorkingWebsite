/**
 * Created by dalewinston on 5/13/16.
 */

$('#noRadio-upload').change(function() {
    $('#select-genre-upload').show();
});
$('#noRadio-record').change(function() {
    $('#select-genre-record').show();
});
$('#yesRadio-upload').change(function() {
    $('#select-genre-upload').hide();
});
$('#yesRadio-record').change(function() {
    $('#select-genre-record').hide();
});

$('#submit-response-form-upload').on('click', function(event) {
    if(document.getElementById('yesRadio-upload').checked){
        var formData = {
            'features': $('#features-input-uplaod').val(),
            'correct' : document.getElementById('yesRadio-upload').checked,
            'genre' : $('#features-genre').val()
        };
    } else {
        var formData = {
            'features': $('#features-input').val(),
            'correct' : document.getElementById('yesRadio-upload').checked,
            'genre' : $('#genre-selector-upload').val()
        };
    }
    submitResponseForm(event,formData);
});
$('#submit-response-form-record').on('click', function(event) {
    if(document.getElementById('yesRadio-record').checked){
        var formData = {
            'features': $('#features-input-record').val(),
            'correct' : document.getElementById('yesRadio-record').checked,
            'genre' : $('#features-genre-record').val()
        };
    } else {
        var formData = {
            'features': $('#features-input-record').val(),
            'correct' : document.getElementById('yesRadio-record').checked,
            'genre' : $('#genre-selector-record').val()
        };
    }
    submitResponseForm(event,formData);
});

function submitResponseForm(event,formData) {
    event.stopPropagation();
    event.preventDefault()
    $.ajax({
        url: '/response',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(formData),
        contentType: false,
        processData: false,
        beforeSend: function(){
            document.getElementsByClassName('loading')[0].style.visibility='visible';
        },
        complete: function(){
            document.getElementsByClassName('loading')[0].style.visibility='hidden';
            $('#response-form-upload').hide();
            $('#response-form-record').hide();
            $('#thanks-text-upload').show();
            $('#thanks-text-record').show();
        },
        error: function (response) {
            console.log(response);
        }
    })
}