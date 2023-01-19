(function(){



  function changeCSSToLight(isLight, cssLinkIndex) {
  
    if($(".bodyswitcher").hasClass("lightTheme")){
      $(".bodyswitcher").removeClass("lightTheme")
    }else{
      $(".bodyswitcher").addClass("lightTheme")
    }



}

$("#change_mode_btn").on("click", function(e){
 e.preventDefault(); 
 var  value = $(this).attr("data-value")
 if(value == "false"){
  value = "true"
  $(this).children('i').attr("class", "fa-solid fa-moon mr-3");
 }else if(value == "true"){
  value = "false"
  $(this).children('i').attr("class", "fa-solid fa-sun mr-3");
 }


 changeCSSToLight(value, 8)
 $(this).attr("data-value", value)




})




})()

