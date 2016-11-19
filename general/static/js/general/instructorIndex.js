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

// Respond to delete a course
function registerDeleteListener() {
  $(".delete").click(function () {
    var id = parseInt($(this).attr("id"));
    console.log("Choose to delete #" + id);
    $(".btn-confirm", "#deleteConfirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"action": "DELETE", "id": id},
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response['result']) {
            $(".btn-success", "#deleteSuccessModal").click(function () {
              window.location.reload(true);
            });
            $("#deleteSuccessModal").modal();
          } else {
            // On error, prompt enrollment error
            $("#deleteFailModal").modal();
          }
        },
        error   : function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        }
      });
    });
    $("#deleteConfirmModal").modal();
  });
}

$(document).ready(function () {
  registerCourseListener();
  registerCreateCourseListener();
  registerDeleteListener();
});
