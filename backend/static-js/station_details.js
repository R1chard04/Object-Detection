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
 var white_balance_lock = document.querySelector('#white_balance_lock_input').textContent;
 var auto_exposure = document.querySelector('#auto-exposure-input').textContent;
 console.log(auto_exposure)

 var slider = document.querySelector('.slider');

 function slide(element) {
  if (Boolean(element)) {
    $(slider).addClass('checked');
    $(slider).prev('input[type="checkbox"]').prop('checked', true);
  }
  else {
    $(slider).removeClass('checked');
    $(slider).prev('input[type="checkbox"]').prop('checked', false);
  }
 }

 slide(white_balance_lock);
 slide(auto_exposure);

 // select the settings section element
 var settingSection = document.querySelector('.settings-section');
 // select the mask section element
 var maskSection = document.querySelector('.mask-section');

 // detect the scrolling event and show the section that is in the viewport
 $(document).ready(function() {
  $(window).scroll(function() {
    var sectionOffset = $(settingSection).offset().top;
    var sectionHeight = $(settingSection).outerHeight();
    var masksectionOffset = $(maskSection).offset().top;
    var masksectionHeight = $(maskSection).outerHeight();
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
  });
});
})