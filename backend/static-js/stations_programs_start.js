document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.querySelector('.toggle_btn');
  const toggleBtnIcon = document.querySelector('.toggle_btn i');
  const dropDownMenu = document.querySelector('.dropdown_menu');
  
  toggleBtn.onclick = function () {
   dropDownMenu.classList.toggle('open');
   const isOpen = dropDownMenu.classList.contains('open');

   toggleBtnIcon.classList = isOpen
    ? 'fa-solid fa-xmark'
    : 'fa-solid fa-bars'
  }
 // button run all the cameras
 let btnClick = document.querySelector('.action_btn');
 function runPrograms() {
  window.location.href = "http://127.0.0.1:5000/bt1xx/startallprograms/";
 }
 btnClick.addEventListener("click", function() {
   runPrograms();
 });
});