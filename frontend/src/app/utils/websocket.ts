let socket: WebSocket;

export const connectToGame = ({ gameId, token, onMessage }) => {
  socket = new WebSocket(`wss://ton-backend/ws/game/${gameId}?token=${token}`);

  socket.onopen = () => console.log("WS connected");
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };
};

export const sendMessage = (msg) => {
  socket?.send(JSON.stringify(msg));
};
