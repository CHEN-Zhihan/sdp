// Respond to designate an instructor
function registerDesignateListener() {
  $(".btn-designate").click(function () {
    var username = $(this).attr("id");
    console.log("Choose to designate " + username + " as instructor");
    $(".modal-body > p", "#confirmModal").text("Are you sure to designate user " + username + " as an instructor?");
    $(".modal-body > p", "#successModal").text("User " + username + " designated as an instructor successfully.");
    $(".btn-confirm", "#confirmModal").click(function () {
      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : {"username": username},
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response["result"]) {
            $(".btn-refresh").click(function () {
              window.location.reload(true);
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
  registerDesignateListener();
});
