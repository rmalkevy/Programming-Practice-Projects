// Локальний замінник httpbin.org, щоб експерименти працювали без інтернету.
//   GET /status/404   -> відповідь зі статусом 404 (будь-який код)
//   GET /json         -> маленький JSON
//   GET /delay/3      -> відповідь через 3 секунди
//
// Окремо (для браузера): node mock-server.js   -> http://localhost:3003
// З інших скриптів: const server = await startServer(); ... await stopServer(server)
import http from 'node:http';
import { pathToFileURL } from 'node:url';

export const PORT = 3003;

export function startServer(port = 0) {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    const [, kind, arg] = url.pathname.split('/');
    // CORS, щоб браузерна сторінка (file:// або інший порт) могла робити fetch
    res.setHeader('Access-Control-Allow-Origin', '*');

    if (kind === 'status') {
      res.writeHead(Number(arg) || 200, { 'Content-Type': 'text/plain' });
      res.end(`status ${arg}`);
    } else if (kind === 'json') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ship: 'ship.png', sound: 'boom.ogg', arena: { w: 800, h: 600 } }));
    } else if (kind === 'delay') {
      const timer = setTimeout(() => {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end(`after ${arg}s`);
      }, Number(arg) * 1000);
      res.on('close', () => clearTimeout(timer)); // клієнт пішов (abort), не чекаємо
    } else {
      res.writeHead(404);
      res.end();
    }
  });
  return new Promise((resolve) => {
    server.listen(port, () => {
      server.base = `http://localhost:${server.address().port}`;
      resolve(server);
    });
  });
}

export function stopServer(server) {
  server.closeAllConnections();
  return new Promise((resolve) => server.close(resolve));
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = await startServer(PORT);
  console.log(`mock-сервер: ${server.base}  (/status/404, /json, /delay/3)`);
}
