/**
 * CREDIT: code for floating buttons taken from 
 * https://www.w3schools.com/howto/howto_js_scroll_to_top.asp 
 */
window.onscroll = function () {
    scrollFunction();
};


/**
 * makes floating button for go to top visible once user starts scrolling.
 */
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        $("#to-top-btn").addClass('active');
    } else {
        $("#to-top-btn").removeClass('active');
    }
}

$('#to-top-btn').click(function () {
    topFunction();
});

/**
 * Scrolls the user bACK to the top of the page
 */
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

/* credit: code for Progress Circle taken from https://bootstrapious.com/p/circular-progress-bar and edited to fit project needs */

$(function() {

  $(".my_progress").each(function() {

    var value = $(this).attr('data-value');
    var left = $(this).find('.progress-left .progress-circle');
    var right = $(this).find('.progress-right .progress-circle');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

});
