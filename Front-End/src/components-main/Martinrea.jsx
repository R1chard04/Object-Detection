import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import STANDARD from "../STANDARD.jpg";
import "./style.css";
import CAM from "../camPic.jpg";

class Martinrea extends Component {
  state = {
    count: 0,
    station: 0,
    imgLogo: "https://camsc.ca/wp-content/uploads/2021/06/Martinrea-logo.png",

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
  };
  changeStation = (sta) => {
    this.setState({ station: sta });
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
      <div class="page">
        <div>
          <p class="credits">Student Co-Op Program Winter 2023</p>
          <p class="names">
            Made by Eren Yilmaz, Henrique Rodrigues, Jamie Yen, Kent Tren & Leo
            You
          </p>
        </div>
        <div>
          <button onClick={() => this.update(1)} class="s1">
            Station 1
          </button>
          <button onClick={() => this.update(2)} class="s2">
            Station 2
          </button>
          <button onClick={() => this.update(3)} class="s3">
            Station 3
          </button>
          <button onClick={() => this.update(4)} class="s4">
            Station 4
          </button>
          <button onClick={() => this.update(5)} class="s5">
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
          <img class="main" src={CAM} alt="main" /> // Put camera pic here
        ) : this.state.station === 1 ? (
          <img class="main" src={CAM} alt="main" /> // put pic s1 here
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
            {/*RUN MASK PROGRAM/} */}
            Calibration
          </button>
        </div>
      </div>
    );
  }
}

export default Martinrea;
