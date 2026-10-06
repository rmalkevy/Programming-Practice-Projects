// Дослід 4: молодший байт уперед. Як 16-бітне число лягає у дві комірки.
// Запуск: ./run.sh 04 0x1234
//         ./run.sh 04 0x0800    — адреса початку даних
// Lab 03, Теорія §5, M1 · ISA.uk.md §4 · Notes 03, §5
#include "common.hpp"
#include <cstring>

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 8;   // маленька пам'ять, щоб дамп умістився в рядок

struct Memory { Byte data[MEM_SIZE] = {}; };

// ДАНО в лабі.
std::uint16_t get16(const Memory& mem, std::size_t addr) {
    Byte lo = mem.data[addr];
    Byte hi = mem.data[addr + 1];
    return (std::uint16_t)(lo | (hi << 8));
}

// Дзеркало get16 — те, що студенти пишуть у M1.
void set16(Memory& mem, std::size_t addr, std::uint16_t value) {
    mem.data[addr] = (Byte)(value & 0xFF);      // молодший
    mem.data[addr + 1] = (Byte)(value >> 8);    // старший
}

void dump(const Byte* p, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) std::cout << hex2(p[i]) << ' ';
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 04 <16-бітне число>   наприклад: 0x1234\n";
        return 1;
    }
    long value = 0;
    try {
        value = parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число: " << argv[1] << '\n';
        return 1;
    }
    std::uint16_t v = (std::uint16_t)value;
    if (value < 0 || value > 0xFFFF)
        std::cout << value << " не влазить у 16 бітів; uint16_t лишає " << hex16(v) << "\n\n";

    std::cout << "v = " << hex16(v) << ":  старший байт " << hex(v >> 8)
              << ", молодший " << hex(v & 0xFF) << "\n\n";

    Memory mem;
    set16(mem, 2, v);
    std::cout << "ember, set16 2 " << hex16(v) << ":\n";
    std::cout << "  адреси  0  1  2  3  4  5  6  7\n  дамп    ";
    for (std::size_t i = 0; i < MEM_SIZE; ++i) std::cout << hex2(mem.data[i]) << ' ';
    std::cout << "\n  get16 2 = " << hex16(get16(mem, 2)) << "   ← має повернутись те, що записали\n";
    std::cout << "  get16 3 = " << hex16(get16(mem, 3)) << "   ← почали читати на комірку пізніше\n";

    // Якби хтось записав старшим уперед, а читав молодшим уперед:
    Memory wrong;
    wrong.data[2] = (Byte)(v >> 8);
    wrong.data[3] = (Byte)(v & 0xFF);
    std::cout << "\nЗаписали старшим уперед (big-endian), читаємо get16:\n";
    std::cout << "  дамп    ";
    dump(wrong.data, MEM_SIZE);
    std::cout << "\n  get16 2 = " << hex16(get16(wrong, 2)) << "   ← байти помінялись місцями\n";

    // Так само лягають операнди інструкцій ember.
    std::cout << "\nОперанди в коді ember:\n";
    std::cout << "  JMP   " << hex16(v) << "    →  30 " << hex2(v & 0xFF) << ' ' << hex2(v >> 8) << '\n';
    std::cout << "  LOADH H, " << hex16(v) << " →  28 " << hex2(v & 0xFF) << ' ' << hex2(v >> 8) << '\n';

    // А як лежить uint16_t у пам'яті цього ноутбука? Дивимось через memcpy, без UB.
    Byte host[4];
    std::memcpy(host, &v, 2);
    std::cout << "\nХост: uint16_t " << hex16(v) << " у пам'яті цього процесу:  ";
    dump(host, 2);
    std::uint32_t w = 0x12345678;
    std::memcpy(host, &w, 4);
    std::cout << "\n      uint32_t 0x12345678:                      ";
    dump(host, 4);
    std::cout << "\n      " << (host[0] == 0x78 ? "молодший уперед, як в ember" : "старший уперед, не як в ember")
              << '\n';
}
