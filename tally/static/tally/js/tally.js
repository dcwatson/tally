$(function() {
    var url = $('.chart').data('url');
    $.getJSON(url, function(data) {
        console.log(data);
    });
});
