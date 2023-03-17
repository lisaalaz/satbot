import React from "react";
import Options from "../Options/Options";

const YesNoOptions = (props) => {
  const options = [
    {
      name: "Yes",
      handler: props.actionProvider.handleButtons,
      id: 1,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "YesNo",
    },
    {
      name: "No",
      handler: props.actionProvider.handleButtons,
      id: 2,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "YesNo",
    },
  ];

  return <Options options={options} />;
};
export default YesNoOptions;
