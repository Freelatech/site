function preventform(){
    $("form").submit(function(e){
        e.preventDefault();
        $(".jsholders").css("background-color","red");
        setTimeout(function(){
          $(".jsholders").css("background-color","inherit");
        }, 1000);
    });
}

function letformgo(){
    if($("#nome").text()=="" && $("#email").text()=="" && $("#senha").text()=="" && $("#senha1").text()==""){
      $("form").unbind();
    }
}
    
function resize(){
      document.getElementsByTagName("footer")[0].style.marginTop= 0 +"px";
      bigbody();
}

function verifier(formid, pid, msg, unfun){
  if (typeof unfun === 'undefined') { unfun = function(){return false;} }
  $(formid).focusout(function(){
      if ($(formid).val()==""){
          $(pid).text(msg);
          preventform();
      }
      else if(unfun()){
        preventform();
      }
      else{
           $(pid).text("");
           letformgo();
      }
      resize();
  });
  $(formid).focus(function(){
    $(pid).text("");
    resize();
  });
}
