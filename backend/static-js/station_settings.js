document.addEventListener('DOMContentLoaded', function() {
  // get the station number from html (100 or 120)
  const stationElement = document.querySelector('#station');
  const stationNumber = stationElement.textContent.trim();
  const numberPattern = /\d+/; // match one or more digits
  const matches = stationNumber.match(numberPattern);
  const stationNumberOnly = matches ? matches[0] : null;

  // function redirect the user to the url of the python program using iframe
  let btnClick = document.getElementById("show-frame-button");
  function loadContent(){
    
    // get the content element
    var content = document.getElementById("content");
    let url = btnClick.getAttribute("data-url");

    // create an iframe element
    var iframe = document.getElementById("iframe");
    iframe.src = url;
    iframe.style.width = "82%";
    iframe.style.height = "35rem";
    iframe.style.display = 'block';
    btnClick.style.display = 'none';

    // add the iframe element to the content element
    content.appendChild(iframe);
    
    // redirect the users to set up the change setting url
    window.location.href = btnClick.getAttribute("data-url");
  }

  // function send GET fetch API to get the frame every 0.3 seconds
  function getImage() {
    fetch('http://127.0.0.1:5000/bt1xx/get-frames/' + stationNumberOnly)
      .then(response => response.blob())
      .then(blob => {
        // create a URL for the blob object
        const url = URL.createObjectURL(blob);

        // get the iframe element and its content document
        const doc = iframe.contentDocument || iframe.contentWindow.document;

        // create an <img> element and set its src attribute to the URL
        const img = doc.createElement('img');
        img.src = url;

        // add the <img> element to the document within the iframe
        doc.body.appendChild(img);
      });
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

 window.addEventListener('keydown', (event) => {
  // fetch key events as a post request onto the 'update-ui' endpoint
  const data = {
    'key' : event.key,
    'change_frame' : true
  };
  
  fetch('http://127.0.0.1:5000/bt1xx/update-ui/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  })
  .then(response => {
    if(!response.ok){
      throw new Error('Failed to update the key event');
    }
    else{
      console.log(data)
    }
  })
  .catch(error => {
    console.error(`Error: ${error}`);
  });

  if(event.key == ','){
   focalLength = Math.max(minFocalLength, focalLength-1);
   updateIndicator();
   inputField.value = focalLength;
   // call the function to update the image
   getImage();
  } // decrease the focal length
  else if (event.key == '.'){
   focalLength = Math.max(minFocalLength, focalLength+1);
   if(focalLength > maxFocalLength){
    focalLength = maxFocalLength;
    valueSpan.textContent = focalLength;
   }
   updateIndicator();
   inputField.value = focalLength;
   // call the function to update the image
   getImage();
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
  console.log('Key pressed:', event.key);
  if(event.key == 'k'){
   brightness = Math.max(minBrightness, brightness-1);
   updateBrightnessIndicator(); 
   inputField_brightness.value = brightness;
    // call the function to update the image
    getImage();  
  } // decrease the focal length
  else if (event.key == 'l'){
   brightness = Math.max(minBrightness, brightness+1);
   if(brightness > maxBrightness){
    brightness = maxBrightness;
    valueSpan_brightness.textContent = brightness;
   }
   updateBrightnessIndicator();
   inputField_brightness.value = brightness;
   // call the function to update the image
   getImage();
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

 document.addEventListener('keydown', event => {
  if(event.key == '1') {
    switchCheckBox.checked = true;
    switchCheckBox_input.value = 'true';  
  }
  else if(event.key == '2') {
    switchCheckBox.checked = false;
    switchCheckBox_input.value = 'false';
  }
 });


 // listen to the input event when the user click 2
 const lock = document.querySelector('.lock');
 const unlock = document.querySelector('.unlock');

 let autoExposure = document.getElementById('auto_exposure_lock_input');

 document.getElementById("auto_exposure_lock_input").value = 'true';

 document.addEventListener('keydown', (event) => {
  if(event.key == '3') {
    lock.classList.remove('unlock');
    unlock.style.display = 'none';
    autoExposure.value = 'true';
  }
  else if (event.key == '4') {
    lock.classList.add('unlock');
    unlock.style.display = 'block';
    autoExposure.value = 'false';
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
  });
});