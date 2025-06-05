import React, { Suspense } from "react";
import GameRoom from "./components/GameRoom";

export default function Page() {
  return (
    <Suspense fallback={<p>Chargement...</p>}>
      <GameRoom />
    </Suspense>
  );
}
