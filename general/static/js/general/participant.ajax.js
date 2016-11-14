

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
