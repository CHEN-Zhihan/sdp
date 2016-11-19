function registerActListener() {
  $(".btn-act").click(function () {
    var action = $(this).attr("id");
    console.log("Choose to " + action);
    $(".btn-confirm", "#confirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"action": action},
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response['result']) {
            $(".btn-success").click(function () {
              redirectHome();
            });
            $("#successModal").modal();
          } else {
            // On error, prompt enrollment error
            $("#failModal").modal();
          }
        },
        error   : function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        }
      });
    });
    $("#confirmModal").modal();
  });
}

$(document).ready(function () {
  registerModuleListener();
  registerActListener();
  registerCategoryListener();
});
