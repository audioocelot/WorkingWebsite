/*
 * Page Handler:
 * Handles display and button actions.
 */

(function (window, $) {
  
  $(function() {
    
    
    $('.ripple').on('click', function (event) {
      event.preventDefault();
      
      var $div = $('<div/>'),
          btnOffset = $(this).offset(),
      		xPos = event.pageX - btnOffset.left,
      		yPos = event.pageY - btnOffset.top;
      
      $div.addClass('ripple-effect');
      var $ripple = $(".ripple-effect");
      
      $ripple.css("height", $(this).height());
      $ripple.css("width", $(this).height());
      $div
        .css({
          top: yPos - ($ripple.height()/2),
          left: xPos - ($ripple.width()/2),
          background: $(this).data("ripple-color")
        }) 
        .appendTo($(this));

      window.setTimeout(function(){
        $div.remove();
      }, 2000);
    });
    
  });
  
})(window, jQuery);


$(document).ready(function(){
  $('#fullImg').delay(1000).fadeIn(500);
  $('#buttonDiv').delay(2000).fadeIn(500);

  $('#AUbutton').click(function(){
      $('#upload').fadeOut(250);
      $('#record').fadeOut(250);
      $('#aboutUs').fadeIn(500);
  })
  $('#Ubutton').click(function(){
      $('#record').fadeOut(250);
      $('#aboutUs').fadeOut(250);
      $('#upload').fadeIn(500);
  })
  $('#Rbutton').click(function(){
      $('#upload').fadeOut(250);
      $('#aboutUs').fadeOut(250);
      $('#record').fadeIn(500);
  })
});