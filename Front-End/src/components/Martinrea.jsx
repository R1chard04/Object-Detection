import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import STANDARD from "../STANDARD.jpg";

class Martinrea extends Component {
  state = {
    count: 0,
    imgLogo: "https://camsc.ca/wp-content/uploads/2021/06/Martinrea-logo.png",
    imgPicture: "STANDARD", // Put camera pic here

    goodOrNot: 1, //This decides if position is good or bad
  };
  add = () => {
    this.setState({ count: this.state.count + 1 });
  };
  goodOrBad = () => {
    if (this.state.goodOrNot === 1)
      return <h1 className="text-success">GOOD</h1>;
    return <h1 className="text-danger">FAILURE</h1>;
  };

  render() {
    return (
      <div class="bg-primary position-relative">
        <div>
          <img src={this.state.imgLogo} alt="image" height="100" width="100" />
        </div>
        <div>
          <img src={STANDARD} alt="image-main" height="576" width="720" />

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
