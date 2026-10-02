// Експеримент 5: WebSocket-сервер і клієнт в одному скрипті, echo.
// Запуск: node 05-ws-echo.js
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 0 }); // 0 = будь-який вільний порт
await new Promise((resolve) => wss.on('listening', resolve));
const { port } = wss.address();
console.log('сервер слухає порт', port);

wss.on('connection', (socket) => {
  socket.on('error', (err) => console.log('[сервер] error:', err.message)); // завжди!
  socket.on('message', (data) => {
    console.log('[сервер] отримав:', data.toString());
    socket.send('echo: ' + data.toString());
  });
});

const client = new WebSocket(`ws://localhost:${port}`);
client.on('open', () => {
  console.log('[клієнт] з\'єднано, шлю "привіт"');
  client.send('привіт');
});
client.on('message', (data) => {
  console.log('[клієнт] отримав:', data.toString());
  client.close();
});
client.on('close', () => {
  console.log('[клієнт] закрито');
  wss.close();
});
