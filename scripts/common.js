$(function(){
    $("head").prepend("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
    $("head").prepend("<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\">");
    $("head").prepend("<link rel=\"stylesheet\" href=\"./css/common.css\">");
    $("body").prepend("<div id=\"navbar-placeholder\"></div>");
    $("#navbar-placeholder").load("./navbar.html");
});
