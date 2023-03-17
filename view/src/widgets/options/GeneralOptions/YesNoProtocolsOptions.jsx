import React from "react";
import Options from "../Options/Options";

const YesNoProtocolOptions = (props) => {
  const options = [
    {
      name: "Yes, I would like to try one of these protocols",
      handler: props.actionProvider.handleButtons,
      id: 14,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "YesNoProtocols",
    },
    {
      name: "No, I would like to try something else",
      handler: props.actionProvider.handleButtons,
      id: 15,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "YesNoProtocols",
    },
  ];

  return <Options options={options} />;
};
export default YesNoProtocolOptions;
