function getsubclasses(){
var classid = $('input[name=classe]:checked', '#prestform').val();
console.log(classid);
  $.getJSON(Flask.url_for("getsubclasses",{classid}), function(data){
        var outros=false;
        var outros_id=0;
        document.getElementById("subclasses").innerHTML="";
        for(i=0; i<Object.keys(data).length; i++){
          var j=Object.keys(data)[i];
          if(data[j]=="Outros"){
            outros=true;
            outros_id=j;
          }
          else{
          console.log(data[j]);
          document.getElementById("subclasses").innerHTML=document.getElementById("subclasses").innerHTML+'<input type="radio" name="subclasse" value="'+j+'">'+data[j]+'<br>';
          }
        }
        if(outros){
        document.getElementById("subclasses").innerHTML=document.getElementById("subclasses").innerHTML+'<input type="radio" name="subclasse" value="'+outros_id+'">'+"Outros"+'<br>';
        }
    });

}

$(function(){
    $("#classes").click(getsubclasses);
    $("#submitall").click(function(){
      console.log("clicou");
      $("#prestform").submit();
    });
    getsubclasses();
});

$("#educform").submit(function( event ) {

  // Stop form from submitting normally
  event.preventDefault();

  // Get some values from elements on the page:
  var $form = $( this ),
    url = $form.attr( "action" );

  // Send the data using post
  formser=$('#educform');
  $.post(url,formser.serialize()).done(function() {
    $("#eductable").append("<tr><td>"+$("#educforminstituicao").val()+"</td><td>"+$("#educformcurso").val()+"</td><td>"+$("#educformanoinicio").val()+"</td><td>"+$("#educformanoconclusao").val()+"</td><td>"+$("#educformdescricao").val()+"</td></tr>");
    document.getElementById("educform").reset();
    $("#educclose" ).click();
  });
});

$("#expform").submit(function( event ) {

  // Stop form from submitting normally
  event.preventDefault();

  // Get some values from elements on the page:
  var $form = $( this ),
    url = $form.attr( "action" );

  // Send the data using post
  formser=$('#expform');
  $.post(url,formser.serialize()).done(function() {
    $("#exptable").append("<tr><td>"+$("#expformlocal").val()+"</td><td>"+$("#expformfuncao").val()+"</td><td>"+$("#expformanoinicio").val()+"</td><td>"+$("#expformanoconclusao").val()+"</td><td>"+$("#expformdescricao").val()+"</td></tr>");
    document.getElementById("expform").reset();
    $("#expclose" ).click();
  });
});

$("#certform").submit(function( event ) {

  // Stop form from submitting normally
  event.preventDefault();

  // Get some values from elements on the page:
  var $form = $( this ),
    url = $form.attr( "action" );

  // Send the data using post
  formser=$('#certform');
  $.post(url,formser.serialize()).done(function() {
    $("#certtable").append("<tr><td>"+$("#certformlocal").val()+"</td><td>"+$("#certformnome").val()+"</td><td>"+$("#certformanoinicio").val()+"</td><td>"+$("#certformanoconclusao").val()+"</td><td>"+$("#certformdescricao").val()+"</td></tr>");
    document.getElementById("certform").reset();
    $("#certclose" ).click();
  });
});