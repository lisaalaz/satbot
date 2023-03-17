import React from "react";
import Options from "../Options/Options";

const EventOptions = (props) => {
  const options = [
    {
      name: "Recent",
      handler: props.actionProvider.handleButtons,
      id: 1,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "RecentDistant",
    },
    {
      name: "Distant",
      handler: props.actionProvider.handleButtons,
      id: 2,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "RecentDistant",
    },
  ];

  return <Options options={options} />;
};
export default EventOptions;
