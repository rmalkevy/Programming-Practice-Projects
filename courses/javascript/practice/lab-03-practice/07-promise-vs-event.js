// Експеримент 7 (§7): проміс пам'ятає, подія ні.
// Запуск: node 07-promise-vs-event.js

// A: проміс. Очікування: і early, і late.
console.log('--- A: проміс');
const sprite = Promise.resolve('ship.png');
sprite.then((v) => console.log('early', v));
sprite.then((v) => console.log('late', v));
await sprite;

// B: подія. Очікування: після першого вибуху лише "heard 1".
// Підписник "too late" почує лише наступний вибух.
console.log('--- B: подія');
const bus = new EventTarget();
bus.addEventListener('exploded', (e) => console.log('heard', e.detail));
bus.dispatchEvent(new CustomEvent('exploded', { detail: 1 }));
bus.addEventListener('exploded', (e) => console.log('too late', e.detail));
console.log('перший вибух пропущено: "too late" мовчить. Другий вибух:');
bus.dispatchEvent(new CustomEvent('exploded', { detail: 2 })); // тепер чують обидва

// C: одну подію можна дочекатись як проміс.
console.log('--- C: once()');
function once(target, type) {
  return new Promise((resolve) => {
    target.addEventListener(type, resolve, { once: true });
  });
}
setTimeout(() => bus.dispatchEvent(new CustomEvent('loaded', { detail: 'готово' })), 100);
const e = await once(bus, 'loaded');
console.log('дочекались події:', e.detail);
