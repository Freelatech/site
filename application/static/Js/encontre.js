function getsubclasses(){
var classid = $('input[name=classe]:checked', '#filtersform').val();
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
});
/*
    $("form").submit(function(e){
        e.preventDefault();
    });*/