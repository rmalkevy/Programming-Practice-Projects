// Дослід 9: перевірка меж має стояти ДО запису. Той самий mem_set двома способами.
// Запуск: ./run.sh 09 0 65       — у межах: обидва записують
//         ./run.sh 09 4095 1     — остання комірка
//         ./run.sh 09 4096 1     — перша за межею
//         ./run.sh 09 5000 1     — як у checks/lab-01.txt
// Lab 01, M3 · CHECKS.md, Lab 1
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;

struct Memory { Byte data[MEM_SIZE]{}; };

// Правильно: спершу перевірити, потім писати.
bool mem_set(Memory& mem, std::size_t addr, Byte value) {
    if (addr >= MEM_SIZE) return false;
    mem.data[addr] = value;
    return true;
}

// Ті самі рядки в іншому порядку: перевірка є, але запис уже стався.
bool mem_set_late(Memory& mem, std::size_t addr, Byte value) {
    mem.data[addr] = value;
    if (addr >= MEM_SIZE) return false;
    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 09 <адреса> <байт>   наприклад: 0 65, 4096 1\n";
        return 1;
    }
    long addr = 0, value = 0;
    try {
        addr = parse_number(argv[1]);
        value = parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (addr < 0 || value < 0 || value > 255) {
        std::cout << "адреса — від 0, байт — 0..255 (це перевіряє main.cpp скелета)\n";
        return 1;
    }

    Memory* mem = new Memory;
    std::cout << "перевірка до запису:    set " << addr << ' ' << value << " → "
              << (mem_set(*mem, (std::size_t)addr, (Byte)value) ? "записано" : "відмова: адреса за межею")
              << std::endl;
    std::cout << "перевірка після запису: set " << addr << ' ' << value << " → " << std::flush;
    bool ok = mem_set_late(*mem, (std::size_t)addr, (Byte)value);
    std::cout << (ok ? "записано" : "відмова: адреса за межею — але байт уже записано туди") << '\n';
    delete mem;
}
