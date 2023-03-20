document.addEventListener('DOMContentLoaded', function() {
 let btnClick = document.getElementById('show-frame-button');
 const station100_top_text = document.getElementById('top-part');
 const station100_top_colour_text = document.getElementById('top-part-colour');
 const station100_left_text = document.getElementById('left-part');
 const station100_left_colour_text = document.getElementById('left-part-colour');
 const station100_bottom_text = document.getElementById('bottom-part');
 const station100_bottom_colour_text = document.getElementById('bottom-part-colour');
 const station100_right_text = document.getElementById('right-part');
 const station100_right_colour_text = document.getElementById('right-part-colour');
 const station100_top = document.getElementById('top-part-button');
 const station100_top_color = document.getElementById('top-part-colour-button');
 const station100_left = document.getElementById('left-part-button');
 const station100_left_colour = document.getElementById('left-part-colour-button');
 const station100_bottom = document.getElementById('bottom-part-button');
 const station100_bottom_color = document.getElementById('bottom-part-colour-button');
 const station100_right = document.getElementById('right-part-button');
 const station100_right_color = document.getElementById('right-part-colour-button');

 // get the mask element
 const topMask = document.getElementById('top-mask');
 const topTimer = document.getElementById('top-timer');

 // function setting the time for generating masks
 async function topMaskTimer() {
  let remainingTime = 60;
  const intervalId = setInterval(() => {
   topTimer.style.display = 'inline-block'
   topTimer.innerHTML = '00:00:' + remainingTime;
   remainingTime--;

   if (remainingTime < 0) {
    clearInterval(intervalId);
    topTimer.style.display = 'none';
    topMask.style.display = 'none';

    // render left part
    station100_left_text.style.display = 'block';
    station100_left.style.display = 'block';
   }
  }, 1000);
 }

 const stationElement = document.querySelector('#station');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 function loadContent(){
  window.location.href = "http://127.0.0.1:5000/bt1xx/createmask/showframe/station/" + stationNumberOnly.toString();
 }

 btnClick.addEventListener('click', function() {
  loadContent();
  if (stationNumberOnly === '100'){
   station100_top_text.style.display = 'block';
   station100_top.style.display = 'block';
   if(station100_top.addEventListener('click', function() {
    station100_top_colour_text.style.display = 'block';
    station100_top_color.style.display = 'block';
    if(station100_top_color.addEventListener('click', async function() {
     topMask.style.display = 'inline-block';
     topMaskTimer();
     if(station100_left.addEventListener('click', function() {
      station100_left_colour_text.style.display = 'block';
      station100_left_colour.style.display = 'block';
      if(station100_left_colour.addEventListener('click', function() {
       station100_bottom_text.style.display = 'block';
       station100_bottom.style.display = 'block';
       if(station100_bottom.addEventListener('click', function () {
        station100_bottom_colour_text.style.display = 'block';
        station100_bottom_color.style.display = 'block';
        if(station100_bottom_color.addEventListener('click', function() {
         station100_right_text.style.display = 'block';
         station100_right.style.display = 'block';
         if(station100_right.addEventListener('click', function() {
          station100_right_colour_text.style.display = 'block';
          station100_right_color.style.display = 'block';
         }));
        }));
       }));
      }));
     }));
    }));
   }));
  }
 });
});
