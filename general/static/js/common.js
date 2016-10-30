$(document).ready(function () {
  // Set up AJAX for Django CSRF token
  $.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
  });

  // Redirect to home page when Home is clicked
  $("#home").click(function () {
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[0] + "/" + pathArray[1];
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });

  // Highlight clicked anchor
  $("a").click(function () {
    $("a.active").removeClass("active");
    $(this).addClass("active");
  });
});
