$(document).ready(function(){
  $("a").click(function(){
    $("a.active").removeClass("active");
    $(this).addClass("active");
  });
});
