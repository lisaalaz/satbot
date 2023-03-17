import React from "react";
import { Chatbot } from "react-chatbot-kit";
import "./App.css";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import config from "./config";

const App = () => {

  return (
    <div className="App">
      <div className="app-chatbot-container">
        <Chatbot
          config={config}
          messageParser={MessageParser}
          actionProvider={ActionProvider}
        />
      </div>
    </div>
    
  );
}

export default App;
