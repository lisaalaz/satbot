import React from "react";
import Options from "../Options/Options";

const EmotionOptions = (props) => {
  const options = [
    {
      name: "Happy",
      handler: props.actionProvider.handleButtonsEmotion,
      id: 8,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Emotion",
    },
    {
      name: "Sad",
      handler: props.actionProvider.handleButtonsEmotion,
      id: 10,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Emotion",
    },
    {
      name: "Angry",
      handler: props.actionProvider.handleButtonsEmotion,
      id: 11,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Emotion",
    },
    {
      name: "Anxious",
      handler: props.actionProvider.handleButtonsEmotion,
      id: 12,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Emotion",
    },
    {
      name: "Scared",
      handler: props.actionProvider.handleButtonsEmotion,
      id: 13,
      userID: props.userState,
      sessionID: props.sessionID,
      userInputType: "Emotion",
    },
  ];

  return <Options options={options} />;
};
export default EmotionOptions;
