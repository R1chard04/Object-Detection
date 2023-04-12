document.addEventListener('DOMContentLoaded', function() {
  // fetch to get the number of stations are running
  const get_cameras_url = 'http://127.0.0.1:5000/bt1xx/get-all-cameras/';

  // get the sand hour glasses
  const sandHourGlass = document.querySelector('.sand-hourglass');
  const sandHourGlass2 = document.querySelector('.sand-hourglass-2');

  sandHourGlass.style.display = 'inline-block';
  sandHourGlass2.style.display = 'inline-block';
  

  // function set time await for the response from the server
  function LoadingTimer() {
    let remainingTime = 17000; //wait for 15 seconds
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(`Successfully got the response from the server!`);
      }, remainingTime);
    })
  };

  LoadingTimer().catch(() => {}) // attempt to swallow all the errors

  // fetch and await for the promise to return the data
  function get_all_cameras() {
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

  async function callBack() {
    // await for the response from the server
    console.log(`Waiting for response from the server ....`);
    const response = await LoadingTimer();
    console.log(response);
    sandHourGlass.style.display = 'none';
    sandHourGlass2.style.display = 'none';
  }

  // main threading
  async function main() {
    await callBack();

    function get_results(url) {
      setInterval(() => {
        // return the promise when waiting for the response
        return new Promise(async function (resolve, reject) {
          // async the response from the server
          const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type' : 'application/json'
            }
          });
          console.log(response);
          // check if the response returns the status code of 200
          if(!response.ok) {
            throw new Error (`Error while handling the GET request to the server ${response.catch(error => {
              `${error}`
            })}`);
          } else {
            // resolve
            console.log(`Getting the response from the server successfully with the status code: ${response.status}`);
            response.json().then(data => resolve(data));
          };
        })
      }, 1000)    
    };
  
    // call the function to get the response from the server when the promise is returned
    const resultPromise_100 = get_results(get_result_url_100);
    const resultPromise_120 = get_results(get_result_url_120);
    
    resultPromise_100.then(data => renderResultElements(data));
    resultPromise_120.then(data => renderResultElements(data));
  }
  
  main();

  // function to append the children element for error, result and timing
  function renderResultElements(data) {
    var passrefNode = document.createElement('p');
    var errorNode = document.createElement('p');
    var resultNode = document.createElement('p');
    var timingNode = document.createElement('p');
    var passrefTextNode = document.createTextNode(`Passing References Station ${data[`get_data`][`station_number`]}: `);
    var passrefValueNode = document.createTextNode(`${data[`get_data`][`passref`]}`);
    var errorTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Errors: `);
    var errorValueNode = document.createTextNode(`${data[`get_data`][`error`]}`);
    var resultTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Result: `);
    var resultValueNode = document.createTextNode(`${data[`get_data`][`result`]}`);
    var timingTextNode = document.createTextNode(`Station ${data[`get_data`][`station_number`]} Time Stamps: `);
    var timingValueNode = document.createTextNode(`${data[`get_data`][`timing`]}`);
    passrefNode.appendChild(passrefTextNode);
    passrefValueNode.style.display = 'inline-block';
    passrefNode.appendChild(passrefValueNode);
    errorNode.appendChild(errorTextNode);
    errorNode.appendChild(errorValueNode);
    errorValueNode.style.display = 'inline-block';
    resultNode.appendChild(resultTextNode);
    resultNode.appendChild(resultValueNode);
    resultValueNode.style.display = 'inline-block';
    timingNode.appendChild(timingTextNode);
    timingNode.appendChild(timingValueNode);
    timingValueNode.style.display = 'inline-block';
    let viewPortnode = document.querySelector(`#station_${data[`get_data`][`station_number`]}_viewPort`);
    viewPortnode.appendChild(passrefNode);
    viewPortnode.appendChild(errorNode);
    viewPortnode.appendChild(resultNode);
    viewPortnode.appendChild(timingNode);
  };

 }
);