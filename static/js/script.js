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