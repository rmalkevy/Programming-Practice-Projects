// Дослід 1: один байт — три записи.
// Запуск: ./run.sh 01 0xA3      (або 163, або 0b10100011; можна кілька чисел)
// Lab 02, Теорія §1 · Notes 02, §1
#include "common.hpp"

void show(long value) {
    std::uint8_t x = (std::uint8_t)value;   // у байт влазить лише 0..255
    if (value < 0 || value > 255)
        std::cout << "  " << value << " не влазить у байт; uint8_t лишає " << (int)x << '\n';

    std::cout << "  шістнадцятковий: " << hex(x) << '\n';
    std::cout << "  двійковий:       " << bits(x) << '\n';
    std::cout << "  десятковий:      " << (int)x << '\n';

    // Позиційний запис: кожен біт множиться на свою вагу.
    std::cout << "  по бітах:        ";
    for (int i = 7; i >= 0; --i) {
        std::cout << ((x >> i) & 1) << "·" << (1 << i);
        if (i > 0) std::cout << " + ";
    }
    std::cout << " = " << (int)x << '\n';

    // Одна шістнадцяткова цифра — це рівно чотири біти.
    int hi = x >> 4, lo = x & 0x0F;
    std::cout << "  по півбайтах:    " << std::hex << std::uppercase << hi << std::dec
              << "·16 + " << std::hex << lo << std::dec
              << " = " << hi << "·16 + " << lo << " = " << (int)x << "\n\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 01 <число> [число ...]   наприклад: 0xA3 163 0b1111\n";
        return 1;
    }
    for (int i = 1; i < argc; ++i) {
        std::cout << argv[i] << '\n';
        try {
            show(parse_number(argv[i]));
        } catch (const std::exception&) {
            std::cout << "  не можу прочитати як число\n\n";
        }
    }
}
