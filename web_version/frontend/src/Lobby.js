import React, { useState, useEffect, useRef } from "react";

function Lobby({ username }) {
  const [players, setPlayers] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    console.log("Lobby mounted - connecting WS");
    ws.current = new WebSocket(`ws://localhost:8000/ws/${username}`);

    ws.current.onopen = () => {
      console.log("Connected to server");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "player_list") {
        setPlayers(data.players);
      }
    };

    ws.current.onclose = () => {
      console.log("Disconnected");
    };

    return () => {
      console.log("Lobby mounted - connecting WS");
      ws.current.close();
    };
  }, [username]);

  return (
    <div>
      <h2>Welcome, {username}!</h2>
      <h3>Players in lobby:</h3>
      <ul>
        {players.map((player) => (
          <li key={player}>{player}</li>
        ))}
      </ul>
      <p>Waiting for more players to join...</p>
    </div>
  );
}

export default Lobby;
