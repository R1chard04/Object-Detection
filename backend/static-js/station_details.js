document.addEventListener('DOMContentLoaded', function() {
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