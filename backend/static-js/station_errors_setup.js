document.addEventListener('DOMContentLoaded', function() {
 let btnClick = document.getElementById('show-frame-button');
 const btnClickEvent = document.getElementById('instructions-box');

 const stationElement = document.querySelector('#station');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 // event for the logo
 var logo = document.getElementById('logo');

 function goToSettingPage() {
   window.location.href = "http://127.0.0.1:5000/bt1xx/station/" + stationNumberOnly.toString();
 }

 logo.addEventListener("click", function() {
   goToSettingPage();
 });

 // add an async and await function to return the promise from the server
 const sandHourGlass = document.querySelector('.sand-hourglass');

 function loadContent(){ // function handles the event after the user click the showframe button
  btnClick.style.display = 'none';
  window.location.href = "http://127.0.0.1:5000/bt1xx/errors/showframe/station/" + stationNumberOnly.toString();
  btnClickEvent.style.display = 'inline-block';
  sandHourGlass.style.display = 'inline-block';
 }
 
 function waitResponseFromServer() {
  let remainingTime = 20000; // wait time to get the server response
  return new Promise(resolve => {
   setTimeout(() => {
    resolve(`Get the response from the server successfully!`);
   }, remainingTime) 
  })
 }
 waitResponseFromServer().catch(() => {}); // attempt to swallow all the errors that were caught

 btnClick.addEventListener('click', async function() {
  loadContent();
  // await to get the response from the server
  console.log(`Waiting for response from the server ....`);
  const returnPromise = await waitResponseFromServer();
  console.log(returnPromise);
  sandHourGlass.style.display = 'none'; // hide the loading effect after receiving the response from the server
 });
});