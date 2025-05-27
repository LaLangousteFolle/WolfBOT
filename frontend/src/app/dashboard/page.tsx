"use client";

import Image from "next/image";
import { useSearchParams } from "next/navigation";

export default function Dashboard() {
  const searchParams = useSearchParams();
  const username = searchParams.get("username");
  const id = searchParams.get("id");
  const avatar = searchParams.get("avatar");

  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-2xl font-bold mb-4">
        Bienvenue sur WolfBot, {username} !
      </h1>

      {avatar && (
        <Image
          src={avatar}
          alt={`Avatar de ${username}`}
          width={128}
          height={128}
          className="rounded-full shadow-lg"
        />
      )}

      <p className="mt-2 text-gray-500 text-sm">ID Discord : {id}</p>
    </div>
  );
}
