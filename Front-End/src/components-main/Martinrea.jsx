import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import STANDARD from "../STANDARD.jpg";
import "./style.css";

class Martinrea extends Component {
  handleWebsiteChange = async (event) => {};
  state = {
    count: 0,
    station: 0,
    imgLogo: "https://camsc.ca/wp-content/uploads/2021/06/Martinrea-logo.png",
    imgPicture1: "STANDARD", // Put camera pic here
    img1: "http://living-wild.net/wp-content/uploads/2016/09/16x9-c-1-768x432.jpg",
    img2: "http://www.jasontheaker.com/images/16x9/Ilkley-Heather.jpg",
    img3: "http://living-wild.net/wp-content/uploads/2016/09/Top-50-21-1.jpg",
    img4: "http://living-wild.net/wp-content/uploads/2016/09/Banado-animoto-26-1-768x432.jpg",
    img5: "http://living-wild.net/wp-content/uploads/2016/09/Snowy-Plover-16x9-1-768x432.jpg",

    goodOrNot: 1, //This decides if position is good or bad (1 is pass)
  };

  //Use if to check images

  update = (staa) => {
    this.changeStation(staa);
    this.updateImg(staa);
  };
  changeStation = (sta) => {
    this.setState({ station: sta });
  };

  updateImg = (sta) => {};

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
          <div class="stations">
            <button
              onClick={() => this.update(1)}
              className="btn btn-secondary brn-sm"
            >
              Station 1
            </button>
            <button
              onClick={() => this.update(2)}
              className="btn btn-secondary brn-sm"
            >
              Station 2
            </button>
            <button
              onClick={() => this.update(3)}
              className="btn btn-secondary brn-sm"
            >
              Station 3
            </button>
            <button
              onClick={() => this.update(4)}
              className="btn btn-secondary brn-sm"
            >
              Station 4
            </button>
            <button
              onClick={() => this.update(5)}
              className="btn btn-secondary brn-sm"
            >
              Station 5
            </button>
          </div>

          <div class="header">
            <img class="logo" src={this.state.imgLogo} alt="Logo" />
            <h1 class="text" id="title">
              BT1XX Testing
            </h1>
          </div>
          <h1 class="text" id="result">
            RESULT:
          </h1>
          <h1 class="stati">
            Station:
            {this.state.station}
          </h1>
          {this.state.station === 0 ? (
            <img class="main" src={STANDARD} alt="main" />
          ) : this.state.station === 1 ? (
            <img class="main" src={this.state.img1} alt="main" />
          ) : this.state.station === 2 ? (
            <img class="main" src={this.state.img2} alt="main" />
          ) : this.state.station === 3 ? (
            <img class="main" src={this.state.img3} alt="main" />
          ) : this.state.station === 4 ? (
            <img class="main" src={this.state.img4} alt="main" />
          ) : (
            <img class="main" src={this.state.img5} alt="main" />
          )}

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
