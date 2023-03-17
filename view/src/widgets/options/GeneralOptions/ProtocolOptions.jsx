import React from "react";
import Options from "../Options/Options";
// import { cloneDeep } from "lodash";

class ProtocolOptions extends React.Component {
  shouldComponentUpdate = () => false

  constructor(props) {
    super(props);
    let protocols = props.protocols;
    this.options = [];
    for (let i = 0; i < protocols.length; i++) {
      this.options.push({
        name: protocols[i],
        handler: props.actionProvider.handleButtons,
        id: 16 + i,
        userID: props.userState,
        sessionID: props.sessionID,
        userInputType: "Protocol",
      });
    }

  }


  render() {
    return <Options options={this.options} />;

  }


};


export default ProtocolOptions;
