function bigbody() {
  var bodyHeight = $(document.body).height();
  var viewHeight = $(window).height();
  d = viewHeight - bodyHeight;
  if(d>0){
    document.getElementsByTagName("footer")[0].style.marginTop=d.toFixed(2)+"px";
    }
  }

$(function(){
  bigbody();
});
