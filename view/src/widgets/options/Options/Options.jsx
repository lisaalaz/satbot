import React from "react";

import styles from "./Options.module.css";

const Options = ({ options }) => {
  const runHandler = (handler, userID, sessionID, userInput, userInputType) => {
    handler(userID, sessionID, userInput, userInputType);
  };
  const markup = options.map((option) => (
    <button
      key={option.id}
      className={styles.option}
      onClick={() =>
        runHandler(
          option.handler,
          option.userID,
          option.sessionID,
          option.name,
          option.userInputType
        )
      }
    >
      {option.name}
    </button>
  ));

  return <div className={styles.options}>{markup}</div>;
};

export default Options;
