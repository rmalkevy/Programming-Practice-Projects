// Дослід 3: той самий байт — чотири погляди. Літерали 65, 0x41, 0b01000001 і 'A' — одні біти.
// Запуск: ./run.sh 03 65 0x41 0b01000001 A
//         ./run.sh 03 A a 0 9 10 32 127 200
// Lab 01, Теорія §2, §4, M3 · Notes 01, §4
#include "common.hpp"

// Одна комірка — чотири погляди, як show_byte у M3.
void show(std::uint8_t b) {
    std::cout << std::setw(3) << (int)b << "  " << hex(b) << "  0b";
    for (int i = 7; i >= 0; --i) std::cout << ((b >> i) & 1);
    std::cout << "  '" << glyph(b) << "'";
    if (b == 0) std::cout << "   ← '\\0', кінець C-рядка";
    if (b == 9) std::cout << "   ← '\\t', табуляція";
    if (b == 10) std::cout << "   ← '\\n', новий рядок";
    if (b == 32) std::cout << "   ← пробіл: друкується, просто його не видно";
    if (b == 127 || (b > 0 && b < 32 && b != 9 && b != 10)) std::cout << "   ← керівний символ, не друкується";
    if (b > 127) std::cout << "   ← поза ASCII";
    std::cout << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 03 <число або символ> [...]   наприклад: 65 0x41 0b01000001 A\n";
        return 1;
    }
    long first = -1;
    for (int i = 1; i < argc; ++i) {
        std::cout << std::left << std::setw(12) << argv[i] << std::right;
        try {
            long v = parse_value(argv[i]);
            if (v < 0 || v > 255) {
                std::cout << v << " не влазить у байт; (std::uint8_t) лишає " << (int)(std::uint8_t)v << '\n'
                          << std::setw(12) << "";
            }
            show((std::uint8_t)v);
            if (first < 0) first = (std::uint8_t)v;
        } catch (const std::exception&) {
            std::cout << "не можу прочитати як число чи символ\n";
        }
    }

    // Символ — це число: з ним можна рахувати.
    if (first >= 0) {
        char c = (char)first;
        std::cout << "\nАрифметика з символом " << (int)first << ":\n";
        std::cout << "  c + 1          = " << c + 1 << "     ← char у виразі стає int\n";
        std::cout << "  (char)(c + 1)  = '" << glyph((std::uint8_t)(c + 1)) << "'\n";
        std::cout << "  (char)(c ^ 32) = '" << glyph((std::uint8_t)(c ^ 32))
                  << "'     ← у ASCII велика й мала літера різняться одним бітом\n";
    }
}
