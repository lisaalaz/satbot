import React from "react";
import Options from "../Options/Options";

const MoreInfoOptions = (props) => {
  const options = [
    {
      name: "More Information",
      handler: props.actionProvider.handleMoreInfo,
      id: 3,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "MoreInfo",
    },
  ];
  return <Options options={options} />;
};

export default MoreInfoOptions;
