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

// Respond to edit course info
function registerEditListener() {
  $(".btn-edit").click(function () {
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + pathArray[3] + "/editCourse";

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

function registerDragSortHandler() {
  $("#sortable").sortable({
    forcePlaceholderSize: true,
    placeholder: "ui-state-highlight",
    start   : function (event, ui) {
      $(".addModule").fadeOut(200);
      ui.placeholder.height($("a > .module", ui.item).outerHeight());
    },
    update  : function (event, ui) {
      var originIndex = parseInt($("a > .module", ui.item).attr("id"));
      var newIndex = parseInt($(this).children().index(ui.item));
      console.log("Change " + originIndex + " to " + newIndex);
      // Ajax POST
      $.ajax({
        url     : window.location.pathname + "/changeModuleOrder",
        type    : "POST",
        data    : {"originIndex": originIndex, "newIndex": newIndex},
        success : function (response) {
          if (response["result"]) {
            $(".modules-container").html(response["data"]);
            registerAddModuleListener();
            registerDragSortHandler();
          } else {
            $(".btn-refresh").click(function () {
              window.location.reload();
            });
            $("#reorderFailModal").modal();
          }
        },
        error   : function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        }
      });
    },
    stop    : function (event, ui) {
      $(".addModule").fadeIn(200);
    }
  });
}

$(document).ready(function () {
  registerAddModuleListener();
  registerEditListener();
  registerOpenListener();
  registerDeleteListener();
  registerDragSortHandler();
});
