"use client";
import { useEffect, useState } from "react";
import WaitingRoom from "./phases/WaitingRoom";

export default function GameRoom({ gameId, player, token }) {
  const [phase, setPhase] = useState("waiting");
  const [players, setPlayers] = useState([player]);

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8000/ws/game/${gameId}?token=${token}`);

    socket.onopen = () => console.log("Connecté WS");
    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "update_players") {
        setPlayers(msg.players);
      }
    };

    return () => socket.close();
  }, []);

  return (
    <div>
      <h1 className="text-2xl text-center mt-4">Partie #{gameId}</h1>
      {phase === "waiting" && <WaitingRoom players={players} />}
    </div>
  );
}
