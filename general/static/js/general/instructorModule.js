// Respond to add new component
function registerAddComponentListener() {
  $(".addComponent").click(function () {
    // Get insert position
    var pos = parseInt($(this).attr("id"));
    console.log("Add component at " + pos);
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + pathArray[3] + "/" + pathArray[4]
                  + "/newComponent?index=" + pos;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

function registerDragSortHandler() {
  $("#sortable").sortable({
    forcePlaceholderSize: true,
    placeholder: "ui-state-highlight",
    start   : function (event, ui) {
      $(".addComponent").fadeOut(200);
      $(".delete").fadeOut(200);
      ui.placeholder.height($("div > .component", ui.item).outerHeight());
    },
    update  : function (event, ui) {
      var originIndex = parseInt($("div > .component", ui.item).attr("id"));
      var newIndex = parseInt($(this).children().index(ui.item));
      console.log("Change " + originIndex + " to " + newIndex);
      // Ajax POST
      $.ajax({
        url     : window.location.pathname + "/changeComponentOrder",
        type    : "POST",
        data    : {"originIndex": originIndex, "newIndex": newIndex},
        success : function (response) {
          if (response["result"]) {
            $(".components-container").html(response["data"]);
            registerAddComponentListener();
            registerDragSortHandler();
            registerDeleteListener();
          } else {
            $(".btn-refresh").click(function () {
              window.location.reload(true);
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
      $(".addComponent").fadeIn(200);
      $(".delete").fadeIn(200);
    }
  });
}

// Respond to edit module info
function registerEditListener() {
  $(".btn-edit").click(function () {
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + pathArray[3] + "/"
                  + pathArray[4] + "/editModule";

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to delete a component
function registerDeleteListener() {
  $(".delete").click(function () {
    var index = parseInt($(this).attr("id"));
    console.log("Choose to delete #" + index);
    $(".btn-confirm", "#deleteConfirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"action": "DELETE", "index": index},
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
  registerEditListener();
  registerAddComponentListener();
  registerDragSortHandler();
  registerDeleteListener();
  registerBack2CourseListener();
});
