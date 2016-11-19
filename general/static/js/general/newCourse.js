// Respond to submit new course form
function registerCourseSubmitListener() {
  $("#createCourseForm").submit(function (event) {
    // Prevent the default action
    event.preventDefault();
    console.log("Submit create course form");

    // Validate the form
    if (validateForm(this)) {
      // If validate success
      console.log("Validation success");

      // Collect form data
      var formData = {
        "action": "submit",
        "name": $("div > #name", this).val(),
        "categoryID": $("div > #category", this).val(),
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
          if (response["result"]) {
            $(".btn-success").click(function () {
              // Redirect to new course page
              var protocol = window.location.protocol;
              var host = window.location.host;
              var pathArray = window.location.pathname.split("/");
              var newPath = pathArray[1] + "/" + pathArray[2] + "/" + response["newCourseID"];
              window.location.assign(protocol + "//" + host + "/" + newPath);
            });
            $("#createSuccessModal").modal();
          } else {
            // On error, prompt creation error
            if (response["newCourseID"] == -2) {
              $(".modal-body > p", "#createFailModal").text("Course name already exists.");
              $("input#name").addClass("has-error").focus(function () {
                $(this).removeClass("has-error");
              });
              $(".btn-fail").click(function () {
                $(".modal-body > p", "#createFailModal").text("An error occurred. Creation failed.");
              });
            }
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
  $("select").on("change", function () {
    $(this).removeClass("placeholder");
  });
  registerCourseSubmitListener();
});
