document.addEventListener('DOMContentLoaded', function() {
  // fetch to get the number of stations are running
  const get_cameras_url = 'http://127.0.0.1:5000/bt1xx/get-all-cameras/';

  // get the sand hour glasses
  const sandHourGlass = document.querySelector('.sand-hourglass');

  sandHourGlass.style.display = 'inline-block';
  
  // function set time await for the response from the server
  function LoadingTimer() {
    let remainingTime = 20000; //wait for 15 seconds
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(`Successfully got the response from the server!`);
      }, remainingTime);
    })
  };

  LoadingTimer().catch(() => {}) // attempt to swallow all the errors

  // function callBack to get the promise from the user
  async function callBack() {
    // await for the response from the server
    console.log(`Waiting for response from the server....`);
    const loading_response = await LoadingTimer();
    console.log(loading_response);
  }


  // fetch and await for the promise to return the data
  async function get_all_cameras() {
   await callBack();
   sandHourGlass.style.display = 'none';

   // return the promise 
   return new Promise(async function (resolve) {
     // async the response from the server
     const response = await fetch(get_cameras_url, {
      method: 'GET',
      headers : {
       'Content-Type' : 'application/json'
      }
     });
     console.log(response);
     if(!response.ok) {
      throw new Error(`Failed to get the response from the server: ${response.catch(error => {
       `${error}`
      })}!`);
     } else {
      // resolve
      console.log(`Get the response successfully from the server with status code: ${response.status}`);
      response.json().then(data => resolve(data));
     }
   })
  }

  // run the function and receive the promise response
  const promiseResponse = get_all_cameras();

  // when the promise is resolved then do the following
  promiseResponse.then(data => renderCameraMonitorViewPort(num_cameras=data['cameras']['cameras'], station_cam=data['cameras']['station_cam']));


  // get the element where the child should be appended to
  const subheadings = document.querySelector('.subheadings');

  // function append the child for the number of cameras viewport
  function renderCameraMonitorViewPort(num_cameras, station_cam) {
   for(let i = 0; i < num_cameras; i++){
    let node = document.createElement('p');
    let viewPortnode = document.createElement('div');
    let nodeText = document.createTextNode(`Station ${station_cam[`${i + 1}`]} camera:`);
    node.appendChild(nodeText);
    node.appendChild(viewPortnode);
    viewPortnode.style.display = 'inline-block';
    // set the id for the new node
    node.setAttribute('id', `station_${station_cam[`${i+1}`]}`);
    viewPortnode.setAttribute('id', `station_${station_cam[`${i+1}`]}_viewPort`);
    subheadings.appendChild(node);
   }
  };
  
  // function using FETCH API to make a GET request to the server to get the result when running the cameras
  const get_result_url_100 = 'http://127.0.0.1:5000/bt1xx/get-result/100/';
  const get_result_url_120 = 'http://127.0.0.1:5000/bt1xx/get-result/120/';
  
  async function main() {
    function get_data(url) {
      setInterval(() => {       
        fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type' : 'application/json'
          }
        })
        .then(response => {
          if(!response.ok){
            throw new Error (`Failed to get the response from the server`);
          } else {
            return response.json();
          }
        })
        .then(data => {
          console.log(data[`get_data`]);
          // Do something with the data
          renderResultElements(data);
        })
        .catch(error => {
          console.error(`Error: ${error}`);
        })
      }, 500);
    };

    // call get_data functions to get the data from 2 urls
    get_data(get_result_url_100);
    get_data(get_result_url_120);  
  }

  main();

  // function takes in the array and round it each element to 2 decimal places
  function roundTo2Decimals(array2round) {
    for(let i = 0; i < array2round.length; i++) {
      array2round[i] = array2round[i].toFixed(2); // round to 2 decimal places
    }
  }
  

  // function to append the children element for error, result and timing
  function renderResultElements(data) {
    let viewPortnode = document.querySelector(`#station_${data[`get_data`][`station_number`]}_viewPort`);
    // clear the content after displaying to render new values
    viewPortnode.innerHTML = '';

    // get the passref, error, result, timing
    let passref = (data[`get_data`][`passref`]);
    let error = (data[`get_data`][`error`]);
    let timing = (data[`get_data`][`timing`]);

    // round each array to 2 decimals places
    roundTo2Decimals(passref);
    roundTo2Decimals(error);
    roundTo2Decimals(timing);

    var passrefNode = document.createElement('p');
    var errorNode = document.createElement('p');
    var resultNode = document.createElement('p');
    var timingNode = document.createElement('p');

    var passrefTextNode = document.createTextNode(`Passing References Station ${data[`get_data`][`station_number`]}: `);
    var passrefValueNode = document.createTextNode(`${passref.join(',      ')}`);
    console.log(passrefValueNode);

    var errorTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Errors: `);
    var errorValueNode = document.createTextNode(`${error.join(',      ')}`);
    console.log(errorValueNode);

    var resultTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Result: `);
    var resultValueNode = document.createTextNode(`${(data[`get_data`][`result`]).join(',      ')}`);
    console.log(resultValueNode);

    var timingTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Time Stamps: `);
    var timingValueNode = document.createTextNode(`${timing.join(',      ')}`);
    console.log(timingValueNode);

    passrefNode.appendChild(passrefTextNode);
    passrefNode.appendChild(passrefValueNode);

    errorNode.appendChild(errorTextNode);
    errorNode.appendChild(errorValueNode);

    resultNode.appendChild(resultTextNode);
    resultNode.appendChild(resultValueNode);

    timingNode.appendChild(timingTextNode);
    timingNode.appendChild(timingValueNode);

    // set the IDs for these nodes
    passrefNode.setAttribute('id', `station_${data[`get_data`][`station_number`]}_passref`);
    errorNode.setAttribute('id', `station_${data[`get_data`][`station_number`]}_error`);
    resultNode.setAttribute('id', `staiton_${data[`get_data`][`station_number`]}_result`);
    timingNode.setAttribute('id', `station_${data[`get_data`][`station_number`]}_timing`);

    // append child to the viewPort
    viewPortnode.appendChild(passrefNode);
    viewPortnode.appendChild(errorNode);
    viewPortnode.appendChild(resultNode);
    viewPortnode.appendChild(timingNode);
  };
 }

);