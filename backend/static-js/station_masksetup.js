document.addEventListener('DOMContentLoaded', function() {
 let btnClick = document.getElementById('show-frame-button');

 function loadContent(){
    
  // get the content element
  var content = document.getElementById("content");
  let url = btnClick.getAttribute("data-url");

  // create an iframe element
  var iframe = document.getElementById("iframe");
  iframe.src = url;
  iframe.style.width = "50%";
  iframe.style.height = "100px";

  // add the iframe element to the content element
  content.appendChild(iframe);
 }

 btnClick.addEventListener('click', function() {
  loadContent();
 });
});