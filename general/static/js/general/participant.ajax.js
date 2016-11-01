function registerCategoryListener() {
  $(".category").click(function () {
    var categoryName = $(this).text();
    var categoryID = parseInt($(this).attr("id"));
    console.log("Category " + categoryName + " selected");
    // Update header text
    $("#header-text").text(categoryName);
    // Ajax POST
    $.ajax({
      url     : window.location.pathname + "/showCourseList",
      type    : "POST",
      data    : {"categoryID": categoryID},
      success : function (response) {
        // Insert result
        $("#main-content").html(response);
        registerCourseListener();
      },
      error   : function (XMLHttpRequest, textStatus, errorThrown) {
        // On error, log the error info and prompt through error modal
        console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
        $("#errorModal").modal();
      }
    });
  });
}

function registerCourseListener() {
  $(".course").click(function () {
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");
    var postURL;
    if ($(this).hasClass("currentCourse")) {
      postURL = window.location.pathname + "/takeCourse";
    } else {
      postURL = window.location.pathname + "/showCourse";
    }
    // Update header text
    $("#header-text").text(courseName);
    // Ajax POST
    $.ajax({
      url     : postURL,
      type    : "POST",
      data    : {"courseID": courseID},
      success : function (response) {
        // Insert result
        $("#main-content").html(response);
        registerEnrollListener();
      },
      error   : function (XMLHttpRequest, textStatus, errorThrown) {
        // On error, log the error info and prompt through error modal
        console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
        $("#errorModal").modal();
      }
    });
  });
}

function registerEnrollListener() {
  $(".btn-enroll").click(function () {
    var courseID = parseInt($(this).attr("id"));
    console.log("Choose to enroll");
    // Ajax POST
    $.ajax({
      url     : window.location.pathname + "/enroll",
      type    : "POST",
      data    : {"courseID": courseID},
      success : function (response) {
        // Prompt result
        console.log(response);
        if (response['result']) {
          $(".btn-success").click(function () {
            redirectHome();
          });
          $("#enrollSuccessModal").modal();
        } else {
          $("#enrollFailModal").modal();
        }
      },
      error   : function (XMLHttpRequest, textStatus, errorThrown) {
        // On error, log the error info and prompt through error modal
        console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
        $("#errorModal").modal();
      }
    });
  });
}

$(document).ready(function () {
  // Get courses under a category
  registerCategoryListener();
  registerCourseListener();
});
