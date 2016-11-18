// Respond to add new module
function registerAddModuleListener() {
  $(".addModule").click(function () {
    // Get insert position
    var pos = parseInt($(this).attr("id"));
    console.log("Add module at " + pos);
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + pathArray[3] + "/newModule?index=" + pos;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to open a course
function registerOpenListener() {
  $(".btn-open").click(function () {
    console.log("Choose to open");
    $(".btn-confirm", "#openConfirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"action": "OPEN"},
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response['result']) {
            $(".btn-success", "#openConfirmModal").click(function () {
              window.location.reload(true);
            });
            $("#openSuccessModal").modal();
          } else {
            // On error, prompt enrollment error
            $("#openFailModal").modal();
          }
        },
        error   : function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        }
      });
    });
    $("#openConfirmModal").modal();
  });
}

// Respond to delete a course
function registerDeleteListener() {
  $(".btn-delete").click(function () {
    console.log("Choose to open");
    $(".btn-confirm", "#deleteConfirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"action": "DELETE"},
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response['result']) {
            $(".btn-success", "#deleteSuccessModal").click(function () {
              redirectHome();
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
  registerAddModuleListener();
  registerOpenListener();
  registerDeleteListener();
});
