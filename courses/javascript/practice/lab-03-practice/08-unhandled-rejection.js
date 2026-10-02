// Експеримент 8 (§6, кінець): reject без .catch.
// Запуск:
//   node 08-unhandled-rejection.js         -> Node падає (код виходу 1)
//   node 08-unhandled-rejection.js --fix   -> із обробником, процес живий
// Перевір код виходу: echo $?
// У браузері те саме показує browser.html (подія unhandledrejection).

if (process.argv.includes('--fix')) {
  process.on('unhandledRejection', (reason) => {
    console.log('unhandledRejection:', reason.message);
  });
}

Promise.reject(new Error('x'));

setTimeout(() => console.log('якщо ти це бачиш, процес вижив'), 100);
