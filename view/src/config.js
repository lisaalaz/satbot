// Config starter code
import React from "react";
import { createChatBotMessage } from "react-chatbot-kit";

import YesNoOptions from "./widgets/options/GeneralOptions/YesNoOptions";
import ProtocolOptions from "./widgets/options/GeneralOptions/ProtocolOptions";
import ContinueOptions from "./widgets/options/GeneralOptions/ContinueOptions";
import FeedbackOptions from "./widgets/options/GeneralOptions/FeedbackOptions";
import EmotionOptions from "./widgets/options/GeneralOptions/EmotionOptions";
import EventOptions from "./widgets/options/GeneralOptions/EventOptions";
import YesNoProtocolOptions from "./widgets/options/GeneralOptions/YesNoProtocolsOptions";

// import Kai from "./Kai.png"

const botName = "SATbot";

// export const getPersona = () => {

//   return <img src={Kai} width="50" height="50" alt=""/>;

// };


const config = {
  botName: botName,
  initialMessages: [
    createChatBotMessage("Hi, I am SATbot, welcome to today's session.", {
      withAvatar: true,
      delay: 0,
    }),
    createChatBotMessage("Before we begin, I just need you to go through authentication.", {
      withAvatar: true,
      delay: 1500,
    }),
    createChatBotMessage("Please enter your username:", {
      withAvatar: true,
      delay: 3000,
    }),
  ],

  state: {
    userState: null,
    username: null,
    password: null,
    sessionID: null,
    protocols: [],
    askingForProtocol: false
  },

  customComponents: {
    header: () => <div style={{height: '15px', fontFamily: 'Trebuchet MS', fontSize: "1em", textAlign: "center", color: '#fff', paddingTop: '1em', paddingBottom: '1em'}}>S A T B O T</div>,
    // botAvatar: (props) => <div class="react-chatbot-kit-chat-bot-avatar-container" style={{fontFamily: 'Arial'}}>
    //   {getPersona()} </div>
    },

  widgets: [
    {
      widgetName: "YesNo",
      widgetFunc: (props) => <YesNoOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
    {
      widgetName: "Continue",
      widgetFunc: (props) => <ContinueOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
    {
      widgetName: "Emotion",
      widgetFunc: (props) => <EmotionOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
    {
      widgetName: "Feedback",
      widgetFunc: (props) => <FeedbackOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
    {
      widgetName: "Protocol",
      widgetFunc: (props) => <ProtocolOptions {...props} />,
      mapStateToProps: ["userState", "sessionID", "protocols", "askingForProtocol"],
    },
    {
      widgetName: "YesNoProtocols",
      widgetFunc: (props) => <YesNoProtocolOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
    {
      widgetName: "RecentDistant",
      widgetFunc: (props) => <EventOptions {...props} />,
      mapStateToProps: ["userState", "sessionID"],
    },
  ],
};

export default config;
