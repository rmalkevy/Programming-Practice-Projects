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
