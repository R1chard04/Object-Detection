import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import STANDARD from "../STANDARD.jpg";
import "../components-main/style.css";

class S1 extends Component {
  state = {
    count: 0,
    imgLogo: "https://camsc.ca/wp-content/uploads/2021/06/Martinrea-logo.png",
    imgPicture: "STANDARD", // Put camera pic here

    goodOrNot: 1, //This decides if position is good or bad (1 is pass)
  };

  goodOrBad = () => {
    if (this.state.goodOrNot === 1)
      return (
        <h1 class="goodOrBad" id="good">
          PASSAAA
        </h1>
      );
    return (
      <h1 class="goodOrBad" id="bad">
        FAILAAA
      </h1>
    );
  };

  render() {
    return (
      <div class="page">
        <div class="header">
          <img class="logo" src={this.state.imgLogo} alt="image" />
          <h1 class="text" id="title">
            BT1XX Testing
          </h1>
        </div>
        <h1 class="text" id="result">
          RESULT:
        </h1>
        <img class="main" src={STANDARD} alt="image-main" />
        <div>{this.goodOrBad()}</div>
        <div class="calibration">
          <button onClick={this.add} className="btn btn-secondary brn-sm">
            Calibration
          </button>
        </div>
      </div>
    );
  }
}

export default S1;
