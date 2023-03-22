document.addEventListener('DOMContentLoaded', function() {
 const stationElement = document.querySelector('#title');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 const default_value = "1";
 const form = document.querySelector("#form-redo-mask");
 let option = document.getElementById('mask-option');
 let submit = document.getElementById('submit');
 const url = "http://127.0.0.1:5000/bt1xx/handle-redo-mask/" + stationNumberOnly;

 option.value = default_value;

 // function redirect the user to handle redo mask url
 form.addEventListener('submit', async function(event) {
  event.preventDefault(); 

  const formData = new FormData(form);

  // using formData here, send it to the server using fetch API
  const response = await fetch(url, {
   method : 'POST',
   body: formData,
  });

  if(response.ok) {
   window.location.href = url;
  }
 })

 // add event listener to form submit button
 

 option.addEventListener('change', function() {

  if(this.value === '2'){
   submit.style.display = 'block';
   
  }
 })

})