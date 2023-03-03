// Create a new WebSocket connection to the Python server
// var socket = io.connect('http://127.0.0.1:5000/bt1xx/station/<int:station_number>/settings');

document.addEventListener('DOMContentLoaded', function() {
  // function redirect the user to the url of the python program using iframe
  let btnClick = document.getElementById("show-frame-button");
  function loadContent(){
    
    // get the content element
    var content = document.getElementById("content");
    let url = btnClick.getAttribute("data-url");

    // create an iframe element
    var iframe = document.getElementById("iframe");
    iframe.src = url;
    iframe.style.width = "50%";
    iframe.style.height = "100px";

    // add the iframe element to the content element
    content.appendChild(iframe);
  }

  btnClick.addEventListener("click", function() {
    loadContent();
  });

  // Update the value of the focal length in real-time when the users drag the thumb
 const indicator = document.querySelector('.indicator');
 const bar = indicator.querySelector('.indicator .bar');
 const thumb = indicator.querySelector('.indicator .thumb');
 const valueSpan = document.getElementById('focal-length-value');
 // get the input value from the focal length input field
 const inputField = document.getElementById('focal_length_setting_input');

 let focalLength = Number(inputField.value); // initial focal length value
 const minFocalLength = Number(inputField.getAttribute('min')); 
 const maxFocalLength = Number(inputField.getAttribute('max'));

 function updateIndicator() {
  const percentage = (focalLength - minFocalLength)/(maxFocalLength - minFocalLength);
  bar.style.width = percentage * 100 + "%";
  thumb.style.left = percentage * 100 + "%";
  valueSpan.textContent = focalLength;
 }

 updateIndicator(); // initialize the indicator

 // detect clicking event to change the focal length
 thumb.addEventListener('mousedown', (event) => {
  event.preventDefault();

  const startX = event.clientX;
  const startFocalLength = focalLength;

  function handMouseMove(event) {
   const deltaX = event.clientX - startX;
   const deltaFocalLength = Math.round(deltaX / indicator.clientWidth * (maxFocalLength - minFocalLength));
   focalLength = Math.max(minFocalLength, Math.min(startFocalLength + deltaFocalLength));
   if(focalLength > maxFocalLength){
    focalLength = maxFocalLength;
    valueSpan.textContent = focalLength;
   }
   updateIndicator();
   inputField.value = focalLength;
  }

  function handleMouseUp() {
   document.removeEventListener('mousemove', handMouseMove);
   document.removeEventListener('mouseup', handleMouseUp);
  }
  
  document.addEventListener('mousemove', handMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
 });

 document.addEventListener('keydown', (event) => {
  if(event.key == ','){
   focalLength = Math.max(minFocalLength, focalLength-1);
   updateIndicator();
   inputField.value = focalLength;
    // send the key code to the python server
    socket.send(event.key.toString());
  } // decrease the focal length
  else if (event.key == '.'){
   focalLength = Math.max(minFocalLength, focalLength+1);
   if(focalLength > maxFocalLength){
    focalLength = maxFocalLength;
    valueSpan.textContent = focalLength;
   }
   updateIndicator();
   inputField.value = focalLength;
    // send the key code to the python server
    socket.send(event.key.toString());
  }
 });

 inputField.addEventListener('input', () => {
  const inputVal = Number(inputField.value);
  if(isNaN(inputVal) || inputVal < minFocalLength || inputVal > maxFocalLength){
   inputField.value = focalLength;
  } else {
   focalLength = inputVal;
   updateIndicator();
  }
 });

 // Update the value of the brightness indicator bar when listening to an event
 const brightness_indicator = document.querySelector('.indicator-brightness');
 const brightness_bar = document.querySelector('.indicator-brightness .bar-brightness');
 const thumb_brightness = document.querySelector('.indicator-brightness .thumb-brightness');
 const valueSpan_brightness = document.getElementById('brightness-value');
 // get the input from the brightness input field
 const inputField_brightness = document.getElementById('brightness-input');

 let brightness = Number(inputField_brightness.value); // initial brightness value
 const minBrightness = Number(inputField_brightness.getAttribute('min')); 
 const maxBrightness= Number(inputField_brightness.getAttribute('max'));

 function updateBrightnessIndicator() {
  const percentage_brightness = (brightness - minBrightness)/(maxBrightness - minBrightness);
  brightness_bar.style.width = percentage_brightness * 100 + "%";
  thumb_brightness.style.left = percentage_brightness * 100 + "%";
  valueSpan_brightness.textContent = brightness;
 }

 updateBrightnessIndicator(); // initialize the brightness indicator

 // detect clicking event to change the focal length
 thumb_brightness.addEventListener('mousedown', (event) => {
  event.preventDefault();

  const startX_brightness = event.clientX;
  const startBrightnessLength = brightness;

  function handMouseMove(event) {
   const deltaX_brightness = event.clientX - startX_brightness;
   const deltaBrightness = Math.round(deltaX_brightness / brightness_indicator.clientWidth * (maxBrightness - minBrightness));
   brightness = Math.max(minBrightness, Math.min(startBrightnessLength + deltaBrightness));
   if(brightness > maxBrightness){
    brightness = maxBrightness;
    valueSpan_brightness.textContent = brightness;
   }
   updateBrightnessIndicator();
   inputField_brightness.value = brightness;
  }

  function handleMouseUp() {
   document.removeEventListener('mousemove', handMouseMove);
   document.removeEventListener('mouseup', handleMouseUp);
  }
  
  document.addEventListener('mousemove', handMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
 });

 document.addEventListener('keydown', (event) => {
  if(event.key == 'k'){
   brightness = Math.max(minBrightness, brightness-1);
   updateBrightnessIndicator(); 
   inputField_brightness.value = brightness;  
   // send the key code to the python server
   socket.send(event.key.toString());
  } // decrease the focal length
  else if (event.key == 'l'){
   brightness = Math.max(minBrightness, brightness+1);
   if(brightness > maxBrightness){
    brightness = maxBrightness;
    valueSpan_brightness.textContent = brightness;
   }
   updateBrightnessIndicator();
   inputField_brightness.value = brightness;
   // send the key code to the python server
   socket.send(event.key.toString());
  }
 });

 inputField_brightness.addEventListener('input', () => {
  const inputVal_brightness = Number(inputField_brightness.value);
  if(isNaN(inputVal_brightness) || inputVal_brightness < minBrightness || inputVal_brightness > maxBrightness){
   inputField_brightness.value = brightness;
  } else {
   brightness = inputVal_brightness;
   updateBrightnessIndicator();
  }
 });

 // listen to the input event when the user click 1
 const switchCheckBox = document.querySelector('.switch input[type="checkbox"]');
 let switchCheckBox_input = document.getElementById('white_balance_lock_input');
  if(switchCheckBox.value == 'on'){
    switchCheckBox_input.value = 1;
    switchCheckBox_input.value = !!(switchCheckBox_input.value)
  }
  else {
    switchCheckBox_input.value = 0;
    switchCheckBox_input.value = !!(switchCheckBox_input.value)
  }

 document.addEventListener('keydown', event => {
  if(event.key == '1') {
    switchCheckBox.checked = !switchCheckBox.checked;
    if(switchCheckBox.value == 'on'){
      switchCheckBox_input.value = 1;
      switchCheckBox_input.value = !!(switchCheckBox_input.value)
    }
    else {
      switchCheckBox_input.value = 0;
      switchCheckBox_input.value = !!(switchCheckBox_input.value)
    }
  }
 });

 // listen to the input event when the user click 2
 const lock = document.querySelector('.lock');
 const unlock = document.querySelector('.unlock');

 let isLocked = true;
  document.getElementById("auto_exposure_lock_input").value = isLocked;

 function toggleLock() {
  isLocked = !isLocked;
  if(isLocked) {
    lock.classList.remove('unlock');
    unlock.style.display = 'none';
  } else {
    lock.classList.add('unlock');
    unlock.style.display = 'block';
  }
 }

 lock.addEventListener('click', toggleLock);
 unlock.addEventListener('click', toggleLock);
 document.addEventListener('keydown', (event) => {
  if(event.key == '2') {
    toggleLock();
    document.getElementById("auto_exposure_lock_input").value = isLocked;
  }
 });

 // event for the saving button
 let btn = document.querySelector('.button');

  btn.addEventListener("click", active);

  function active() {
    btn.classList.toggle('is_active');
  }

  // event for the logo
  var logo = document.getElementById('logo');
  const stationElement = document.querySelector('#station');
  // cut out the station number in the url
  const stationNumber = stationElement.textContent.trim();
  const numberPattern = /\d+/; // match one or more digits
  const matches = stationNumber.match(numberPattern);
  const stationNumberOnly = matches ? matches[0] : null;

  function goToSettingPage() {
    window.location.href = "http://127.0.0.1:5000/bt1xx/station/" + stationNumberOnly.toString();
  }

  logo.addEventListener("click", function() {
    goToSettingPage();
  });

  // hamburger
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('ul');
  const bars = document.querySelectorAll('.bar');

  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    bars.forEach(bar => {
      bar.classList.toggle('closed');
    });
  });

  // after the users submit the form
  document.querySelector("#form").addEventListener("submit", function(event) {
    event.preventDefault();
    // send all the input fields to the database when the users hit submit button
    document.querySelector("#form").submit()
  })
});