// Дослід 6: навіщо OUTS стеля. Рядок гостя закінчується там, де гість поклав нуль, — або ніде.
// Запуск: ./run.sh 06 HELLO                 — HELLO\0 з 0x800: обидва друки однакові
//         ./run.sh 06 OK repeat=200         — 400 байтів без нуля посередині
//         ./run.sh 06 HELLO at=0xFFD        — рядок наприкінці пам'яті: на '\0' місця немає
// Lab 05, Теорія §3, M4 · Notes 05, §3 · ISA.uk.md §5, OUTS
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const int OUTS_MAX = 256;

struct Memory { Byte data[MEM_SIZE] = {}; };

// Тільки до нуля — як strlen. Що гість поклав, те й надрукуємо.
int print_until_zero(const Memory& mem, std::size_t addr) {
    int n = 0;
    while (mem.data[addr + n] != 0) {
        std::cout << (char)mem.data[addr + n] << std::flush;   // щоб надруковане не загубилось, якщо впаде
        ++n;
    }
    return n;
}

// До нуля, але не більше OUTS_MAX байтів і не далі кінця пам'яті.
int print_with_ceiling(const Memory& mem, std::size_t addr) {
    int n = 0;
    while (n < OUTS_MAX && addr + n < MEM_SIZE && mem.data[addr + n] != 0) {
        std::cout << (char)mem.data[addr + n];
        ++n;
    }
    return n;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 06 <текст латиницею> [repeat=N] [at=0x800]   наприклад: HELLO\n";
        return 1;
    }
    std::string text = argv[1];
    long repeat = 1, at = 0x800;
    try {
        for (int i = 2; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("repeat=", 0) == 0) repeat = parse_number(arg.substr(7));
            else if (arg.rfind("at=", 0) == 0) at = parse_number(arg.substr(3));
            else throw std::invalid_argument(arg);
        }
    } catch (const std::exception&) {
        std::cout << "не можу прочитати: очікую repeat=N або at=ADDR\n";
        return 1;
    }
    if (at < 0 || at >= (long)MEM_SIZE || repeat < 1) {
        std::cout << "at — від 0 до 0xFFF, repeat — від 1\n";
        return 1;
    }

    static Memory mem;   // 4 КБ — не на стеку
    long addr = at;
    for (long r = 0; r < repeat; ++r)
        for (char ch : text)
            if (addr < (long)MEM_SIZE) mem.data[addr++] = (Byte)ch;
    bool zero = addr < (long)MEM_SIZE;
    if (zero) mem.data[addr] = 0;

    std::cout << "Байтів покладено з " << hex16((std::uint16_t)at) << ": " << addr - at;
    if (zero) std::cout << ", а нуль — на " << hex16((std::uint16_t)addr) << '\n';
    else std::cout << ", аж до кінця пам'яті. Нуля немає: на нього не лишилось місця\n";

    std::cout << "\nЗі стелею (" << OUTS_MAX << " байтів і кінець пам'яті):\n  \"";
    int n = print_with_ceiling(mem, (std::size_t)at);
    std::cout << "\"\n  надруковано: " << n << '\n';

    std::cout << "\nЛише до нуля:\n  \"" << std::flush;
    n = print_until_zero(mem, (std::size_t)at);
    std::cout << "\"\n  надруковано: " << n << '\n';
}
