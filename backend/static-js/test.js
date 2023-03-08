document.addEventListener('keydown', function(event) {
 // Send the key data to the Flask endpoint
 var xhr = new XMLHttpRequest();
 var url = 'http://127.0.0.1/handle-key-event';
 xhr.open('POST', url, true);
 xhr.setRequestHeader('Content-Type', 'application/json');
 xhr.onreadystatechange = function() {
     if (xhr.readyState === 4 && xhr.status === 200) {
         console.log(xhr.responseText);
     }
 };
 var data = JSON.stringify({'key': event.key});
 xhr.send(data);

 fetch('http://127.0.0.1/handle-key-event', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    'key' : event.key
  })
 })
  .then(response => {
    // Handle the response from the server
  })
  .catch(error => {
    // Handle any errors that occur
 });
});

