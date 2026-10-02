// Браузерна частина Lab 03. Підключається з browser.html.
const BASE = 'http://localhost:3003'; // mock-server.js
const out = document.getElementById('out');

function log(...args) {
  console.log(...args);
  out.textContent += args.join(' ') + '\n';
}
const header = (text) => log('\n--- ' + text);

// 1. fetch: 404 виконується, відсутній хост відхиляється (Lab 03, §4)
document.getElementById('fetch404').onclick = async () => {
  header('fetch 404 проти мережевої помилки');
  try {
    const r = await fetch(`${BASE}/status/404`);
    log('404: проміс виконався. ok:', r.ok, 'status:', r.status);
  } catch (e) {
    log('404: reject?!', e.name, '(mock-server не запущено?)');
    return;
  }
  try {
    await fetch('https://no-such-host.invalid/');
  } catch (e) {
    log('немає хоста: reject,', e.name);
  }
};

// 2. unhandledrejection (Lab 03, §6): у браузері сторінка не падає, лише подія
window.addEventListener('unhandledrejection', (e) => {
  log('unhandledrejection:', e.reason.message);
  e.preventDefault(); // без цього ще й червоний рядок у консолі
});
document.getElementById('unhandled').onclick = () => {
  header('reject без catch');
  Promise.reject(new Error('x'));
  log('(рядок після Promise.reject: сторінка не впала)');
};

// 3. Порядок з requestAnimationFrame (Lab 03, M4)
// Мікрозадача завжди перша; setTimeout 0 і rAF зазвичай у порядку
// "таймер, потім rAF", але це не гарантовано: rAF чекає наступного кадру.
document.getElementById('order').onclick = () => {
  header('порядок (спитай прогноз)');
  setTimeout(() => log('setTimeout 0'), 0);
  requestAnimationFrame(() => log('requestAnimationFrame'));
  Promise.resolve().then(() => log('мікрозадача'));
  log('синхронно');
};

document.getElementById('clear').onclick = () => { out.textContent = ''; };
