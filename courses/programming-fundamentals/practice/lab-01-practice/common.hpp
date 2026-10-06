// Спільне для всіх дослідів: прочитати число з командного рядка й надрукувати байт.
// Тут немає ідей цієї лаби — лише те, що заважало б дивитись на них.
#pragma once
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

// "0x..." — шістнадцяткове, "0b..." — двійкове, інакше десяткове (можна з мінусом).
// Кидає виняток, якщо рядок — не число.
inline long parse_number(const std::string& s) {
    std::string t = s;
    bool minus = !t.empty() && t[0] == '-';
    if (minus) t = t.substr(1);
    int base = 10;
    std::string p = t.substr(0, 2);
    if (p == "0x" || p == "0X") { base = 16; t = t.substr(2); }
    if (p == "0b" || p == "0B") { base = 2;  t = t.substr(2); }
    std::size_t used = 0;
    long v = std::stol(t, &used, base);
    if (used != t.size()) throw std::invalid_argument(s);
    return minus ? -v : v;
}

// "1010 0011" — вісім бітів, пробіл між півбайтами.
inline std::string bits(std::uint8_t x) {
    std::string out;
    for (int i = 7; i >= 0; --i) {
        out += ((x >> i) & 1) ? '1' : '0';
        if (i == 4) out += ' ';
    }
    return out;
}

// "0xA3"
inline std::string hex(std::uint8_t x) {
    std::ostringstream out;
    out << "0x" << std::uppercase << std::hex << std::setw(2) << std::setfill('0') << (int)x;
    return out.str();
}

// "A3" — так байти пишуться в дампі
inline std::string hex2(std::uint8_t x) {
    return hex(x).substr(2);
}

// "0x0800" — адреса гостя
inline std::string hex16(std::uint16_t x) {
    std::ostringstream out;
    out << "0x" << std::uppercase << std::hex << std::setw(4) << std::setfill('0') << x;
    return out.str();
}

// Доповнити рядок пробілами до w символів. std::setw рахує байти, а кирилична
// літера в UTF-8 — це два байти, тож колонки з українським текстом роз'їжджаються.
inline std::string pad(const std::string& s, std::size_t w) {
    std::size_t chars = 0;
    for (unsigned char c : s)
        if ((c & 0xC0) != 0x80) ++chars;
    return chars >= w ? s : s + std::string(w - chars, ' ');
}

// Як parse_number, але ще й символ: A або 'A' дає 65.
inline long parse_value(const std::string& s) {
    if (s.size() == 3 && s[0] == '\'' && s[2] == '\'') return (unsigned char)s[1];
    if (s.size() == 1 && !(s[0] >= '0' && s[0] <= '9')) return (unsigned char)s[0];
    return parse_number(s);
}

// Байт як символ: друкований — сам собою, решта — крапкою, як у дампі.
inline char glyph(std::uint8_t b) {
    return (b >= 0x20 && b <= 0x7E) ? (char)b : '.';
}
