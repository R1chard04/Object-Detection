document.addEventListener('DOMContentLoaded', function() {
 if (!window.fetch) {
  // If fetch is not available, load a polyfill
  // You can use any polyfill library you prefer
  import('whatwg-fetch');
}

 // fetch to get the number of stations are running
 const get_cameras_url = 'http://127.0.0.1:5000/bt1xx/startallprograms/';

 function get_cameras_running() {
  fetch(get_cameras_url, {
   method: 'GET',
   headers: {
    'Content-Type' : 'application/json'
   }
  })
  .this(response => {
   if(!response.ok) {
    throw new Error(`Failed to get the response from the server!`);
   }
   else {
    console.log(response.json()['cameras']);
   }
  
  })
  .catch(error => {
   console.error(`Error while sending the request: ${error}`);
  })
 }
 
 get_cameras_running();
});