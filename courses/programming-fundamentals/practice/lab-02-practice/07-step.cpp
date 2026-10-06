// Дослід 7: процесор, який крокує. decode() через маску й зсув, step() по таблиці ISA.
// Запуск: ./run.sh 07                          — сценарій з CHECKS.md: A=200, B=100, [ADD, HALT]
//         ./run.sh 07 a=7 b=1 12 00            — AND, HALT
//         ./run.sh 07 a=0x41 16 16 16 00       — SHL тричі: стежте за C
// Байти програми пишуться, як у дампі: шістнадцяткові, без 0x.
// Lab 02, Теорія §5, «Крок проєкту» · ISA.uk.md §3, §5
#include "common.hpp"

struct Flags { bool z = false, n = false, c = false; };

struct CPU {
    std::uint8_t mem[4096] = {};   // нулі — це HALT, тож за кінцем програми машина зупиниться
    std::uint16_t pc = 0;
    std::uint8_t a = 0, b = 0;
    Flags f;
    bool halted = false;
};

// Z і N рахуються однаково для всіх інструкцій ALU.
void set_zn(CPU& cpu) {
    cpu.f.z = cpu.a == 0;
    cpu.f.n = (cpu.a >> 7) & 1;
}

const char* name(std::uint8_t op) {
    const char* ctrl[] = {"HALT", "NOP"};
    const char* alu[] = {"ADD", "SUB", "AND", "OR", "XOR", "NOT", "SHL", "SHR", "INC", "DEC"};
    int group = (op >> 4) & 0x0F, index = op & 0x0F;
    if (group == 0 && index <= 1) return ctrl[index];
    if (group == 1 && index <= 9) return alu[index];
    return "???";
}

// Група 0x1_: усі інструкції по 1 байту, прапорці — як у ISA.uk.md §5.
void alu(CPU& cpu, int index) {
    int wide = 0;
    switch (index) {
    case 0x0: wide = cpu.a + cpu.b; cpu.f.c = wide > 0xFF;  cpu.a = (std::uint8_t)wide; break; // ADD
    case 0x1: cpu.f.c = cpu.a < cpu.b; cpu.a = (std::uint8_t)(cpu.a - cpu.b); break;        // SUB: C — позика
    case 0x2: cpu.a &= cpu.b; cpu.f.c = false; break;                                       // AND
    case 0x3: cpu.a |= cpu.b; cpu.f.c = false; break;                                       // OR
    case 0x4: cpu.a ^= cpu.b; cpu.f.c = false; break;                                       // XOR
    case 0x5: cpu.a = (std::uint8_t)~cpu.a; cpu.f.c = false; break;                         // NOT
    case 0x6: cpu.f.c = (cpu.a >> 7) & 1; cpu.a = (std::uint8_t)(cpu.a << 1); break;        // SHL
    case 0x7: cpu.f.c = cpu.a & 1; cpu.a = (std::uint8_t)(cpu.a >> 1); break;               // SHR
    case 0x8: cpu.a = (std::uint8_t)(cpu.a + 1); break;                                     // INC: C не чіпає
    case 0x9: cpu.a = (std::uint8_t)(cpu.a - 1); break;                                     // DEC: C не чіпає
    default: return;                                                                        // ще не існує
    }
    set_zn(cpu);
}

void step(CPU& cpu) {
    if (cpu.halted) {
        std::cout << "halted\n";
        return;
    }
    std::uint8_t op = cpu.mem[cpu.pc];
    int group = (op >> 4) & 0x0F;   // старший півбайт — група
    int index = op & 0x0F;          // молодший — номер у групі

    switch (group) {
    case 0x0:
        if (index == 0) cpu.halted = true;   // HALT; NOP (index 1) нічого не робить
        break;
    case 0x1:
        alu(cpu, index);
        break;
    default:
        break;                               // поки що як NOP; у Lab 4 це стане помилкою
    }
    cpu.pc += 1;                             // у груп 0x0_ і 0x1_ розмір завжди 1
}

void regs(const CPU& cpu) {
    std::cout << "A=" << std::setw(3) << (int)cpu.a << " (" << bits(cpu.a) << ")  B="
              << std::setw(3) << (int)cpu.b << "  Z=" << cpu.f.z << " N=" << cpu.f.n
              << " C=" << cpu.f.c << "  PC=" << cpu.pc;
}

int main(int argc, char* argv[]) {
    CPU cpu;
    int len = 0;
    if (argc < 2) {
        cpu.a = 200;
        cpu.b = 100;
        cpu.mem[0] = 0x10;   // ADD
        cpu.mem[1] = 0x00;   // HALT
        len = 2;
    }
    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("a=", 0) == 0) cpu.a = (std::uint8_t)parse_number(arg.substr(2));
            else if (arg.rfind("b=", 0) == 0) cpu.b = (std::uint8_t)parse_number(arg.substr(2));
            else cpu.mem[len++] = (std::uint8_t)parse_number("0x" + arg);
        }
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 07 [a=N] [b=N] <байти програми, напр. 10 00>\n";
        return 1;
    }

    std::cout << "старт                          ";
    regs(cpu);
    std::cout << "\n\n";
    for (int i = 0; i < 20 && !cpu.halted; ++i) {
        std::uint8_t op = cpu.mem[cpu.pc];
        std::cout << "mem[" << cpu.pc << "]=" << hex(op) << " " << bits(op) << " "
                  << std::left << std::setw(4) << name(op) << std::right << " → ";
        step(cpu);
        regs(cpu);
        std::cout << '\n';
    }
    std::cout << "\nще один step: ";
    step(cpu);
    std::cout << "PC лишився " << cpu.pc << '\n';
}
