import React from "react";
import "./Station1Button.css";

const Button1 = (props) => {
  return (
    <React.Fragment>
      <input 
        className={`${props.className} Station1Button`}
        id="station1"
        onChange={props.onClick}
      />
      <label htmlFor="station1" className={`${props.className} Station1Button`}> 
          Station 1
      </label>
    </React.Fragment>
  );
};

export default Button1;