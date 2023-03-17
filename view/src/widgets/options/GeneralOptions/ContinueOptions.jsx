import React from "react";
import Options from "../Options/Options";

const ContinueOptions = (props) => {
  const options = [
    {
      name: "Continue",
      handler: props.actionProvider.handleButtons,
      id: 4,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Continue",
    },
  ];
  return <Options options={options} />;
};

export default ContinueOptions;
