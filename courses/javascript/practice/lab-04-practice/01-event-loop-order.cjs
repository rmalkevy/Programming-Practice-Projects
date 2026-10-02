// Експеримент 1 (CommonJS): порядок черг у Node.
// Запуск: node 01-event-loop-order.cjs   (повтори 5 разів)
//
// Спитай студентів ПЕРЕД запуском: у якому порядку з'являться n, p, t, i?
//
// Очікування: n (nextTick) завжди перед p (проміс).
// t (setTimeout 0) проти i (setImmediate) з головного модуля може "плавати".

setTimeout(() => console.log('t  setTimeout 0'), 0);
setImmediate(() => console.log('i  setImmediate'));
process.nextTick(() => console.log('n  nextTick'));
Promise.resolve().then(() => console.log('p  promise'));

// Частина 2: те саме, але всередині I/O-колбека.
// Тут порядок вже СТАБІЛЬНИЙ: setImmediate завжди раніше за setTimeout 0.
const fs = require('node:fs');
fs.readFile(__filename, () => {
  setTimeout(() => console.log('   [I/O] t  setTimeout 0'), 0);
  setImmediate(() => console.log('   [I/O] i  setImmediate'));
});
