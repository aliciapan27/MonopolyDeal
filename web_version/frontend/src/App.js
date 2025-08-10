import React, { useState } from "react";
import WelcomeScreen from "./WelcomeScreen";

export default function App() {
  const [username, setUsername] = useState("");

  if (!username) {
    return <WelcomeScreen onStart={setUsername} />;
  }

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontSize: "2rem" }}>
      Hi {username} 👋
    </div>
  );
}
