import Image from "next/image";

type Player = {
  username: string;
  avatar: string;
  discord_id: string;
  isAdmin: boolean;
};

type WaitingRoomProps = {
  players: Player[];
};

export default function WaitingRoom({ players }: WaitingRoomProps) {
  return (
    <>
      <h1>Waiting Room</h1>
      <ul>
        {players.map((p) => (
          <div
            key={p.discord_id}
            className="p-4 border rounded-md shadow-md bg-white max-w-sm"
          >
            <div className="flex items-center gap-4">
              <Image
                src={p.avatar}
                alt={`${p.username}'s avatar`}
                width={48}
                height={48}
                className="rounded-full"
              />
              <div>
                <p className="font-semibold text-lg">{p.username}</p>
              </div>
              {p.isAdmin && (
                <div>
                  <p>Admin</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </ul>
      <div>
        <p>Nombre de joueurs : {players.length}</p>
      </div>
    </>
  );
}
