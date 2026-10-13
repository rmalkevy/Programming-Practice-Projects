#include "dump.hpp"
#include <iostream>
#include <iomanip>
#include <bitset>

void dump(const Memory& mem) {
    for (std::size_t i = 0; i < MEM_SIZE; i += 16) {
        // Друкуємо адресу (0000, 0010, 0020...)
        std::cout << std::hex << std::uppercase << std::setfill('0') << std::setw(4) << i << "  ";

        // Hex-колонки (байтив у шістнадцятковому вигляді)
        for (std::size_t j = 0; j < 16; ++j) {
            std::cout << std::setw(2) << static_cast<int>(mem.data[i + j]) << ' ';
        }

        std::cout << " |";

        // ASCII-колонка (символи)
        for (std::size_t j = 0; j < 16; ++j) {
            Byte b = mem.data[i + j];
            if (b >= 32 && b <= 126) {
                std::cout << static_cast<char>(b);
            } else {
                std::cout << '.';
            }
        }

        std::cout << "|\n" << std::dec;
    }
}

void show_byte(Byte b) {
    // 1. Десятичний формат
    std::cout << static_cast<int>(b) << "  ";

    // 2. Шістнадцятичний формат (0x41)
    std::cout << "0x" << std::hex << std::uppercase 
              << std::setfill('0') << std::setw(2) << static_cast<int>(b) << std::dec << "  ";

    // 3. Двійковий формат (0b01000001)
    std::cout << "0b" << std::bitset<8>(b) << "  ";

    // 4. Символьний ASCII ('A' або '.')
    if (b >= 32 && b <= 126) {
        std::cout << "'" << static_cast<char>(b) << "'";
    } else {
        std::cout << "'.' (non-printable)";
    }
    std::cout << '\n';
}