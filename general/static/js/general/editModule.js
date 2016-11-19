// Respond to submit new course form
function registerModuleEditListener() {
  $("#editModuleForm").submit(function (event) {
    // Prevent the default action
    event.preventDefault();
    console.log("Submit edit module form");

    // Validate the form
    if (validateForm(this)) {
      // If validate success
      console.log("Validation success");

      // Collect form data
      var formData = {
        "name": $("div > #name", this).val(),
        "description": $("div > #description", this).val()
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
          if (response["result"] == 0) {
            $(".btn-success").click(function () {
              // Redirect to new course page
              var protocol = window.location.protocol;
              var host = window.location.host;
              var pathArray = window.location.pathname.split("/");
              var newPath = pathArray[1] + "/" + pathArray[2] + "/" + pathArray[3]
                            + "/" + pathArray[4];
              window.location.assign(protocol + "//" + host + "/" + newPath);
            });
            $("#editSuccessModal").modal();
          } else {
            // On error, prompt creation error
            if (response["result"] == -2) {
              $(".modal-body > p", "#editFailModal").text("Module name already exists.");
              $("input#name").addClass("has-error").focus(function () {
                $(this).removeClass("has-error");
              });
              $(".btn-fail").click(function () {
                $(".modal-body > p", "#editFailModal").text("An error occurred. Edition failed.");
              });
            }
            $("#editFailModal").modal();
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
  registerModuleEditListener();
});
