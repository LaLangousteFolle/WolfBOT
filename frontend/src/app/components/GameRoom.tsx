"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Account from "./Account";
import AdminRoom from "./AdminRoom";
import RolesRoom from "./RolesRoom";
import WaitingRoom from "./WaitingRoom";

export default function GameRoom() {
  const searchParams = useSearchParams();

  type Player = {
    username: string;
    avatar: string;
    discord_id: string;
    isAdmin: boolean;
  };

  const [players, setPlayers] = useState<Player[]>([]);
  const [player, setPlayer] = useState<Player | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const paramToken = searchParams.get("token");
    if (!paramToken) return;

    setToken(paramToken);
    const decoded = JSON.parse(atob(paramToken.split(".")[1]));

    const newPlayer = {
      username: decoded.username,
      avatar: decoded.avatar,
      discord_id: decoded.discord_id,
      isAdmin: decoded.isAdmin,
    };

    setPlayer(newPlayer);
    setPlayers([newPlayer]);

    const socket = new WebSocket(
      `${process.env.NEXT_PUBLIC_WS_URL}?token=${paramToken}`
    );

    socket.onopen = () => console.log("Connecté WS");
    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "update_players") {
        setPlayers(msg.players);
      }
    };

    return () => socket.close();
  }, [searchParams]);

  if (!token || !player) return <p>Chargement...</p>;

  return (
    <>
      <Account player={player} />
      {player.isAdmin && <AdminRoom nbJoueurs={players.length} />}
      <RolesRoom />
      <WaitingRoom players={players} />
    </>
  );
}
