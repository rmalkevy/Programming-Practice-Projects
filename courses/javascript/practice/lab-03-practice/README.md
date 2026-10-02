# Lab 03: практика

Експерименти до [Lab 03](../../lab-03-async-javascript.md) і його [нотаток](../../lab-03-async-javascript.notes.md).
Кожен файл запускається окремо й показує одну ідею. Встановлювати нічого не треба
(Node 20+, без залежностей).

## Порядок показу

| Файл | Запуск | Розділ нотаток | Що показує |
|---|---|---|---|
| `01-once-and-later.js` | `node 01-once-and-later.js` | §1 | другий `resolve` ігнорується; `.then` готового проміса все одно біжить пізніше |
| `02-await-order.js` | `node 02-await-order.js` | §2 | синхронне, мікрозадачі, таймер; `await null`; головоломка `4 6 2 5 3 1`; обробник повідомлень |
| `03-chain.js` | `node 03-chain.js` | §3 | забутий `return`; `throw` і `catch`; `async` завжди повертає проміс |
| `04-fetch-404.js` | `node 04-fetch-404.js` | §4 | 404 виконується, відсутній хост відхиляється; тіло окремим `await`; `fetchJson` |
| `05-all-vs-sequential.js` | `node 05-all-vs-sequential.js` | §5 | 2000 мс проти 1000 мс; «slow still ran»; `allSettled`, `race`, `any`; прогрес |
| `06-abort.js` | `node 06-abort.js` | §6 | `AbortError`, `TimeoutError`, `race` не скасовує запит |
| `07-promise-vs-event.js` | `node 07-promise-vs-event.js` | §7 | проміс пам'ятає, подія ні; `once()` |
| `08-unhandled-rejection.js` | `node 08-unhandled-rejection.js`, потім `--fix` | §6 | reject без `catch` валить Node (код виходу 1) |
| `browser.html` | відкрити в браузері | §4, §6, M4 | те саме в браузері: 404, `unhandledrejection`, порядок із `requestAnimationFrame` |

## Мережа

У нотатках використано `httpbin.org`. Тут його замінює `mock-server.js` (`/status/404`, `/json`, `/delay/N`),
тому на парі не залежимо від інтернету.

- Скрипти `04` і `06` піднімають сервер самі.
- Для `browser.html` запусти в окремому терміналі `node mock-server.js` (порт 3003).

## Примітки для показу

- Перед кожною частиною проси прогноз уголос, потім запускай. У `02`, `03`, `05` частини розділені заголовками `--- A`, `--- B`.
- `06`, частина B: `AbortSignal.timeout` дає `TimeoutError`, а не `AbortError`. У нотатках лаби про це не сказано, добре питання студентам.
- `07`: після першого вибуху чути лише `heard 1`. «too late» озветься лише на другий вибух.
- `04`, частина B: потрібен DNS; без інтернету код помилки може відрізнятись, але `TypeError` лишиться.
- `browser.html`: порядок `setTimeout 0` і `requestAnimationFrame` не гарантований, а мікрозадача завжди перша.
