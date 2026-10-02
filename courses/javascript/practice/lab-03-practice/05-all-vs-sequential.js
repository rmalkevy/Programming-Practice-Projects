// Експеримент 5 (§5): послідовно проти Promise.all, і що робить "програвший".
// Запуск: node 05-all-vs-sequential.js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const since = (t0) => Math.round(performance.now() - t0) + ' мс';

// A: час. Очікування: seq ~2000 мс, all ~1000 мс.
console.log('--- A: час');
let t0 = performance.now();
await wait(1000);
await wait(1000);
console.log('seq:', since(t0));

t0 = performance.now();
await Promise.all([wait(1000), wait(1000)]);
console.log('all:', since(t0));

// B: all падає на першому reject, а сусіди добігають.
// Очікування: одразу "all fast", і через ~300 мс "slow still ran".
console.log('--- B: сусіди не зупиняються');
const slow = new Promise((resolve) =>
  setTimeout(() => {
    console.log('slow still ran');
    resolve('s');
  }, 300),
);
try {
  await Promise.all([slow, Promise.reject(new Error('fast'))]);
} catch (e) {
  console.log('all', e.message);
}
await wait(400);

// C: allSettled, race, any.
console.log('--- C: allSettled / race / any');
const results = await Promise.allSettled([wait(10).then(() => 'ok'), Promise.reject(new Error('no'))]);
console.log('allSettled:', results);
console.log('race:', await Promise.race([wait(200).then(() => 'повільний'), wait(50).then(() => 'швидкий')]));
console.log('any:', await Promise.any([Promise.reject(new Error('x')), wait(20).then(() => 'перший успіх')]));
try {
  await Promise.any([Promise.reject(new Error('x')), Promise.reject(new Error('y'))]);
} catch (e) {
  console.log('any, усі впали:', e.name);
}

// D: прогрес-бар. Лічильник рахуємо самі, до all.
console.log('--- D: прогрес');
const urls = ['a.png', 'b.png', 'c.png'];
let done = 0;
const loads = urls.map((url, i) =>
  wait(100 * (i + 1)).then(() => {
    done += 1;
    console.log(`${done}/${urls.length}  ${url}`);
    return url;
  }),
);
await Promise.all(loads);
