// Експеримент 6 (§6): скасування через AbortController.
// Запуск: node 06-abort.js
import { startServer, stopServer } from './mock-server.js';

const server = await startServer();
const base = server.base;

// A: abort() одразу. Очікування: AbortError.
console.log('--- A: abort()');
const c = new AbortController();
const req = fetch(`${base}/delay/5`, { signal: c.signal }).catch((e) => console.log('ім\'я помилки:', e.name));
c.abort();
await req;

// B: таймаут. Питання: яке тут ім'я? Підказка: НЕ те саме, що в A.
console.log('--- B: AbortSignal.timeout(1000)');
const t0 = performance.now();
try {
  await fetch(`${base}/delay/5`, { signal: AbortSignal.timeout(1000) });
} catch (e) {
  console.log('ім\'я помилки:', e.name, 'через', Math.round(performance.now() - t0), 'мс');
}

// C: race з таймаутом НЕ скасовує запит, він висить далі.
console.log('--- C: race з таймаутом (запит не скасовується)');
const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('таймаут')), 500));
try {
  await Promise.race([fetch(`${base}/delay/2`), timeout]);
} catch (e) {
  console.log('race:', e.message, '(але fetch ще йде, сервер його не кинув)');
}

await stopServer(server);
