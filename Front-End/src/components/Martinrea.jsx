import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";

class Martinrea extends Component {
  state = {
    count: 0,
    imgLogo: "https://camsc.ca/wp-content/uploads/2021/06/Martinrea-logo.png",
    imgPicture:
      "C:/Users/henrique.engelke/Desktop/Martinrea/Object-Detection/Image_Processing/photosInput/20230124110825.jpeg", // Put camera pic here

    goodOrNot: 1, //This decides if position is good or bad
  };
  add = () => {
    this.setState({ count: this.state.count + 1 });
  };
  goodOrBad = () => {
    if (this.state.goodOrNot === 1)
      return <p className=".text-success">GOOD</p>;
    return <p className=".text-danger">FAILURE</p>;
  };

  render() {
    return (
      <div class="bg-danger position-relative">
        <div>
          <img src={this.state.imgLogo} alt="image" height="100" width="100" />
        </div>
        <div>
          <img
            src={this.state.imgPicture}
            alt="image-main"
            height="576"
            width="720"
          />

          <div className="position-absolute top-50 start-50">
            {this.goodOrBad()}
            <button onClick={this.add} className="btn btn-secondary brn-sm">
              Calibration
            </button>
          </div>
        </div>
        <div class="text-dark position-absolute top-0 start-50">
          <h1>BT1XX Testing</h1>
        </div>
      </div>
    );
  }
}

export default Martinrea;
