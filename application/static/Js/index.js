$(window).scroll(navfun);

navfun();

function navfun(event) {
    var scroll = $(window).scrollTop();
    if(scroll!=0){
      $("#nav").css("background-color","white");
      $("#nav").css("opacity","1");
      $("#nav").css("height","60px");
      $("#nav").css("box-shadow","0px 0px 1px 1px rgba(0, 0, 0, 0.3)")
    }
    else{
      $("nav").css("background-color","transparent");
      $("#nav").css("height","140px")
      $("#nav").css("box-shadow","none")
    }
}