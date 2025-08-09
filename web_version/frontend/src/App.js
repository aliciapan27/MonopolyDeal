import React, { useState } from "react";
import WelcomeScreen from "./WelcomeScreen";

export default function App() {
  const [started, setStarted] = useState(false);

  const handleStartClick = () => {
    setStarted(true);
  };

  return (
    <div>
      {!started ? (
        <WelcomeScreen onStart={handleStartClick} />
      ) : (
        <div style={{ padding: "2rem", textAlign: "center" }}>
          <h1>Game Screen</h1>
          <p>This is where the game will go!</p>
        </div>
      )}
    </div>
  );
}
