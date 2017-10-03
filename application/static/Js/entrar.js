//$(function(){
//    verifier("#emailf", "#email", "Não há email");
//    verifier("#senhaf", "#senha", "Não há senha");
//})

function signInCallBack(authResult){
    if (authResult['code']){
     // Hide the sign-in button now that the user is authorized
     $('#signinButton').attr('stye', 'display: none');
     // Send the one-time-use code to the server, if the server responds, write a 'login_successful' message
     $.ajax({
         type: 'POST',
         url: '/gconnect?state={{STATE}}',
         processData: false,
         data: authResult['code'],
         contentType: 'application/octet-stream; charset=utf-8',
         success: function(result){
             //Handle or verify the server response if necessary.
             if(result){
             $('#result').html('Login Successful!</br>'+result+'</br>Redirecting...')
             setTimeout(function(){
                 window.location.href = "{{url_for('gconnect'), dest=dest}}";
             },4000);
         } else if (authResult['error']){
             console.log('There was an error: ' + authResult['error']);
         } else {
             $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }
        }
     });
    }
}

 function sendTokenToServer() {
    var access_token = FB.getAuthResponse()['accessToken'];
    console.log(access_token)
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
     $.ajax({
      type: 'POST',
      url: '/fbconnect?state={{STATE}}',
      processData: false,
      data: access_token,
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Handle or verify the server response if necessary.
        if (result) {
          $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...')
         setTimeout(function() {
          window.location.href = "/index";
         }, 4000);
      } else {
        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }
      }
  });
    });
  }
