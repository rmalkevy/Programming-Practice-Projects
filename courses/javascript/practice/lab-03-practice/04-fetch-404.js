// Експеримент 4 (§4): fetch і 404. Мережева помилка = reject, 404 = fulfill.
// Запуск: node 04-fetch-404.js
// Сервер піднімається сам (mock-server.js), інтернет не потрібен.
import { startServer, stopServer } from './mock-server.js';

const server = await startServer();
const base = server.base;

// A: 404 це fulfill. Очікування: ok false, status 404.
console.log('--- A: 404');
const r404 = await fetch(`${base}/status/404`);
console.log('проміс виконався. ok:', r404.ok, 'status:', r404.status);

// B: немає хоста. Тут уже reject. Очікування: TypeError.
console.log('--- B: хоста не існує');
try {
  await fetch('https://no-such-host.invalid/');
} catch (e) {
  console.log('reject:', e.name, '-', e.cause?.code ?? e.message);
}

// C: проміс fetch = прийшли заголовки; тіло окремим await.
console.log('--- C: заголовки, потім тіло');
const r = await fetch(`${base}/json`);
console.log('headers', r.status, r.ok);
const data = await r.json();
console.log('body', Object.keys(data));

// D: як це робить fetchJson з лаби: перетворює !ok на помилку.
console.log('--- D: fetchJson');
async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
try {
  await fetchJson(`${base}/status/404`);
} catch (e) {
  console.log('fetchJson кинув:', e.message);
}

await stopServer(server);
