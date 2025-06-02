"use client";
export default function PlayerCard({ player }) {
  return (
    <div className="flex items-center gap-3 p-3 bg-white rounded-xl shadow">
      <img
        src={player.avatar}
        alt={player.username}
        className="w-12 h-12 rounded-full"
      />
      <span className="text-lg font-medium text-gray-500">{player.username}</span>
      <span className="text-lg font-medium text-gray-500">{player.discord_id}</span>
    </div>
  );
}
