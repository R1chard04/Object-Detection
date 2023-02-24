document.addEventListener('DOMContentLoaded', function() {
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
   updateIndicator();
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
  } // decrease the focal length
  else if (event.key == '.'){
   focalLength = Math.max(minFocalLength, focalLength+1);
   updateIndicator();
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
   updateBrightnessIndicator();
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
  } // decrease the focal length
  else if (event.key == 'l'){
   brightness = Math.max(minBrightness, brightness+1);
   updateBrightnessIndicator();
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
});