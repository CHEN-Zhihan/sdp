// Respond to click on course
function registerCourseListener() {
  // If developing course clicked
  $(".developingCourse").click(function () {
    // Get course name and ID
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");

    // Assemble new URL
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/" + courseID;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to menu item 'Create Course'
function registerCreateCourseListener() {
  $("#createCourse").click(function () {
    console.log("Create course selected");
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/newCourse";

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

$(document).ready(function () {
  registerCourseListener();
  registerCreateCourseListener();
});
