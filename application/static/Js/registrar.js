function senha1f(){
  if($("#senhaf").val() != $("#senha1f").val()){
    $("#senha1").text("As senhas não correspondem");
    return true;
  }
  else{
    return false;
  }
}

function senhaf(){
  $("#senha1f").focusout();
  if($("#senhaf").val().length<6){
    $("#senha").text("Senha deve ter no mínimo 6 caracteres");
    return true;
  }
  return false;
}

function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function verifyemail(){
  path=$("#email").val();
  if(validateEmail(path)==false){
    $("#emailf").text("Email inválido");
    return true;
  }
  exists=false;
  $.getJSON(Flask.url_for("verifyemail",{path:path}), function(data){
    if(data.emailexists){
      exists=true;
      $("#emailf").text("Email já em uso");
      return true;
    }
  });
  return false;
}

function verifyuser(){
  pat=$("#nome").val();
  exists=false;
  $.getJSON(Flask.url_for("verifyuser",{pat}), function(data){
    if(data.userexists){
      exists=true;
      $("#nomef").text("Nome de usuário já em uso");
    }
  });
  return exists;
}

$(function(){
  verifier("#email", "#emailf", "Não há email", verifyemail);
  verifier("#nome", "#nomef", "Não há nome", verifyuser);
  verifier("#senha", "#senhaf", "Não há senha", senhaf);
  verifier("#senha1", "#senha1f", "Confirme a senha", senha1f);
  $("#senha1").focusout(function(){
      if ($("#senha1").val()==""){
          $("#senha1f").text("Confirme a senha");
          preventform();
      }
      else if($("senha").value != $("senha1").value){
           $("#senha1f").text("As senhas não correspondem");
           preventform();
      }
      else{
        $("#senha1").text("");
        letformgo();
      }
      resize();
  });


})