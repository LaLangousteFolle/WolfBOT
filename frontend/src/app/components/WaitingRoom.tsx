import { Avatar, AvatarImage } from "@/components/ui/avatar";

export default function WaitingRoom({ players }) {
  console.log(players.length);
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
              <img
                src={p.avatar}
                alt={`${p.username}'s avatar`}
                className="w-12 h-12 rounded-full"
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
