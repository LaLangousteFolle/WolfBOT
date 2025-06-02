export default function WaitingRoom({ players }) {
  return (
    <>
      <h1>Waiting Room</h1>
      <ul>
        {players.map((p) => (
          <li key={p.discord_id}>{p.username}</li>
        ))}
      </ul>
    </>
  );
}
