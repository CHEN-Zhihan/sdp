function registerCourseListener() {}

function registerCreateCourseListener() {
  $("#createCourse").click(function () {
    console.log("Create course selected");
    // Ajax POST
    $.ajax({
      url     : window.location.pathname + "/newCourse",
      type    : "POST",
      data    : {"action": "getForm"},
      success : function (response) {
        // Update header text
        $("#header-text").text("Create Course");
        // Insert result
        $("#main-content").html(response);
        // TODO: register submit listener
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
  registerCourseListener();
  registerCreateCourseListener();
});
