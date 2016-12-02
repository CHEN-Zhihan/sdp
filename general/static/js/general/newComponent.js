function registerTypeSelectListener() {
  $("#type").on("change", function () {
    if ($(this).val() == "TEXT") {
      $(".form-content").html(`
        <textarea class="well well-sm well-input fullwidth" placeholder="Add Content" rows=10 id="text" name="text"></textarea>
      `);
    } else if ($(this).val() == "VIDEO") {
      $(".form-content").html(`
        <input class="well well-sm well-input fullwidth" placeholder="Paste video URL here" id="text" name="text"></input>
      `);
    } else {
      $(".form-content").html(`
        <input type="file" name="file" id="id_file">
        <label for="id_file" class="btn btn-default btn-file">
          <span class="glyphicon glyphicon-upload"></span>
          <span id="info">Choose File</span>
        </lable>
      `);
      registerFileSelectListener();
    }
  });
}

function registerFileSelectListener() {
  $("input#id_file").each( function() {
    var $input   = $(this),
        $label	 = $input.next('label'),
        labelVal = $label.html();

    $input.on( 'change', function(e) {
      var fileName = '';

      if( this.files && this.files.length > 1 )
        fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
      else if( e.target.value )
        fileName = e.target.value.split( '\\' ).pop();

      if( fileName )
        $label.find('span#info').html(fileName);
      else
        $label.html( labelVal );
    });

    // Firefox bug fix
    $input.on( 'focus', function(){ $input.addClass( 'has-focus' ); }).on( 'blur', function(){ $input.removeClass( 'has-focus' ); });
  });
}

function registerComponentSubmitListener() {
  $("#createComponentForm").submit(function (event) {
    // Prevent the default action
    event.preventDefault();
    console.log("Submit create component form");
    var type = $("div > select#type", this).val()

    var formData = new FormData($(this)[0]);

    if (type == "TEXT" || type == "VIDEO") {
      if (!validateForm(this)) {
        $("#validateFailModal").modal();
        return;
      }
    } else {
      if ($("div > input#id_file", this).val() == "") {
        $("#validateFailModal").modal();
        return;
      }
    }

    $.ajax({
      url: window.location.pathname,
      type: 'POST',
      data: formData,
      async: false,
      success: function (response) {
        // Prompt result
        console.log(response);
        if (response["result"]) {
          $(".btn-success").click(function () {
            // Redirect to new module page
            var protocol = window.location.protocol;
            var host = window.location.host;
            var pathArray = window.location.pathname.split("/");
            var newPath = pathArray[1] + "/" + pathArray[2] + "/"
                          + pathArray[3] + "/" + pathArray[4];
            window.location.assign(protocol + "//" + host + "/" + newPath);
          });
          $("#createSuccessModal").modal();
        } else {
          // On error, prompt creation error
          $("#createFailModal").modal();
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
  });
}

function registerBack2ModuleListener() {
  $("#back-module").click(function () {
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2] + "/"
                  + pathArray[3] + "/" + pathArray[4];

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

$(document).ready(function () {
  registerTypeSelectListener();
  registerComponentSubmitListener();
  registerBack2ModuleListener();
});
