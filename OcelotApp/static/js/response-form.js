/**
 * Created by dalewinston on 5/13/16.
 */

//$('optionsRadios').change(function () {
//    console.log('clicked');
//    if ($(this).id = "noRadio") {
//        console.log('clicked');
//    }
//});

//$(document).ready(function() {
//    $('input[type=radio]').change(function() {
//        if($(this).id='noRadio') {
//            console.log('clicked')
//        }
//    });
//});

$('#noRadio').change(function() {
    $('.select-genre').show();
});

$('#submit-response-form').on('click', function(event) {
    submitResponseForm(event);
});

function submitResponseForm(event) {
    event.stopPropagation();
    event.preventDefault();

    var formData =  {
        'features': $('#features-input').val(),
        'correct' : $('input[name=optionsRadios]:checked', '#response-form').val(),
        'genre' : $('#genre-selector').val()
    };
    console.log(formData);
    $.ajax({
        url: '/response',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,

        success: function (resposne) {
            console.log(response);
            $('#response-form').hide();
            $('.thanks-text').show();

        }
    })
}