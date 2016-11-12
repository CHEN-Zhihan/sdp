// Respond to click on course
function registerCourseListener() {
  // If developing course clicked
  $(".developingCourse").click(function () {
    // Get course name and ID
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");

    // Assemble new URL
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/" + courseID;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

// Respond to menu item 'Create Course'
function registerCreateCourseListener() {
  $("#createCourse").click(function () {
    console.log("Create course selected");
    // Ajax POST
    $.ajax({
      url     : window.location.pathname + "/newCourse",
      type    : "POST",
      data    : {"action": "getForm"},
      success : function (response) {
        // Update header text
        $("#header-text").text("Create Course");
        // Insert result
        $("#main-content").html(response);

        // Remove placeholder styles when select box updated
        $("select").change(function () {
          $(this).removeClass("placeholder");
        });
        registerSubmitListener();
      },
      error   : function (XMLHttpRequest, textStatus, errorThrown) {
        // On error, log the error info and prompt through error modal
        console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
        $("#errorModal").modal();
      }
    });
  });
}

// Respond to submit new course form
function registerSubmitListener() {
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
        url     : window.location.pathname + "/newCourse",
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
  registerCourseListener();
  registerCreateCourseListener();
});
