// Експеримент 6: maxPayload. Що буде, якщо клієнт шле більше, ніж дозволено.
// Запуск: node 06-ws-maxpayload.js
//
// Спитай: яка подія спрацює на сервері, а яка на клієнті?
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 0, maxPayload: 1024 }); // ліміт 1 KB
await new Promise((resolve) => wss.on('listening', resolve));
const { port } = wss.address();

wss.on('connection', (socket) => {
  socket.on('message', (data) => console.log('[сервер] message, байтів:', data.length));
  socket.on('error', (err) => console.log('[сервер] error:', err.code, '-', err.message));
  socket.on('close', (code) => console.log('[сервер] close, код:', code));
});

const client = new WebSocket(`ws://localhost:${port}`);
client.on('open', () => {
  console.log('[клієнт] шлю 500 байтів (влізе)');
  client.send('a'.repeat(500));
  setTimeout(() => {
    console.log('[клієнт] шлю 2 KB (не влізе)');
    client.send('a'.repeat(2048));
  }, 200);
});
client.on('error', (err) => console.log('[клієнт] error:', err.message));
client.on('close', (code) => {
  console.log('[клієнт] close, код:', code, '(1009 = повідомлення завелике)');
  wss.close();
});
