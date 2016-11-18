// Respond to add new module
function registerAddModuleListener() {
  $(".addModule").click(function () {
    // Get insert position
    var pos = parseInt($(this).attr("id"));
    console.log("Add module at " + pos);
    var protocol = window.location.protocol;
    var host = window.location.host;
    var pathArray = window.location.pathname.split("/");
    var newPath = pathArray[1] + "/" + pathArray[2]
                  + "/" + pathArray[3] + "/newModule?index=" + pos;

    // Redirect to new URL
    window.location.assign(protocol + "//" + host + "/" + newPath);
  });
}

$(document).ready(function () {
  registerAddModuleListener();
});
