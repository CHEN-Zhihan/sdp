// Get cookie
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

// Check CSRF requirement
function csrfSafeMethod (method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Redirect to current user home page
function redirectHome() {
  var protocol = window.location.protocol;
  var host = window.location.host;
  var pathArray = window.location.pathname.split("/");
  var newPath = pathArray[1] + "/" + pathArray[2];
  window.location.assign(protocol + "//" + host + "/" + newPath);
}

// Validate submitted form
function validateForm(form) {
  var validate = true;
  $(form).children().not(".submit").each(function () {
    if ($(this).children().val() === "" || $(this).children().val() === "placeholder") {
      $(this).children().addClass("has-error").focus(function () {
        $(this).removeClass("has-error");
      });
      validate = false;
    }
  });
  $(".form-container", form).children().not(".submit").each(function () {
    if ($(this).children().val() === "" || $(this).children().val() === "placeholder") {
      $(this).children().addClass("has-error").focus(function () {
        $(this).removeClass("has-error");
      });
      validate = false;
    }
  });
  return validate;
}

// Respond to a course clicked
function registerCourseListener() {
  $(".course:not(.disabled)").click(function () {
    // Get course name and ID
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + courseID;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to click on course
function registerModuleListener() {
  // If developing course clicked
  $(".module:not(.disabled)").click(function () {
    // Get course name and ID
    var moduleName = $(".module-name", this).text();
    var moduleIndex = parseInt($(this).attr("id"));
    console.log("Module " + moduleName + " selected");

    // Assemble new URL
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/" + pathArray[3]
                  + "/" + moduleIndex;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to a category clicked
function registerCategoryListener() {
  $(".category").click(function () {
    // Get category name and ID
    var categoryName = $(this).text();
    var categoryID = parseInt($(this).attr("id"));
    console.log("Category " + categoryName + " selected");
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/showCourseList?categoryID=" + categoryID;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

function registerBack2CourseListener() {
  $("#back").click(function () {
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/" + pathArray[3];

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
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
  $("a:not(.link)").click(function (event) {
    event.preventDefault();
    $("a.active").removeClass("active");
    $(this).addClass("active");
  });
});
