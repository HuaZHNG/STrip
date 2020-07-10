/**
 * Particleground demo
 * @author Jonathan Nicol - @mrjnicol
 */

$(document).ready(function() {
    $('#particles').particleground({
        dotColor: '#bdbdbd',
        lineColor: '#bdbdbd'
    });
    $('.intro').css({
        'margin-top': -($('.intro').height() / 2)
    });
});