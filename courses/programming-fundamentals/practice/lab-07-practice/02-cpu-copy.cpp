// Дослід 2: step(CPU cpu) працює з копією машини. PC того, хто викликав, стоїть, а байти копіюються щоразу.
// Запуск: ./run.sh 02 3      — три кроки: за значенням і за посиланням
// Lab 07, «Про що ця лаба», Теорія §2 · Notes 07, §1
#include "common.hpp"

using Byte = std::uint8_t;

struct CPU {
    Byte mem[4096] = {};   // у справжньому ember пам'ять окремо, тут — усередині, щоб копія була чесною
    std::uint16_t pc = 0;
    Byte a = 0;
};

// Крок: NOP завдовжки в один байт, лише PC + 1.
void step_copy(CPU cpu) {
    std::cout << "    step_copy: &cpu = " << &cpu << "  PC " << cpu.pc;
    cpu.pc = (std::uint16_t)(cpu.pc + 1);
    std::cout << " → " << cpu.pc << '\n';
}

void step_ref(CPU& cpu) {
    std::cout << "    step_ref:  &cpu = " << &cpu << "  PC " << cpu.pc;
    cpu.pc = (std::uint16_t)(cpu.pc + 1);
    std::cout << " → " << cpu.pc << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 02 <скільки кроків>   наприклад: 3\n";
        return 1;
    }
    long n = 0;
    try {
        n = parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 0 || n > 20) {
        std::cout << "кроків — від 0 до 20\n";
        return 1;
    }

    CPU cpu;
    std::cout << "sizeof(CPU) = " << sizeof(CPU) << " байтів, у main &cpu = " << &cpu << "\n\n";

    std::cout << "За значенням:\n";
    for (long i = 0; i < n; ++i) step_copy(cpu);
    std::cout << "  у main PC = " << cpu.pc << ", скопійовано " << n * (long)sizeof(CPU) << " байтів\n\n";

    std::cout << "За посиланням:\n";
    for (long i = 0; i < n; ++i) step_ref(cpu);
    std::cout << "  у main PC = " << cpu.pc << ", скопійовано 0 байтів\n";
}
