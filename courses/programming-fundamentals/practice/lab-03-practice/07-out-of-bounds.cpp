// Дослід 7: одна комірка за край. Гість отримує відмову, хост — звіт ASan.
// Запуск: ./run.sh 07 3     — у межах: обидва записи вдалі
//         ./run.sh 07 4     — на одиницю за межу
//         ./run.sh 07 -1    — на одиницю перед початком
// Lab 03, M4 · Notes 03, §5 · errors.notes.md §3
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4;

struct Memory { Byte data[MEM_SIZE] = {}; };

// Як mem_set у проєкті: перевірити адресу, перш ніж писати.
bool mem_set(Memory& mem, std::size_t addr, Byte value) {
    if (addr >= MEM_SIZE) return false;
    mem.data[addr] = value;
    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 07 <індекс>   наприклад: 3, 4, -1\n";
        return 1;
    }
    long i = 0;
    try {
        i = parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число: " << argv[1] << '\n';
        return 1;
    }

    // Гість: адреса — число, і його можна перевірити. -1 як size_t — дуже велике число.
    Memory mem;
    std::cout << "Гість (ember), розмір " << MEM_SIZE << ":\n";
    if (mem_set(mem, (std::size_t)i, 5))
        std::cout << "  set " << i << " 5 → записано\n";
    else
        std::cout << "  set " << i << " 5 → відмова: адреса за межею пам'яті. Машина живе далі.\n";

    // Хост: голий масив C++. Перевірки немає, тож пише туди, куди скажуть.
    int a[4] = {1, 2, 3, 4};
    std::cout << "\nХост (C++), int a[4]:\n  a[" << i << "] = 5 ..." << std::endl;
    a[i] = 5;
    std::cout << "  записано, a[" << i << "] = " << a[i] << '\n';
}
