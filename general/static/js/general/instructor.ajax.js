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
        registerCourseSubmitListener();
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

// Respond to add new module
function registerAddModuleListener() {
  $(".addModule").click(function () {
    // Get insert position
    var pos = parseInt($(this).attr("id"));
    console.log("Add module at " + pos);

    // Update header text
    $("#header-text").text("Add Module");
    // Insert form
    $("#main-content").html(`
      <!-- Module information form -->
      <form id="createModuleForm">
        <!-- Input module name -->
        <div class="form-group">
          <input class="well well-sm well-input fullwidth" placeholder="Module name" id="name"></input>
        </div>

        <!-- Input module description -->
        <div class="form-group">
          <textarea class="well well-sm well-input fullwidth" placeholder="Module description" rows=10 id="description"></textarea>
        </div>

        <!-- Submit button -->
        <div class="form-group submit">
          <button type="submit" class="btn btn-default">Create</button>
        </div>
      </form> <!-- End course information form -->

      <!-- Validation failed modal dialog -->
      <div class="modal fade" id="validateFailModal" role="dialog">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">Error</h4>
            </div>
            <div class="modal-body">
              <p>One or more fields required.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div> <!-- End modal -->

      <!-- Create success modal dialog -->
      <div class="modal fade" id="createSuccessModal" role="dialog">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">Success</h4>
            </div>
            <div class="modal-body">
              <p>Module added successfully.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default btn-success" data-dismiss="modal">Go to module</button>
            </div>
          </div>
        </div>
      </div> <!-- End modal -->

      <!-- Create failed modal dialog -->
      <div class="modal fade" id="createFailModal" role="dialog">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">Error</h4>
            </div>
            <div class="modal-body">
              <p>An error occurred. Creation failed.</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div> <!-- End modal -->
    `);
    registerModuleSubmitListener(pos);
  });
}

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

      // Collect form data
      var formData = {
        "name": $("div > #name", this).val(),
        "description": $("div > #description", this).val(),
        "index": pos
      };
      console.log(formData);

      // Ajax POST
      $.ajax({
        url     : window.location.pathname + "/newModule",
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
                            + pathArray[3] + "/" + response["newModuleID"];
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
  registerAddModuleListener();
});
