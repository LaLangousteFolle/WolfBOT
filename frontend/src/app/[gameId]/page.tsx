"use client";
import GameRoom from "./GameRoom";

export default function GamePage({ params, searchParams }) {
  const token = searchParams.token;
  const gameId = params.gameId;

  const payload = JSON.parse(atob(token.split('.')[1]));

  const player = {
    username: payload.username,
    avatar: payload.avatar,
    discord_id: payload.discord_id,
  };

  return <GameRoom gameId={gameId} player={player} token={token} />;
}