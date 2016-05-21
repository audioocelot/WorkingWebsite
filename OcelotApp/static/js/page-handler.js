/*
 * Page Handler:
 * Handles display and button actions.
 */

(function (window, $) {

    $(function () {


        $('.ripple').on('click', function (event) {
            event.preventDefault();

            var $div = $('<div/>');
            //    btnOffset = $(this).offset(),
            //		xPos = event.pageX - btnOffset.left,
            //		yPos = event.pageY - btnOffset.top;

            $div.addClass('ripple-effect');
            var $ripple = $(".ripple-effect");

            $ripple.css("height", $(this).height());
            $ripple.css("width", $(this).height());
            $div
                .css({
                    //top: yPos - ($ripple.height()/2),
                    //left: xPos - ($ripple.width()/2),
                    background: $(this).data("ripple-color")
                })
                .appendTo($(this));

            window.setTimeout(function () {
                $div.remove();
            }, 2000);
        });

    });

})(window, jQuery);


$(document).ready(function () {
    $('#over-logo').hide();
    $('#button-container').hide();
    $('#over-logo').delay(2000).fadeIn(500);
    $('#button-container').delay(4000).fadeIn(1000);

    $('#about-button').click(function () {
        document.getElementById('yesRadio-upload').checked=true;
        document.getElementById('yesRadio-record').checked=true;
        $('#select-genre-upload').hide();
        $('#response-form-uplaod').hide();
        $('#thanks-text-upload').hide();
        $('#select-genre-record').hide();
        $('#response-form-record').hide();
        $('#thanks-text-record').hide();
        $('#upload').fadeOut(250);
        $('#record').fadeOut(250);
        $('#aboutUs').fadeIn(500);
        ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'Click',
          eventLabel: 'Navigation'
          eventValue: 'About Page'
        });
    });
    $('#upload-button').click(function () {
        document.getElementById('yesRadio-upload').checked=true;
        document.getElementById('yesRadio-record').checked=true;
        $('#select-genre-upload').hide();
        $('#response-form-uplaod').hide();
        $('#thanks-text-upload').hide();
        $('#select-genre-record').hide();
        $('#response-form-record').hide();
        $('#thanks-text-record').hide();
        $('#record').fadeOut(250);
        $('#aboutUs').fadeOut(250);
        $('#upload').fadeIn(500);
        ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'Click',
          eventLabel: 'Navigation',
          eventValue: 'Upload Page'
        });
    });
    $('#record-button').click(function () {
        document.getElementById('yesRadio-upload').checked=true;
        document.getElementById('yesRadio-record').checked=true;
        $('#select-genre-upload').hide();
        $('#response-form-uplaod').hide();
        $('#thanks-text-upload').hide();
        $('#select-genre-record').hide();
        $('#response-form-record').hide();
        $('#thanks-text-record').hide();
        $('#upload').fadeOut(250);
        $('#aboutUs').fadeOut(250);
        $('#record').fadeIn(500);
        ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'Click',
          eventLabel: 'Navigation',
          eventValue: 'Record Page'
        });
    });
});