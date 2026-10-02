// Експеримент 1 (§1): проміс виконується один раз, і .then завжди "пізніше".
// Запуск: node 01-once-and-later.js
//
// Спитай студентів ПЕРЕД запуском про кожну частину.

// Частина A: другий resolve ігнорується. Очікування: лише 1.
const p = new Promise((resolve) => {
  resolve(1);
  resolve(2);
});
p.then((v) => console.log('A:', v));

// Частина B: проміс УЖЕ готовий, але .then все одно не біжить зараз.
// Очікування: спочатку "after subscribe", потім "then ready".
Promise.resolve('ready').then((v) => console.log('B: then', v));
console.log('B: after subscribe');
