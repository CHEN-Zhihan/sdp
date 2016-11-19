// Respond to a category clicked
function registerCategoryListener() {
  $(".category").click(function () {
    // Get category name and ID
    var categoryName = $(this).text();
    var categoryID = parseInt($(this).attr("id"));
    console.log("Category " + categoryName + " selected");
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/showCourseList?categoryID=" + categoryID;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

$(document).ready(function () {
  registerCategoryListener();
  registerCourseListener();
});
