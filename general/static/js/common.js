function getCookie (name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod (method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function redirectHome() {
  var protocol = window.location.protocol;
  var host = window.location.host;
  var pathArray = window.location.pathname.split("/");
  var newPath = pathArray[1] + "/" + pathArray[2];
  window.location.assign(protocol + "//" + host + "/" + newPath);
}

$(document).ready(function () {
  // Set up AJAX for Django CSRF token
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      }
    }
  });

  // Redirect to home page when Home is clicked
  $("#home").click(function () {
    redirectHome();
  });

  // Highlight clicked anchor
  $("a").click(function () {
    $("a.active").removeClass("active");
    $(this).addClass("active");
  });
});
