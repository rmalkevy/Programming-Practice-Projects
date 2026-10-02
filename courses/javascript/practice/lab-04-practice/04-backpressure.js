// Експеримент 4: backpressure. Безпечна версія: кількість кроків обмежена.
// Запуск:
//   node 04-backpressure.js naive      -> ігноруємо write() === false
//   node 04-backpressure.js pipeline   -> pipeline сам чекає 'drain'
//
// Дивимось на writableLength: скільки байтів лежить у черзі приймача.
import { Readable, Writable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

const CHUNKS = 500;               // 500 * 64 KB = ~32 MB
const CHUNK_SIZE = 64 * 1024;
const mb = (n) => (n / 1024 / 1024).toFixed(1) + ' MB';

// Повільний приймач: кожен шматок "пишеться" 5 мс.
function slowSink() {
  return new Writable({
    highWaterMark: 64 * 1024,     // поріг, після якого write() поверне false
    write(chunk, encoding, callback) {
      setTimeout(callback, 5);
    },
  });
}

const mode = process.argv[2];

if (mode === 'naive') {
  const sink = slowSink();
  let falseCount = 0;
  for (let i = 0; i < CHUNKS; i++) {
    if (!sink.write(Buffer.alloc(CHUNK_SIZE))) falseCount++; // ігноруємо false!
  }
  console.log('write() повернув false разів:', falseCount);
  console.log('у черзі приймача:', mb(sink.writableLength));
  console.log('rss процесу:     ', mb(process.memoryUsage().rss));
  sink.end();
} else if (mode === 'pipeline') {
  const sink = slowSink();
  let maxQueued = 0;
  const timer = setInterval(() => {
    maxQueued = Math.max(maxQueued, sink.writableLength);
  }, 20);

  function* chunks() {
    for (let i = 0; i < CHUNKS; i++) yield Buffer.alloc(CHUNK_SIZE);
  }
  await pipeline(Readable.from(chunks()), sink);
  clearInterval(timer);

  console.log('максимум у черзі приймача:', mb(maxQueued));
  console.log('rss процесу:              ', mb(process.memoryUsage().rss));
} else {
  console.log('Вкажи режим: node 04-backpressure.js naive | pipeline');
}
