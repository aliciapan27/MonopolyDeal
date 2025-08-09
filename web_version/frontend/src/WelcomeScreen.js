import React, { useState } from "react";
import monopolyLogo from "./assets/welcome_screen/monopoly-logo.png";
import deal from "./assets/welcome_screen/DEAL.png";
import "./WelcomeScreen.css";

export default function WelcomeScreen({ onStart }) {
  const [username, setUsername] = useState("");

  const handleStart = () => {
    if (username.trim()) {
      onStart(username);
    } else {
      alert("Please enter a username!");
    }
  };

  return (
    <div className="welcome-container">
      <img src={monopolyLogo} alt="Monopoly Logo" className="logo" />
      <img src={deal} alt="deal" className="deal" />

      <input
        type="text"
        placeholder="Enter your name"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="username-input"
      />

      <button className="start-button" onClick={handleStart}>
        Start Game
      </button>
    </div>
  );
}
