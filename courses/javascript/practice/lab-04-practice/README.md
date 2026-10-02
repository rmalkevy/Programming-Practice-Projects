# Lab 04: практика

Експерименти до [Lab 04](../../lab-04-node-streams-websockets.md) і його [нотаток](../../lab-04-node-streams-websockets.notes.md).
Кожен файл запускається окремо й показує одну ідею.

## Перший запуск

```bash
cd courses/javascript/practice/lab-04-practice
npm install        # ставить ws
```

Потрібен Node 20+ (перевірити: `node -v`).

## Порядок показу

| Файл | Запуск | Що показує |
|---|---|---|
| `01-event-loop-order.cjs` | `node 01-event-loop-order.cjs` | `nextTick` раніше за проміс; `setTimeout 0` проти `setImmediate` (запусти кілька разів); у I/O-колбеку порядок стабільний |
| `01b-event-loop-order-esm.mjs` | `node 01b-event-loop-order-esm.mjs` | ті самі рядки в ESM: проміс раніше за `nextTick` |
| `02-emitter-error.js` | `node 02-emitter-error.js`, потім `--fix` | `error` без слухача валить процес |
| `03-bytes-vs-chars.js` | `node 03-bytes-vs-chars.js` | `'привіт'.length` = 6, байтів 12; big-endian проти little-endian; `TextEncoder` як аналог для браузера |
| `04-backpressure.js` | `node 04-backpressure.js naive`, потім `pipeline` | `write()` повертає `false`; черга приймача 31 MB проти 0.1 MB |
| `05-ws-echo.js` | `node 05-ws-echo.js` | сервер і клієнт WebSocket в одному скрипті |
| `06-ws-maxpayload.js` | `node 06-ws-maxpayload.js` | `maxPayload`: помилка на сервері, код закриття 1009 на клієнті |

## Примітки для показу

- У `04` дивіться на **«у черзі приймача»**, а не на `rss`: на 32 MB шум пам'яті процесу
  перекриває різницю. Щоб `rss` став показовим, збільште `CHUNKS` (наприклад, до 5000).
  Це вже ~320 MB, тож `naive` краще не запускати на слабкій машині.
- У `01` і `01b` перед запуском питайте студентів, який буде порядок.
- У `05` і `06` порт вибирається автоматично, тому конфліктів із запущеним сервером не буде.
