$(document).ready(function () {
  // Get courses under a category
  $(".category").click(function () {
    var category_name = $(this).text();
    var category_id = parseInt($(this).attr("id"));
    console.log("Category " + category_name + " selected");
    // Update header text
    $("#header-text").text(category_name);
    // Ajax POST
    $.ajax({
      url     : "showCourseList",
      type    : "POST",
      data    : {"category_id": category_id},
      success : function (response) {
        // Insert result
        $("#main-content").html(response);
      },
      error   : function (XMLHttpRequest, textStatus, errorThrown) {
        // On error, log the error info and prompt through error modal
        console.log(XMLHttpRequest.readyState + XMLHttpRequest.status + XMLHttpRequest.responseText);
        $("#errorModal").modal();
      }
    });
  });
});
