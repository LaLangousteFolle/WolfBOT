"use client";

import { useSearchParams } from "next/navigation";

export default function Dashboard() {
  const searchParams = useSearchParams();
  const username = searchParams.get("username");
  const id = searchParams.get("id");

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Bienvenue, {username} !</h1>
      <p>ID utilisateur : {id}</p>
    </div>
  );
}
