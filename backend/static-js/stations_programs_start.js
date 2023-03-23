document.addEventListener('DOMContentLoaded', function() {
 const toggleBtn = document.querySelector('.toggle_btn');
 const toggleBtnIcon = document.querySelector('.toggle_btn i');
 const dropDownMenu = document.querySelector('.dropdown_menu')

 toggleBtn.addEventListener('click', function() {
  dropDownMenu.classList.toggle('open')
 })

 // button run all the cameras
 let btnClick = document.getElementById('start-button');
 function runPrograms() {
  window.location.href = "http://127.0.0.1:5000/bt1xx/startallprograms/";
 }
 btnClick.addEventListener("click", function() {
   runPrograms();
 });
});