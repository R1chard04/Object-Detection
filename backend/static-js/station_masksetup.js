document.addEventListener('DOMContentLoaded', function() {
 const stationElement = document.querySelector('#station');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 let btnClick = document.getElementById('show-frame-button');
 let redoMaskBtn = document.getElementById('redo-mask-chosen');

 redoMaskBtn.addEventListener('click', function() {
  window.location.href = 'http://127.0.0.1:5000/bt1xx/redo-mask/' + stationNumberOnly;
 })

 // get all the elements in station 100
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

 // get all the elements in station 120
 const station120_topRight_text = document.getElementById('topRight-part');
 const station120_topRightColour_text = document.getElementById('topRight-part-colour');
 const station120_topLeft_text = document.getElementById('topLeft-part');
 const station120_topLeftCoulour_text = document.getElementById('topLeft-part-colour');
 const station120_left_text = document.getElementById('left120-part');
 const station120_left_colour_text = document.getElementById('left120-part-colour');
 const station120_bottomLeft_text = document.getElementById('bottomLeft-part');
 const station120_bottomLeftColour_text = document.getElementById('bottomLeft-part-colour');
 const station120_bottomRight_text = document.getElementById('bottomRight-part');
 const station120_bottomRightColour_text = document.getElementById('bottomRight-part-colour');
 const station120_right_text = document.getElementById('right120-part');
 const station120_right_colour_text = document.getElementById('right120-part-colour');
 const station120_topRight = document.getElementById('topRight-part-button');
 const station120_topRight_colour = document.getElementById('topRight-part-colour-button');
 const station120_topLeft = document.getElementById('topLeft-part-button');
 const station120_topLeftColour = document.getElementById('topLeft-part-colour-button');
 const station120_left = document.getElementById('left120-part-button');
 const station120_leftColour = document.getElementById('left120-part-colour-button');
 const station120_bottomLeft = document.getElementById('bottomLeft-part-button');
 const station120_bottomLeftColour = document.getElementById('bottomLeft-part-colour-button');
 const station120_bottomRight = document.getElementById('bottomRight-part-button');
 const station120_bottomRightColour = document.getElementById('bottomRight-part-colour-button');
 const station120_right = document.getElementById('right120-part-button');
 const station120_rightColour = document.getElementById('right120-part-colour-button');

 // get the mask element for station 100
 const topMask = document.getElementById('top-mask');
 const topTimer = document.getElementById('top-timer');
 const leftMask = document.getElementById('left-mask');
 const leftTimer = document.getElementById('left-timer');
 const bottomMask = document.getElementById('bottom-mask');
 const bottomTimer = document.getElementById('bottom-timer');
 const rightMask = document.getElementById('right-mask');
 const rightTimer = document.getElementById('right-timer');

 // get the mask element for station 120
 const topRightMask = document.getElementById('topRight-mask');
 const topRightTimer = document.getElementById('topRight-timer');
 const topLeftMask = document.getElementById('topLeft-mask');
 const topLeftTimer = document.getElementById('topLeft-timer');
 const left120Mask = document.getElementById('left120-mask');
 const left120Timer = document.getElementById('left120-timer');
 const bottomRightMask = document.getElementById('bottomRight-mask');
 const bottomRightTimer = document.getElementById('bottomRight-timer');
 const bottomLeftMask = document.getElementById('bottomLeft-mask');
 const bottomLeftTimer = document.getElementById('bottomLeft-timer');
 const right120Mask = document.getElementById('right120-mask');
 const right120Timer = document.getElementById('right120-timer');

 // function setting the time for generating masks
 async function Timer(mask, timer, text, button) {
  let remainingTime = 60;
  mask.style.display = 'inline-block';
  const intervalId = setInterval(() => {
   timer.style.display = 'inline-block'
   timer.innerHTML = '00:00:' + remainingTime;
   remainingTime--;

   if (remainingTime < 0) {
    clearInterval(intervalId);
    timer.style.display = 'none';
    mask.style.display = 'none';

    // render a text and a button
    text.style.display = 'block';
    button.style.display = 'block';
   }
  }, 1000);
 }

 // function detect the 'click' event and send the event to the URL server
 function handleClickEvent() {
  // fetch the click event as a post request onto the 'handle-click' endpoint
  const data = {'btnclick' : true}
  fetch('http://127.0.0.1:5000/bt1xx/handle-click/', {
   method : 'POST',
   headers: {'Content-Type' : 'application/json'},
   body : JSON.stringify(data)
  })
  .then(response => {
   if(!response.ok){
    throw new Error('Failed to handle click event');
   }
   else {
    console.log(data);
   }
  })
  .catch(error => {
   console.error(`Error: ${error}`);
  })
 }

 function loadContent(){
  window.location.href = "http://127.0.0.1:5000/bt1xx/createmask/showframe/station/" + stationNumberOnly.toString();
 }

 btnClick.addEventListener('click', function() {
  loadContent();
  if (stationNumberOnly === '100'){
   station100_top_text.style.display = 'block';
   station100_top.style.display = 'block';
   if(station100_top.addEventListener('click', function() {
    handleClickEvent();
    station100_top_colour_text.style.display = 'block';
    station100_top_color.style.display = 'block';
    if(station100_top_color.addEventListener('click', async function() {
     handleClickEvent();
     Timer(topMask, topTimer, station100_left_text, station100_left);
     if(station100_left.addEventListener('click', function() {
      handleClickEvent();
      station100_left_colour_text.style.display = 'block';
      station100_left_colour.style.display = 'block';
      if(station100_left_colour.addEventListener('click', function() {
       handleClickEvent();
       Timer(leftMask, leftTimer, station100_bottom_text, station100_bottom)
       if(station100_bottom.addEventListener('click', function () {
        handleClickEvent();
        station100_bottom_colour_text.style.display = 'block';
        station100_bottom_color.style.display = 'block';
        if(station100_bottom_color.addEventListener('click', function() {
         handleClickEvent();
         Timer(bottomMask, bottomTimer, station100_right_text, station100_right)
         if(station100_right.addEventListener('click', function() {
          handleClickEvent();
          station100_right_colour_text.style.display = 'block';
          station100_right_color.style.display = 'block';
          if(station100_right_color.addEventListener('click', function() {
           handleClickEvent();
           Timer(rightMask, right120Timer, null, null);
          }));
         }));
        }));
       }));
      }));
     }));
    }));
   }));
  }
  else if (stationNumberOnly === '120'){
   station120_topRight_text.style.display = 'block';
   station120_topRight.style.display = 'block';
   if(station120_topRight.addEventListener('click', function() {
    handleClickEvent();
    station120_topRightColour_text.style.display = 'block';
    station120_topRight_colour.style.display = 'block';
    if(station120_topRight_colour.addEventListener('click', function() {
     handleClickEvent();
     Timer(topRightMask, topRightTimer, station120_topLeft_text, station120_topLeft);
     if(station120_topLeft.addEventListener('click', function() {
      handleClickEvent();
      station120_topLeftCoulour_text.style.display = 'block';
      station120_topLeftColour.style.display = 'block';
      if(station120_topLeftColour.addEventListener('click', function() {
       handleClickEvent();
       Timer(topLeftMask, topLeftTimer, station120_left_text, station120_left);
       if(station120_left.addEventListener('click', function() {
        handleClickEvent();
        station120_left_colour_text.style.display = 'block';
        station120_leftColour.style.display = 'block';
        if(station120_leftColour.addEventListener('click', function() {
         handleClickEvent();
         Timer(left120Mask, left120Timer, station120_bottomLeft_text, station120_bottomLeft);
         if(station120_bottomLeft.addEventListener('click', function() {
          handleClickEvent();
          station120_bottomLeftColour_text.style.display = 'block';
          station120_bottomLeftColour.style.display = 'block';
          if(station120_bottomLeftColour.addEventListener('click', function() {
           handleClickEvent();
           Timer(bottomLeftMask, bottomLeftTimer, station120_bottomRight_text, station120_bottomRight);
           if(station120_bottomRight.addEventListener('click', function() {
            handleClickEvent();
            station120_bottomRightColour_text.style.display = 'block';
            station120_bottomRightColour.style.display = 'block';
            if(station120_bottomRightColour.addEventListener('click', function() {
             handleClickEvent();
             Timer(bottomRightMask, bottomRightTimer, station120_right_text, station120_right);
             if(station120_right.addEventListener('click', function() {
              handleClickEvent();
              station120_right_colour_text.style.display = 'block';
              station120_rightColour.style.display = 'block';
              if(station120_rightColour.addEventListener('click', function() {
               handleClickEvent();
               Timer(right120Mask, right120Timer, null, null);
              }));
             }));
            }));
           }));
          }));
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
