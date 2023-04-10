document.addEventListener('DOMContentLoaded', function() {

 // get the station number from html (100 or 120)
 const stationElement = document.querySelector('#station');
 const stationNumber = stationElement.textContent.trim();
 const numberPattern = /\d+/; // match one or more digits
 const matches = stationNumber.match(numberPattern);
 const stationNumberOnly = matches ? matches[0] : null;

 // read in the params.json file using Fetch API
 const json_url = 'http://127.0.0.1:5000/params.json';
 console.log(json_url);

 const passref_section = document.querySelector('.passref-section');

 fetch(json_url)
  .then((response) => response.json())
  .then((json => passRef(json=json)))
  .catch(error => {
    console.log(`Error: ${error}`)
  });

 // add the css styles for passref section
 var styles = `
  #passref_station${stationNumberOnly} {
    font-weight: bold;
    font-size: 25px;
    space-between: 20rem;
  }
 `
 var stylesheet = document.createElement("style");
 stylesheet.innerText = styles;
 document.head.appendChild(stylesheet);

 function passRef(json) { // this is a function that append the HTML elements as a list of the passrefs depend on the parts
  const partList = json[`station${stationNumberOnly}`]['parts']; // the list of all the parts for .this station
  const passref_list = json[`station${stationNumberOnly}`]['passref']; // passref for .this station
  for(var i = 0; i < partList.length; i++) {
    const node = document.createElement("p");
    const newPartList = partList[i].charAt(0).toUpperCase() + partList[i].slice(1);
    const TextNode = document.createTextNode(`${newPartList}          :       ${passref_list[i]}`);
    node.appendChild(TextNode);
    // set the id for our node
    node.setAttribute('id', `passref_station${stationNumberOnly}`);  
    passref_section.appendChild(node);
  }
 }
 
 let arrow = document.querySelectorAll('.arrow');
 for(var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
   let arrowParent = e.target.parentElement.parentElement;
   arrowParent.classList.toggle("showMenu");
  });
 }

 let sidebar = document.querySelector(".sidebar");
 let sidebarBtn = document.querySelector(".bx-menu");
 sidebarBtn.addEventListener('click', () => {
  sidebar.classList.toggle("close");
 });

 let mask_section = document.querySelector('.mask-section');

 // toggle the blue background when scroll the carousel
 $('input').on('change', function() {
  $(mask_section).toggleClass('blue');
 });

 // turn on the slider if the value of the white balance and auto exposure lock is True
 let white_balance_lock = document.querySelector('#white_balance_lock_input').textContent.toLowerCase();
 console.log(white_balance_lock);
 let auto_exposure_lock = document.querySelector('#auto_exposure_lock_input').textContent.toLowerCase();
 console.log(auto_exposure_lock);
 let white_balance_lock_checkbox = document.querySelector('#white_balance_lock');
 let auto_exposure_lock_checkbox = document.querySelector('#auto_exposure_lock');

 let boolean_white_balance_lock = (white_balance_lock === 'true');
 let boolean_auto_exposure_lock = (auto_exposure_lock === 'true');
 console.log(boolean_white_balance_lock);
 console.log(boolean_auto_exposure_lock);

 function checkSlider(boolean_white_balance_lock, boolean_auto_exposure_lock) {
  if(boolean_white_balance_lock) {
    // if the data passed in for white balance lock is true, then slide the slider to the right
    white_balance_lock_checkbox.checked = true;
  }
  else {
    // if the data passed in for white balance lock is false, then slide the slider to the left
    white_balance_lock_checkbox.checked = false;
  }

  if(boolean_auto_exposure_lock) {
    // if the data passed in for auto exposure lock is true, then slide the slider to the right
    auto_exposure_lock_checkbox.checked = true;
  }
  else {
    // if the data passed in for auto exposure lock is false, then slide the slider to the left
    auto_exposure_lock_checkbox.checked = false;
  }
 }
 
 // check the slider for both elements
 checkSlider(boolean_white_balance_lock, boolean_auto_exposure_lock);
 
 // select the settings section element
 var settingSection = document.querySelector('.settings-section');
 // select the mask section element
 var maskSection = document.querySelector('.mask-section');
 // select the error section element
 var errorSection = document.querySelector('.error-section');

 // detect the scrolling event and show the section that is in the viewport
 $(document).ready(function() {
  $(window).scroll(function() {
    var sectionOffset = $(settingSection).offset().top;
    var sectionHeight = $(settingSection).outerHeight();
    var masksectionOffset = $(maskSection).offset().top;
    var masksectionHeight = $(maskSection).outerHeight();
    var errorsectionOffset = $(errorSection).offset().top;
    var errorsectionHeight = $(errorSection).outerHeight();
    var scrollTop = $(this).scrollTop();
    var windowHeight = $(this).height();
    if (scrollTop > sectionOffset - windowHeight + sectionHeight / 2) {
      $(settingSection).addClass('visible');
    }
    if (scrollTop < sectionOffset - windowHeight + sectionHeight / 2) {
      $(settingSection).removeClass('visible');
    }
    if (scrollTop > masksectionOffset - windowHeight + masksectionHeight / 2) {
     $(maskSection).addClass('visible');
    }
    if (scrollTop < masksectionOffset - windowHeight + masksectionHeight / 2) {
     $(maskSection).removeClass('visible');
    }
    if (scrollTop > errorsectionOffset - windowHeight + errorsectionHeight / 2) {
      $(errorSection).addClass('visible');
     }
    if (scrollTop < errorsectionHeight - windowHeight + errorsectionHeight / 2) {
      $(errorSection).removeClass('visible');
    }
  });
});
})