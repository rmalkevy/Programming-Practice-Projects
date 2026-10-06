// Дослід 8: step(CPU cpu) працює з копією, step(CPU& cpu) — із самою машиною. Але копія тягне той самий Memory*.
// Запуск: ./run.sh 08 3   — три кроки кожною функцією
// Lab 06, Теорія §4 · Notes 06, «Купа всередині ember» (останній рядок) · докладно — Lab 7
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const std::uint16_t DATA_LO = 0x800;

struct Memory { Byte data[MEM_SIZE] = {}; };

struct CPU {
    Memory* mem = nullptr;
    std::uint16_t pc = 0;
    Byte a = 0;
};

// Крок-іграшка: A = A + 1, записати A за адресою 0x800 + PC, PC = PC + 1.
void step_copy(CPU cpu) {
    cpu.a = (Byte)(cpu.a + 1);
    cpu.mem->data[DATA_LO + cpu.pc] = cpu.a;
    cpu.pc = (std::uint16_t)(cpu.pc + 1);
}   // тут копія зникає разом зі своїми pc і a

void step_ref(CPU& cpu) {
    cpu.a = (Byte)(cpu.a + 1);
    cpu.mem->data[DATA_LO + cpu.pc] = cpu.a;
    cpu.pc = (std::uint16_t)(cpu.pc + 1);
}

void report(const std::string& title, const CPU& cpu, int n) {
    std::cout << title << "\n  PC = " << cpu.pc << ", A = " << (int)cpu.a << "\n  пам'ять з 0x800:";
    for (int i = 0; i < n; ++i) std::cout << ' ' << (int)cpu.mem->data[DATA_LO + i];
    std::cout << "\n\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 08 <кроків>   наприклад: 3\n";
        return 1;
    }
    int n = 0;
    try {
        n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 1 || n > 16) {
        std::cout << "від 1 до 16\n";
        return 1;
    }

    Memory m1, m2;
    CPU c1{&m1}, c2{&m2};   // агрегатна ініціалізація: pc і a — нулі

    for (int i = 0; i < n; ++i) step_copy(c1);
    report(std::to_string(n) + " × step_copy(CPU cpu):", c1, n);

    for (int i = 0; i < n; ++i) step_ref(c2);
    report(std::to_string(n) + " × step_ref(CPU& cpu):", c2, n);

    std::cout << "Копія CPU копіює поле mem — адресу на " << sizeof(Memory*) << " байтів, а не "
              << sizeof(Memory) << " байтів самої пам'яті.\n";
}
