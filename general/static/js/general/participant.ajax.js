// Respond to a category clicked
function registerCategoryListener() {
  $(".category").click(function () {
    // Get category name and ID
    var categoryName = $(this).text();
    var categoryID = parseInt($(this).attr("id"));
    console.log("Category " + categoryName + " selected");

    // Ajax POST
    $.ajax({
      url     : window.location.pathname + "/showCourseList",
      type    : "POST",
      data    : {"categoryID": categoryID},
      success : function (response) {
        // Update header text
        $("#header-text").text(categoryName);
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

// Respond to a course clicked
function registerCourseListener() {
  $(".course").click(function () {
    // Get course name and ID
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");

    // Determine course type to assign URL
    var postURL;
    if ($(this).hasClass("currentCourse")) {
      // If is current course, post to takeCourse
      postURL = window.location.pathname + "/takeCourse";
    } else {
      // If else, post to showCourse
      postURL = window.location.pathname + "/showCourse";
    }

    // Ajax POST
    $.ajax({
      url     : postURL,
      type    : "POST",
      data    : {"courseID": courseID},
      success : function (response) {
        // Update header text
        $("#header-text").text(courseName);
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

// Respond to enroll a course
function registerEnrollListener() {
  $(".btn-enroll").click(function () {
    // Get course ID
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
            // On close of modal dialog, redirect to home page
            redirectHome();
          });
          $("#enrollSuccessModal").modal();
        } else {
          // On error, prompt enrollment error
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
  registerCategoryListener();
  registerCourseListener();
});
