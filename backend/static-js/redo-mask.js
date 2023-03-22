document.addEventListener('DOMContentLoaded', function() {
 const stationElement = document.querySelector('#title');
 // cut out the station number in the url
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

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

 const selection = document.querySelector('#mask-option');

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

 // function handle the click event
 function handleRedoMask() {
  // fetch the click event and send as a POST request into '/bt1xx/handle-click/' endpoint
  const data = {
   'btnClick' : true
  }
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

 const default_value = "--select--";
 const form = document.querySelector("#form-redo-mask");
 let option = document.getElementById('mask-option');
 let submit = document.querySelector('#submit');
 const text = document.querySelector('#text');

 option.value = default_value;

 option.addEventListener('change', function() {

  // handle station 100 options
  if(stationNumberOnly == '100'){
   if(submit.addEventListener('click', (event) => {
    selection.style.display = 'none';
    submit.style.display = 'none';
    // top part
    if(this.value === 'top'){
     text.innerHTML = 'Please follow the instructions to re-setup the Top mask for station 100';
     station100_top_text.style.display = 'block';
     station100_top.style.display = 'block';
     if(station100_top.addEventListener('click', (event) => {
      handleRedoMask();
      station100_top_colour_text.style.display = 'block';
      station100_top_color.style.display = 'block';
      if(station100_top_color.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(topMask, topTimer, null, null);
      }));
     }));
    }
    // left part
    else if (this.value === 'left') {
     text.innerHTML = 'Please follow the instructions to re-setup the Left mask for station 100';
     station100_left_text.style.display = 'block';
     station100_left.style.display = 'block';
     if(station100_left.addEventListener('click', (event) => {
      handleRedoMask();
      station100_left_colour_text.style.display = 'block';
      station100_left_colour.style.display = 'block';
      if(station100_left_colour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(leftMask, leftTimer, null, null);
      }));
     }));
    }
    // bottom part
    else if (this.value === 'bottom') {
     text.innerHTML = 'Please follow the instructions to re-setup the Bottom mask for station 100';
     station100_bottom_text.style.display = 'block';
     station100_bottom.style.display = 'block';
     if(station100_bottom.addEventListener('click', (event) => {
      handleRedoMask();
      station100_bottom_colour_text.style.display = 'block';
      station100_bottom_color.style.display = 'block';
      if(station100_bottom_color.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(bottomMask, bottomTimer, null, null);
      }));
     }));
    }
    // right part
    else if (this.value === 'right') {
     text.innerHTML = 'Please follow the instructions to re-setup the Right mask for station 100';
     station100_right_text.style.display = 'block';
     station100_right.style.display = 'block';
     if(station100_right.addEventListener('click', (event) => {
      handleRedoMask();
      station100_right_colour_text.style.display = 'block';
      station100_right_color.style.display = 'block';
      if(station100_right_color.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(rightMask, rightTimer, null, null);
      }));
     }));
    }
   }));
  }

  // handle station 120 options
  else if(stationNumberOnly === '120'){
   if(submit.addEventListener('click', (event) => {
    selection.style.display = 'none';
    submit.style.display = 'none';
    // topRight part
    if(this.value === 'topRight'){
     text.innerHTML = 'Please follow the instructions to re-setup the Top Right mask for station 120';
     station120_topRight_text.style.display = 'block';
     station120_topRight.style.display = 'block';
     if(station120_topRight.addEventListener('click', (event) => {
      handleRedoMask();
      station120_topRightColour_text.style.display = 'block';
      station120_topRight_colour.style.display = 'block';
      if(station120_topRight_colour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(topRightMask, topRightTimer, null, null);
      }));
     }));
    }
    else if (this.value === 'topLeft') {
     text.innerHTML = 'Please follow the instructions to re-setup the Top Left mask for station 120';
     station120_topLeft_text.style.display = 'block';
     station120_topLeft.style.display = 'block';
     if(station120_topLeft.addEventListener('click', (event) => {
      handleRedoMask();
      station120_topLeftCoulour_text.style.display = 'block';
      station120_topLeftColour.style.display = 'block';
      if(station120_topLeftColour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(topLeftMask, topLeftTimer, null, null);
      }));
     }));
    }
    else if (this.value === 'left') {
     text.innerHTML = 'Please follow the instructions to re-setup the Left mask for station 120';
     station120_left_text.style.display = 'block';
     station120_left.style.display = 'block';
     if(station120_left.addEventListener('click', function(event) {
      handleRedoMask();
      station120_left_colour_text.style.display = 'block';
      station120_leftColour.style.display = 'block';
      if(station120_leftColour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(left120Mask, left120Timer, null, null);
      }));
     }));
    }
    else if (this.value === 'bottomLeft') {
     text.innerHTML = 'Please follow the instructions to re-setup the Bottom Left mask for station 120';
     station120_bottomLeft_text.style.display = 'block';
     station120_bottomLeft.style.display = 'block';
     if(station120_bottomLeft.addEventListener('click', (event) => {
      handleRedoMask();
      station120_bottomLeftColour_text.style.display = 'block';
      station120_bottomLeftColour.style.display = 'block';
      if(station120_bottomLeftColour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(bottomLeftMask, bottomLeftTimer, null, null);
      }));
     }));
    }
    else if (this.value === 'bottomRight') {
     text.innerHTML = 'Please follow the instructions to re-setup the Bottom Right mask for station 120';
     station120_bottomRight_text.style.display = 'block';
     station120_bottomRight.style.display = 'block';
     if(station120_bottomRight.addEventListener('click', (event) => {
      handleRedoMask();
      station120_bottomRightColour_text.style.display = 'block';
      station120_bottomRightColour.style.display = 'block';
      if(station120_bottomRightColour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(bottomRightMask, bottomRightTimer, null, null);
      }));
     }));
    }
    else if (this.value === 'right') {
     text.innerHTML = 'Please follow the instructions to re-setup the Right mask for station 120';
     station120_right_text.style.display = 'block';
     station120_right.style.display = 'block';
     if(station120_right.addEventListener('click', (event) => {
      handleRedoMask();
      station120_right_colour_text.style.display = 'block';
      station120_rightColour.style.display = 'block';
      if(station120_rightColour.addEventListener('click', (event) => {
       handleRedoMask();
       Timer(right120Mask, right120Timer, null, null);
      }));
     }));
    }
   }));
  }
 })

})