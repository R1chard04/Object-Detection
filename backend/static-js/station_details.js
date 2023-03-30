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

 $('input').on('change', function() {
  $(mask_section).toggleClass('blue');
 });
 
 // add the fade-in effect for the section when scroll down
 // function to check if an element is in the viewport
 function isElementInViewPort(el) {
  var rect = el.getBoundingClientRect();
  return (
   rect.top >= 0 &&
   rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
  );
 }

 // select the settings section element
 var settingSection = document.querySelector('.settings-section');
 // select the mask section element
 var maskSection = document.querySelector('.mask-section');

 // listen for scroll event
 window.addEventListener('scroll', function(event) {
  // check if the setting section is in the viewport
  if(isElementInViewPort(settingSection)) {
   // add the visisble class to animate the setting section in
   console.log(isElementInViewPort(settingSection));
   settingSection.classList.add('visible');
  } else {
   // remove the visible class to animate the settings section out
   settingSection.classList.remove('visible');
  }

  // cehck if the mask section is in the viewport
  if(isElementInViewPort(maskSection)) {
   console.log(isElementInViewPort(maskSection));
   // add the visible class to animate the mask section in
   maskSection.classList.add('visible');
  } else {
   // remove the visible class to animate the mask section out
   maskSection.classList.remove('visible');
  }
 })

 $(document).ready(function() {
  $(window).scroll(function() {
    var sectionOffset = $('.mask-section').offset().top;
    var sectionHeight = $('.mask-section').outerHeight();
    var scrollTop = $(this).scrollTop();
    var windowHeight = $(this).height();
    if (scrollTop > sectionOffset - windowHeight + sectionHeight / 2) {
      $('.mask-section').addClass('fade-in');
    }
    if (scrollTop < sectionOffset - windowHeight + sectionHeight / 2) {
      $('.mask-section').removeClass('fade-in');
    }
  });
});
})