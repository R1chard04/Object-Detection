import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import STANDARD from "../STANDARD.jpg";
import "./style.css";
import Button1 from "./Station1Button.jsx";

class Martinrea extends Component {
  handleWebsiteChange = async (event) => {};
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
          PASS
        </h1>
      );
    return (
      <h1 class="goodOrBad" id="bad">
        FAIL
      </h1>
    );
  };

  render() {
    return (
      <React.Fragment>
        <div class="page">
          <Button1 onClick={this.handleWebsiteChange} />
          <div class="header">
            <img class="logo" src={this.state.imgLogo} alt="Logo" />
            <h1 class="text" id="title">
              BT1XX Testing
            </h1>
          </div>
          <h1 class="text" id="result">
            RESULT:
          </h1>
          <img class="main" src={STANDARD} alt="main" />
          <div>{this.goodOrBad()}</div>
          <div class="calibration">
            <button onClick={this.add} className="btn btn-secondary brn-sm">
              Calibration
            </button>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Martinrea;
