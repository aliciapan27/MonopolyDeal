import React, { useState } from "react";
import WelcomeScreen from "./WelcomeScreen";
import Lobby from "./Lobby";

export default function App() {
  const [username, setUsername] = useState("");
  const [inLobby, setInLobby] = useState(false);

  if (!username) {
    return <WelcomeScreen onStart={setUsername} />;
  }

  return <Lobby username={username} />;
}
