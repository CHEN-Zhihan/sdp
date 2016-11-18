// Respond to submit new module form
function registerModuleSubmitListener(pos) {
  $("#createModuleForm").submit(function (event) {
    // Prevent the default action
    event.preventDefault();
    console.log("Submit create module form");

    // Validate the form
    if (validateForm(this)) {
      // If validate success
      console.log("Validation success");
      var pos = parseInt($("#index", this).val());

      // Collect form data
      var formData = {
        "name": $("div > #name", this).val(),
        "description": $("div > #description", this).val(),
        "index": pos
      };
      console.log(formData);

      // Ajax POST
      $.ajax({
        url     : window.location.pathname,
        type    : "POST",
        data    : formData,
        success : function (response) {
          // Prompt result
          console.log(response);
          if (response["result"]) {
            $(".btn-success").click(function () {
              // Redirect to new module page
              var protocol = window.location.protocol;
              var host = window.location.host;
              var pathArray = window.location.pathname.split("/");
              var newPath = pathArray[1] + "/" + pathArray[2] + "/"
                            + pathArray[3] + "/" + pos;
              window.location.assign(protocol + "//" + host + "/" + newPath);
            });
            $("#createSuccessModal").modal();
          } else {
            // On error, prompt creation error
            $("#createFailModal").modal();
          }
        },
        error   : function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        }
      });
    } else {
      // If validation failed, prompt error
      $("#validateFailModal").modal();
    }
  });
}

$(document).ready(function () {
  registerModuleSubmitListener();
});
