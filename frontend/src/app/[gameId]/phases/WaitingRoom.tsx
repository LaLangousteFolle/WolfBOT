"use client";
import PlayerCard from "../../components/PlayerCard";

export default function WaitingRoom({ players }) {
  return (
    <div className="p-4">
      <h2 className="text-xl mb-4">Salle d’attente</h2>
      <div className="grid grid-cols-2 gap-4">
        {players.map((p) => (
          <PlayerCard key={p.discord_id} player={p} />
        ))}
      </div>
      <p className="mt-6 text-gray-500">En attente du lancement de la partie…</p>
    </div>
  );
}
