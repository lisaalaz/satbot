import React from "react";
import Options from "../Options/Options";

const FeedbackOptions = (props) => {
  const options = [
    {
      name: "Better",
      handler: props.actionProvider.handleButtons,
      id: 5,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Feedback",
    },
    {
      name: "Worse",
      handler: props.actionProvider.handleButtons,
      id: 6,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Feedback",
    },
    {
      name: "No Change",
      handler: props.actionProvider.handleButtons,
      id: 7,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Feedback",
    },
  ];

  return <Options options={options} />;
};
export default FeedbackOptions;
