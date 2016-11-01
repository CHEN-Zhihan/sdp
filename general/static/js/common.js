$(document).ready(function () {
  // Set up AJAX for Django CSRF token
  $.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
  });

  // Redirect to home page when Home is clicked
  $("#home").click(function () {
    var protocol = window.location.protocol;
    console.log(protocol);
    var host = window.location.host;
    console.log(host);
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2];
    console.log(newPath);
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });

  // Highlight clicked anchor
  $("a").click(function () {
    $("a.active").removeClass("active");
    $(this).addClass("active");
  });
});
