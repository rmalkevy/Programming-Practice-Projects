// Дослід 7: дамп із ASCII-колонкою. Байти, рядок і нуль, що його закінчує.
// Запуск: ./run.sh 07 65 66 0             — у колонці |AB..............|
//         ./run.sh 07 H i 0 '!'           — після нуля C-рядок закінчився
//         ./run.sh 07 72 105 10 9 200 255
// Байти кладуться з адреси 0; можна числами або символами.
// Lab 01, Теорія §4, M2, M4.3
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t SIZE = 32;          // дві стрічки дампу замість 256
const std::size_t BYTES_PER_LINE = 16;

struct Memory { Byte data[SIZE]{}; };

// Як dump у скелеті: зовнішній цикл по рядках, внутрішній по стовпцях.
void dump(const Memory& mem) {
    for (std::size_t row = 0; row < SIZE; row += BYTES_PER_LINE) {
        std::cout << std::hex << std::setfill('0') << std::setw(4) << row << "  ";
        for (std::size_t col = 0; col < BYTES_PER_LINE; ++col)
            std::cout << std::setw(2) << (int)mem.data[row + col] << ' ';
        std::cout << " |";
        for (std::size_t col = 0; col < BYTES_PER_LINE; ++col)
            std::cout << glyph(mem.data[row + col]);
        std::cout << "|\n";
    }
    std::cout << std::dec << std::setfill(' ');
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 07 <байт або символ> [...]   наприклад: 65 66 0\n";
        return 1;
    }
    Memory mem;
    std::size_t n = 0;
    try {
        for (int i = 1; i < argc && n < SIZE - 1; ++i) {
            long v = parse_value(argv[i]);
            if (v < 0 || v > 255) {
                std::cout << "байт — це 0..255, отримав " << v << '\n';
                return 1;
            }
            mem.data[n++] = (Byte)v;
        }
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число чи символ\n";
        return 1;
    }

    dump(mem);

    // Той самий початок пам'яті як C-рядок: друкує, доки не трапиться нуль.
    // Останній байт у mem завжди нуль (n < SIZE - 1), тож за межу не вийде.
    // Невидимі байти показуємо як \n, \t, \xC8 — інакше термінал їх виконає або зіпсує.
    std::string text = (const char*)mem.data;
    std::string shown;
    for (unsigned char c : text) {
        if (c == '\n') shown += "\\n";
        else if (c == '\t') shown += "\\t";
        else if (c >= 0x20 && c <= 0x7E) shown += (char)c;
        else shown += "\\x" + hex2(c);
    }
    std::cout << "\nяк C-рядок: \"" << shown << "\"  — " << text.size() << " байт(и) до першого нуля\n";
}
