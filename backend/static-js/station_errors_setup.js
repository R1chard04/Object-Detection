document.addEventListener('DOMContentLoaded', function() {
 let btnClick = document.getElementById('show-frame-button');
 const btnClickEvent = document.getElementById('instructions-box');

 const stationElement = document.querySelector('#station');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 function loadContent(){
  window.location.href = "http://127.0.0.1:5000/bt1xx/errors/showframe/station/" + stationNumberOnly.toString();
 }

 btnClick.addEventListener('click', function() {
  loadContent();
  btnClickEvent.style.display = 'inline-block';
 });
});