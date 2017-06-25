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
  path=$("#emailf").val();
  if(validateEmail(path)==false){
    $("#email").text("Email inválido");
    return true;
  }
  exists=false;
  $.getJSON(Flask.url_for("verifyemail",{path:path}), function(data){
    if(data.emailexists){
      exists=true;
      $("#email").text("Email já em uso");
      return true;
    }
  });
  return false;
}

function verifyuser(){
  pat=$("#nomef").val();
  exists=false;
  $.getJSON(Flask.url_for("verifyuser",{pat}), function(data){
    if(data.userexists){
      exists=true;
      $("#nome").text("Nome de usuário já em uso");
    }
  });
  return exists;
}
  
$(function(){
  verifier("#emailf", "#email", "Não há email", verifyemail);
  verifier("#nomef", "#nome", "Não há nome", verifyuser);
  verifier("#senhaf", "#senha", "Não há senha", senhaf);
  verifier("#senha1f", "#senha1", "Confirme a senha", senha1f);
/*  $("#senha1f").focusout(function(){
      if ($("#senha1f").val()==""){
          $("#senha1").text("Confirme a senha");
          preventform();
      }
      else if($("senhaf").value != $("senha")){
           $("#senha1").text("As senhas não correspondem");
           preventform();
      }
      else{
        $("#senha1").text("");
        letformgo();
      }
      resize();
  });
*/

})