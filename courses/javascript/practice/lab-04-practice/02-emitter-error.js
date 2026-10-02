// Експеримент 2: 'error' без слухача валить процес.
// Запуск:
//   node 02-emitter-error.js          -> процес падає
//   node 02-emitter-error.js --fix    -> із слухачем, процес живий
import { EventEmitter } from 'node:events';

const emitter = new EventEmitter();

if (process.argv.includes('--fix')) {
  emitter.on('error', (err) => console.log('перехопив помилку:', err.message));
}

console.log('перед emit');
emitter.emit('error', new Error('boom'));
console.log('після emit: якщо ти це бачиш, процес вижив');
