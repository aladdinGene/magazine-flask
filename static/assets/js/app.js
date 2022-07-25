var slug = ''
$(document).ready(function(){
    $(window).scroll(function(){
        if($(window).scrollTop() > 0){
            $('.header_area').addClass('show');
        } else {
            $('.header_area').removeClass('show');
        }
    });
})