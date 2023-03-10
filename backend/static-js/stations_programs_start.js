document.addEventListener('DOMContentLoaded', function() {
 let btnClick = document.getElementById('start-button');
 function runPrograms() {
  window.location.href = "http://127.0.0.1:5000/bt1xx/startallprograms/";
 }
 btnClick.addEventListener("click", function() {
   runPrograms();
 });
});