"use client";

import Image from "next/image";

type Player = {
  username: string;
  avatar: string;
  discord_id: string;
};

type AccountProps = {
  player: Player;
};

export default function Account({ player }: AccountProps) {
  return (
    <div className="p-4 border rounded-md shadow-md bg-white max-w-sm">
      <div className="flex items-center gap-4">
        <Image
          src={player.avatar}
          alt={`${player.username}'s avatar`}
          className="w-12 h-12 rounded-full"
        />
        <div>
          <p className="font-semibold text-lg">{player.username}</p>
        </div>
      </div>
    </div>
  );
}
