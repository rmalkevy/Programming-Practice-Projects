// Експеримент 3 (§3): ланцюжок .then. Поверни, не вкладай.
// Запуск: node 03-chain.js
const pause = () => new Promise((resolve) => setTimeout(resolve, 50));

// Частина A: забули return. Очікування: "forgot undefined", потім "returned 2".
console.log('--- A');
Promise.resolve(1)
  .then((n) => {
    Promise.resolve(n + 1); // немає return!
  })
  .then((n) => console.log('forgot', n));

Promise.resolve(1)
  .then((n) => Promise.resolve(n + 1))
  .then((n) => console.log('returned', n));
await pause();

// Частина B: throw -> reject, після catch ланцюг знову fulfilled.
// Очікування: "a 1", "c boom", "d". Рядка "b" немає.
console.log('--- B');
Promise.resolve(1)
  .then((n) => {
    console.log('a', n);
    throw new Error('boom');
  })
  .then((n) => console.log('b', n))
  .catch((e) => console.log('c', e.message))
  .then(() => console.log('d'));
await pause();

// Частина C: async-функція завжди повертає проміс.
console.log('--- C');
async function ok() { return 5; }
async function bad() { throw new Error('bad'); }
console.log('ok()  ->', ok());   // Promise { 5 }
console.log('bad() ->', bad().catch(() => {})); // Promise { <pending> } (поки не зловили)
try {
  await bad();
} catch (e) {
  console.log('try/catch зловив:', e.message);
}
