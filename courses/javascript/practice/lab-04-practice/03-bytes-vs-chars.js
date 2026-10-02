// Експеримент 3: байти != символи.
// Запуск: node 03-bytes-vs-chars.js
const text = 'привіт';

console.log('символів (text.length):   ', text.length);
console.log('байтів у UTF-8 (Buffer):  ', Buffer.from(text).length);

// Кожна українська літера = 2 байти. Подивимось самі байти:
console.log('байти:', Buffer.from(text));

// Два байти 0xff 0x00 як одне число (big-endian: старший байт першим):
console.log('readUInt16BE:', Buffer.from([0xff, 0x00]).readUInt16BE(0)); // 65280
console.log('readUInt16LE:', Buffer.from([0xff, 0x00]).readUInt16LE(0)); // 255

// Той самий результат без Buffer, працює і в браузері:
console.log('TextEncoder:', new TextEncoder().encode(text).length);
console.log('DataView:', new DataView(new Uint8Array([0xff, 0x00]).buffer).getUint16(0));
