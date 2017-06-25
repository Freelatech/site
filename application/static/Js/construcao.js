$(function(){

document.getElementsByTagName("BODY")[0].onresize=altura();

function altura(){
    var af=0;
    af=document.getElementsByTagName("footer")[0].offsetHeight;
    var aw=0;
    aw=$(window).height();
    var mt=0;
    var dh=400;
    mb=(aw-af-100-(dh))/2;
    if(mb<0){
        mb=0;
    }
    mt=100+mb;
    document.getElementById("outer").style.marginTop=mt.toFixed(2)+"px";
    document.getElementsByTagName("footer")[0].style.marginTop=mb.toFixed(2)+"px";
    }
    
altura();

});