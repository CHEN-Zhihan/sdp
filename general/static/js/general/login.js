function registerTabListener() {
  $(".tab").click(function () {
    $(".tab.active").removeClass("active");
    $(this).addClass("active");
    console.log($(this).text().trim());
    if ($(this).text().trim() == "LOGIN") {
      $(".form-container").html(`
        <input name="action" value="LOGIN" hidden/>
        <!-- Username -->
        <div class="form-group">
          <input type="text" class="well well-sm well-input" placeholder="Username" name="username"></input>
        </div>

        <!-- Password -->
        <div class="form-group">
          <input type="password" class="well well-sm well-input" placeholder="Password" name="password" id="password"></input>
        </div>

        <!-- Select user type -->
        <div class="form-group">
          <select class="well well-sm well-input" name="usertype">
            <option value="Participant">Participant</option>
            <option value="Instructor">Instructor</option>
            <option value="HR">HR</option>
            <option value="Administrator">Administrator</option>
          </select>
        </div>

        <!-- Submit button -->
        <div class="form-group submit">
          <button type="submit" class="btn btn-default">Login</button>
        </div>
      `);
      $("form").attr("id", "loginForm").off("submit");
      registerLoginListener();
    } else if ($(this).text().trim() == "SIGN UP") {
      $(".form-container").html(`
        <input name="action" value="REGISTER" hidden/>
        <!-- Username -->
        <div class="form-group">
          <input type="text" class="well well-sm well-input" placeholder="Username" name="username" id="username"></input>
        </div>

        <!-- First name -->
        <div class="form-group">
          <input type="text" class="well well-sm well-input" placeholder="First name" name="firstName"></input>
        </div>

        <!-- Last name -->
        <div class="form-group">
          <input type="text" class="well well-sm well-input" placeholder="Last name" name="lastName"></input>
        </div>

        <!-- Password -->
        <div class="form-group">
          <input type="password" class="well well-sm well-input" placeholder="Password" name="password" id="password"></input>
        </div>

        <!-- Confirm password -->
        <div class="form-group">
          <input type="password" class="well well-sm well-input" placeholder="Confirm password" id="confirm-password"></input>
        </div>

        <!-- Submit button -->
        <div class="form-group submit">
          <button type="submit" class="btn btn-default">Sign up</button>
        </div>
      `);
      $("form").attr("id", "registerForm").off("submit");
      registerRegisterListener();
    }
  });
}

function registerLoginListener() {
  $("#loginForm").submit(function (event) {
    event.preventDefault();
    if (validateForm(this)) {
      var formData = new FormData($(this)[0]);
      $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: formData,
        async: false,
        success: function (response) {
          // Prompt result
          console.log(response);
          if (response["result"]) {
            var protocol = window.location.protocol;
            var host = window.location.host;
            window.location.assign(protocol + "//" + host + "/" + response["url"]);
          } else {
            $("#loginFailModal").modal();
          }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        },
        cache: false,
        contentType: false,
        processData: false
      });
    } else {
      $("#validateFailModal").modal();
    }
  })
}

function registerRegisterListener() {
  $("#registerForm").submit(function (event) {
    event.preventDefault();
    if (!validateForm(this)) {
      $("#validateFailModal").modal();
      return;
    }
    if ($("#password").val() == $("#confirm-password").val()) {
      var formData = new FormData($(this)[0]);
      $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: formData,
        async: false,
        success: function (response) {
          // Prompt result
          console.log(response);
          if (response["result"]) {
            var protocol = window.location.protocol;
            var host = window.location.host;
            window.location.assign(protocol + "//" + host + "/" + response["url"]);
          } else if (response["errno"] == -1) {
            $("#username").addClass("has-error").focus(function () {
              $(this).removeClass("has-error");
            });
            $("#dupErrorModal").modal();
          } else if (response["errno"] == -2) {
            $("#username").addClass("has-error").focus(function () {
              $(this).removeClass("has-error");
            });
            $("#invErrorModal").modal();
          }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          // On error, log the error info and prompt through error modal
          console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
          $("#errorModal").modal();
        },
        cache: false,
        contentType: false,
        processData: false
      });
    } else {
      $("#password").addClass("has-error").focus(function () {
        $(this).removeClass("has-error");
      });
      $("#confirm-password").addClass("has-error").focus(function () {
        $(this).removeClass("has-error");
      });
      $("#registerErrorModal").modal();
    }
  })
}

$(document).ready(function () {
  registerTabListener();
  registerLoginListener();
  $(".btn-error").click(function () {
    $("#password").val("");
    $("#confirm-password").val("");
  });
});
