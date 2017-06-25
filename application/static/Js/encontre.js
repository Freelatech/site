function teste(){
    console.log("teste");
    console.log(document.getElementById("filters").action);
    document.getElementById("parent").innerHTML=document.getElementById("filters").action;
}

$(function(){

});
/*
    $("form").submit(function(e){
        e.preventDefault();
    });*/