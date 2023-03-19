import axios from 'axios';
// ActionProvider starter code
class ActionProvider {
  constructor(createChatBotMessage, setStateFunc, createClientMessage) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
    this.createClientMessage = createClientMessage;
  }


  // Asks for password after storing username
  askForPassword = (username) => {
    this.setState((state) => ({
      ...state,
      username: username,
    }));
    const messages = this.createChatBotMessage(
      "Please enter your password:",
      {
        withAvatar: true,
      }
    );

    this.addMessageToBotState(messages);
  }

  // Checking for ID with a request
  updateUserID = async (username, password) => {

    this.setState((state) => ({
      ...state,
      password: password,
    }));

    // URL to use for AWS (Axios requests)
    // const uri = `/api/login`

    // URL to use for local requests
    const uri = `http://localhost:5000/api/login`
    let user_info = {
      username: username,
      password: password
    };

    const response = await axios.post(uri, {
      user_info
    })

    // dataReceived format: {validID : bool, userID: string}
    let dataReceived = response.data
    if (!dataReceived.validID) {
      let message = this.createChatBotMessage(
        "The ID and password combination is not valid, sorry. What is your user ID?",
        {
          withAvatar: true,
        });
      this.addMessageToBotState(message);
      // let user_id_message = this.createChatBotMessage("What is your user ID?",
      //   { withAvatar: true,
      //     delay: 1500 }
      // );
      // this.addMessageToBotState(user_id_message)
      this.setState((state) => ({
        ...state,
        username: null,
        password: null
      }));

    } else {
      let model_prompt = dataReceived.model_prompt
      this.setState((state) => ({ ...state, userState: dataReceived.userID, inputType: dataReceived.choices, sessionID: dataReceived.sessionID }));
      let message = this.createChatBotMessage("The user ID and password combination is valid, thank you!", {
        withAvatar: true,
      });

      // Opening prompt -> open text
      this.addMessageToBotState(message);
      message = this.createChatBotMessage(model_prompt, {
        withAvatar: true,
        delay: 1500,
      });
      this.addMessageToBotState(message);
    }

  };

  // Send API request
  sendRequest = async (choice_info) => {
    // URL to use for AWS (Axios requests)
    // const uri = `/api/update_session`

    // URL to use for local requests
    const uri = `http://localhost:5000/api/update_session`;
    const response = await axios.post(uri, {
      choice_info
    })

    this.handleReceivedData(response.data);
  };

  handleReceivedData = (dataReceived) => {
    // dataReceived = {
    //   chatbot_response: "This is the chatbot message to display",
    //   user_options: options to map to expected buttons below
    // }

    const userOptions = dataReceived.user_options
    let optionsToShow = null;


    //  Required options: null or "YesNo" or "Continue" or "Feedback" or "Emotion"}
    if (userOptions.length === 1 && (userOptions[0] === "open_text" || userOptions[0] === "any")) {
      optionsToShow = null;
    } else if (userOptions.length === 1 && userOptions[0] === "continue") {
      optionsToShow = "Continue"
    } else if (userOptions.length === 2 && userOptions[0] === "yes" && userOptions[1] === "no") {
      optionsToShow = "YesNo"
    } else if (userOptions.length === 2 && userOptions[0] === "yes, i would like to try one of these protocols" && userOptions[1] === "no, i would like to try something else") {
      optionsToShow = "YesNoProtocols"
    } else if (userOptions.length === 2 && userOptions[0] === "recent" && userOptions[1] === "distant") {
      optionsToShow = "RecentDistant"
    } else if (userOptions.length === 3 && userOptions[0] === "positive" && userOptions[1] === "neutral" && userOptions[2] === "negative") {
      optionsToShow = "Emotion"
    } else if (userOptions.length === 3 && userOptions[0] === "better" && userOptions[1] === "worse" && userOptions[2] === "no change") {
      optionsToShow = "Feedback"
    } else {
      // Protocol case
      optionsToShow = "Protocol"
      this.setState((state) => ({
        ...state,
        protocols: userOptions,
        askingForProtocol: true
      }));
    }
    this.setState((state) => ({
      ...state,
      currentOptionToShow: optionsToShow,
    }));

    // Responses are either strings or list of strings

    if (typeof dataReceived.chatbot_response === "string") {
      const messages = this.createChatBotMessage(dataReceived.chatbot_response, {
        withAvatar: true,
        widget: optionsToShow,
      });
      this.addMessageToBotState(messages);
    } else {
      for (let i = 0; i < dataReceived.chatbot_response.length; i++) {
        let widget = null;
        // Shows options after last message
        if (i === dataReceived.chatbot_response.length - 1) {
          widget = optionsToShow;
        }
        const message_to_add = this.createChatBotMessage(dataReceived.chatbot_response[i], {
          withAvatar: true,
          widget: widget,
          delay: (i)*1500,
        });
        this.addMessageToBotState(message_to_add);

      }

    }
  };

  handleButtonsEmotion = (userID, sessionID, userInput, userInputType) => {
    let inputToSend = userInput;
    let message = this.createClientMessage(userInput);
    this.addMessageToBotState(message);


    // Ignores input type above and manually defines; other cases will need an if check for this
    let input_type = ["positive", "neutral", "negative"]
    const dataToSend = {
      user_id: userID,
      session_id: sessionID,
      user_choice: inputToSend,
      input_type: input_type,
    };
    this.sendRequest(dataToSend);
  }

  handleButtons = (userID, sessionID, userInput, userInputType) => {
    let message = this.createClientMessage(userInput);
    this.addMessageToBotState(message);

    const dataToSend = {
      user_id: userID,
      session_id: sessionID,
      user_choice: userInput,
      input_type: userInputType,
    };
    return this.sendRequest(dataToSend);
  };

  askForProtocol = () => {
    let message = "Please type a protocol number (1-20), using the workshops to help you."
    this.addMessageToBotState(message);
    this.setState((state) => ({
      ...state,
      askingForProtocol: true,
    }))
  }

  stopAskingForProtocol = () => {
    this.setState((state) => ({
      ...state,
      askingForProtocol: false,
    }))
  }


  // Copies last message from model
  copyLastMessage = () => {
    this.setState((state) => ({
      ...state,
      messages: [...state.messages, state.messages[state.messages.length - 2]],
    }))
  }


  // Add message to state
  addMessageToBotState = (message) => {
    this.setState((state) => ({
      ...state,
      messages: [...state.messages, message],
    }));
  };
}

export default ActionProvider;
