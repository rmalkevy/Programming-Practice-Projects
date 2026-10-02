// Експеримент 1b (ESM): ті самі чотири рядки, але в модулі.
// Запуск: node 01b-event-loop-order-esm.mjs
//
// Сюрприз: тут p (проміс) стоїть РАНІШЕ за n (nextTick), на відміну від 01.
// Причина: ESM-модуль сам виконується всередині промісу, тож черга
// мікрозадач обробляється раніше за nextTick.

setTimeout(() => console.log('t  setTimeout 0'), 0);
setImmediate(() => console.log('i  setImmediate'));
process.nextTick(() => console.log('n  nextTick'));
Promise.resolve().then(() => console.log('p  promise'));
