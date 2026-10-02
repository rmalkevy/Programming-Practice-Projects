// Експеримент 2 (§2): порядок синхронного коду, мікрозадач, таймерів і await.
// Запуск: node 02-await-order.js
//
// Кожна частина друкується з паузою між ними, щоб виводи не змішувались.
// Перед кожною частиною зупиняйся і проси прогноз уголос.
const pause = () => new Promise((resolve) => setTimeout(resolve, 50));

// Частина A. Очікування: 2, 1
console.log('--- A');
Promise.resolve(1).then(console.log);
console.log(2);
await pause();

// Частина B: додаємо таймер. Очікування: 2, 1, 4
console.log('--- B');
setTimeout(() => console.log(4), 0);
Promise.resolve(1).then(() => console.log(1));
console.log(2);
await pause();

// Частина C: await null віддає чергу. Очікування: 1, 3, 2
console.log('--- C');
async function a() {
  console.log(1);
  await null;
  console.log(2);
}
a();
console.log(3);
await pause();

// Частина D: головоломка з лаби. Очікування: 4, 6, 2, 5, 3, 1
console.log('--- D');
setTimeout(() => console.log(1), 0);
Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));
(async () => {
  console.log(4);
  await 0;
  console.log(5);
})();
console.log(6);
await pause();

// Частина E: обробник повідомлень з await. Два обробники живуть одночасно.
// Дивись, як вони перемежовуються: перевірка 1, перевірка 2, потім робота.
console.log('--- E');
const lightProcess = async (e) => {
  console.log(`  перевірка ${e.id}`);
  return e.ok;
};
const heavyProcess = (e) => console.log(`  важка робота ${e.id}`);
const acknowledgment = (id, ok) => console.log(`  підтвердження ${id}: ${ok}`);

async function onMessage(arrivedEvent) {
  const eventStatus = await lightProcess(arrivedEvent);
  if (eventStatus !== true) {
    acknowledgment(arrivedEvent.id, false);
    return;
  }
  heavyProcess(arrivedEvent);
  acknowledgment(arrivedEvent.id, true);
}
onMessage({ id: 1, ok: true });
onMessage({ id: 2, ok: false });
console.log('  (обидва виклики повернулись, а підтверджень ще немає)');
