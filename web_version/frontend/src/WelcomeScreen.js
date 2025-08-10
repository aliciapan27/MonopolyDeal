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

      <div className="form-container">
        <input
          type="text"
          placeholder="Enter your name"
          className="name-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button className="start-button" onClick={handleStart}>
          ✓ Join Game
        </button>
      </div>
    </div>
  );
}
