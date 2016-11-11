function registerCourseListener() {
  $(".developingCourse").click(function () {
    var courseName = $(".course-name", this).text();
    var courseID = parseInt($(this).attr("id"));
    console.log("Course " + courseName + " selected");
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/" + courseID;
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

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

function registerSubmitListener() {
  $("#createCourseForm").submit(function (event) {
    event.preventDefault();
    console.log("Submit create course form");
    if (validateForm(this)) {
      console.log("Validation success");
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
              var protocol = window.location.protocol;
              var host = window.location.host;
              var pathArray = window.location.pathname.split("/");
              var newPath = pathArray[1] + "/" + pathArray[2] + "/" + response["newCourseID"];
              window.location.assign(protocol + "//" + host + "/" + newPath);
            });
            $("#createSuccessModal").modal();
          } else {
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
      $("#validateFailModal").modal();
    }
  });
}

function validateForm(form) {
  var validate = true;
  $(form).children().not(".submit").each(function () {
    if ($(this).children().val() === "" || $(this).children().val() === "placeholder") {
      $(this).children().addClass("has-error").focus(function () {
        $(this).removeClass("has-error");
      });
      validate = false;
    }
  });
  return validate;
}

$(document).ready(function () {
  registerCourseListener();
  registerCreateCourseListener();
});
