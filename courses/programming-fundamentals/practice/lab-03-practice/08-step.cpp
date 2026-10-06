// Дослід 8: процесор, який дістає до пам'яті. LOAD/STORE, безпосередні операнди й регістр H.
// Запуск: ./run.sh 08                          — сценарій із CHECKS.md: за 0x800 лежить 41 42 00, вивід AB
//         ./run.sh 08 data=48,49               — той самий код, інші дані
//         ./run.sh 08 22 00 08 02 00           — LOAD A, [0x0800]; OUT; HALT — адреса вшита в інструкцію
//         ./run.sh 08 28 FF 0F 29 2B 29 00     — H доходить до кінця пам'яті
// Байти програми й даних пишуться, як у дампі: шістнадцяткові, без 0x.
// Lab 03, Теорія §5–6, M2–M4 · ISA.uk.md §5, група 0x2_
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const std::uint16_t DATA_LO = 0x800;

struct Memory { Byte data[MEM_SIZE] = {}; };

struct Flags { bool z = false, n = false, c = false; };

struct CPU {
    Memory* mem = nullptr;   // вказівник хоста на всю коробку
    std::uint16_t pc = 0;    // адреси гостя — просто числа
    std::uint16_t h = 0;
    Byte a = 0, b = 0;
    Flags f;
    bool halted = false;
    std::string error;
    std::string out;         // що надрукували OUT і OUTN
};

// Читання й запис з перевіркою меж: адреса за кінцем — помилка, а не загортання.
Byte rd(CPU& cpu, std::size_t addr) {
    if (addr >= MEM_SIZE) {
        if (cpu.error.empty()) cpu.error = "читання за межею пам'яті, адреса " + hex16((std::uint16_t)addr);
        return 0;
    }
    return cpu.mem->data[addr];
}

void wr(CPU& cpu, std::size_t addr, Byte v) {
    if (addr >= MEM_SIZE) {
        if (cpu.error.empty()) cpu.error = "запис за межею пам'яті, адреса " + hex16((std::uint16_t)addr);
        return;
    }
    cpu.mem->data[addr] = v;
}

// Два байти, молодший перший (ISA.uk.md §4).
std::uint16_t rd16(CPU& cpu, std::size_t addr) {
    Byte lo = rd(cpu, addr);
    Byte hi = rd(cpu, addr + 1);
    return (std::uint16_t)(lo | (hi << 8));
}

// Розмір інструкції з таблиці ISA — рівно на стільки рухається PC.
int op_size(Byte op) {
    if (op == 0x20 || op == 0x21) return 2;
    if (op >= 0x22 && op <= 0x25) return 3;
    if (op == 0x28) return 3;
    return 1;
}

std::string text(Byte op, Byte imm, std::uint16_t addr) {
    const char* ctrl[] = {"HALT", "NOP", "OUT", "OUTN"};
    const char* alu[] = {"ADD A, B", "SUB A, B", "AND A, B", "OR A, B", "XOR A, B",
                         "NOT A", "SHL A", "SHR A", "INC A", "DEC A"};
    switch (op) {
    case 0x20: return "LOADI A, " + hex(imm);
    case 0x21: return "LOADI B, " + hex(imm);
    case 0x22: return "LOAD A, [" + hex16(addr) + "]";
    case 0x23: return "LOAD B, [" + hex16(addr) + "]";
    case 0x24: return "STORE [" + hex16(addr) + "], A";
    case 0x25: return "STORE [" + hex16(addr) + "], B";
    case 0x26: return "MOV A, B";
    case 0x27: return "MOV B, A";
    case 0x28: return "LOADH H, " + hex16(addr);
    case 0x29: return "LOAD A, [H]";
    case 0x2A: return "STORE [H], A";
    case 0x2B: return "INCH";
    case 0x2C: return "DECH";
    case 0x2D: return "HLOW";
    }
    if (op <= 0x03) return ctrl[op];
    if (op >= 0x10 && op <= 0x19) return alu[op - 0x10];
    return "???";
}

void set_zn(CPU& cpu) {
    cpu.f.z = cpu.a == 0;
    cpu.f.n = (cpu.a >> 7) & 1;
}

// Група 0x1_ — без змін з Lab 2.
void alu(CPU& cpu, int index) {
    int wide = 0;
    switch (index) {
    case 0x0: wide = cpu.a + cpu.b; cpu.f.c = wide > 0xFF; cpu.a = (Byte)wide; break;
    case 0x1: cpu.f.c = cpu.a < cpu.b; cpu.a = (Byte)(cpu.a - cpu.b); break;
    case 0x2: cpu.a &= cpu.b; cpu.f.c = false; break;
    case 0x3: cpu.a |= cpu.b; cpu.f.c = false; break;
    case 0x4: cpu.a ^= cpu.b; cpu.f.c = false; break;
    case 0x5: cpu.a = (Byte)~cpu.a; cpu.f.c = false; break;
    case 0x6: cpu.f.c = (cpu.a >> 7) & 1; cpu.a = (Byte)(cpu.a << 1); break;
    case 0x7: cpu.f.c = cpu.a & 1; cpu.a = (Byte)(cpu.a >> 1); break;
    case 0x8: cpu.a = (Byte)(cpu.a + 1); break;
    case 0x9: cpu.a = (Byte)(cpu.a - 1); break;
    default: return;
    }
    set_zn(cpu);
}

// Група 0x2_: пересилання. Жодна з цих інструкцій не чіпає прапорці.
void move(CPU& cpu, int index, Byte imm, std::uint16_t addr) {
    switch (index) {
    case 0x0: cpu.a = imm; break;                          // LOADI A, imm8
    case 0x1: cpu.b = imm; break;                          // LOADI B, imm8
    case 0x2: cpu.a = rd(cpu, addr); break;                // LOAD A, [addr16]
    case 0x3: cpu.b = rd(cpu, addr); break;                // LOAD B, [addr16]
    case 0x4: wr(cpu, addr, cpu.a); break;                 // STORE [addr16], A
    case 0x5: wr(cpu, addr, cpu.b); break;                 // STORE [addr16], B
    case 0x6: cpu.a = cpu.b; break;                        // MOV A, B
    case 0x7: cpu.b = cpu.a; break;                        // MOV B, A
    case 0x8: cpu.h = addr; break;                         // LOADH H, imm16
    case 0x9: cpu.a = rd(cpu, cpu.h); break;               // LOAD A, [H]   — *p
    case 0xA: wr(cpu, cpu.h, cpu.a); break;                // STORE [H], A  — *p = a
    case 0xB: cpu.h = (std::uint16_t)(cpu.h + 1); break;   // INCH          — ++p
    case 0xC: cpu.h = (std::uint16_t)(cpu.h - 1); break;   // DECH          — --p
    case 0xD: cpu.a = (Byte)(cpu.h & 0xFF); break;         // HLOW (opt)
    default: break;
    }
}

void step(CPU& cpu) {
    if (cpu.halted) return;
    Byte op = rd(cpu, cpu.pc);
    int size = op_size(op);
    Byte imm = size >= 2 ? rd(cpu, cpu.pc + 1) : 0;               // наступний байт після опкода
    std::uint16_t addr = size == 3 ? rd16(cpu, cpu.pc + 1) : 0;   // або два наступні
    if (!cpu.error.empty()) { cpu.halted = true; return; }

    int group = (op >> 4) & 0x0F, index = op & 0x0F;
    switch (group) {
    case 0x0:
        if (index == 0) cpu.halted = true;                                   // HALT
        if (index == 2) cpu.out += (char)cpu.a;                              // OUT
        if (index == 3) cpu.out += std::to_string(cpu.a) + " ";              // OUTN
        break;
    case 0x1: alu(cpu, index); break;
    case 0x2: move(cpu, index, imm, addr); break;
    default: break;   // поки що як NOP; у Lab 4 це стане помилкою
    }
    if (!cpu.error.empty()) { cpu.halted = true; return; }   // PC лишається на інструкції, що впала
    cpu.pc = (std::uint16_t)(cpu.pc + size);                  // розмір із таблиці, а не на око
}

void regs(const CPU& cpu) {
    std::cout << "A=" << std::setw(3) << (int)cpu.a << " B=" << std::setw(3) << (int)cpu.b
              << " H=" << hex16(cpu.h) << " Z=" << cpu.f.z << " N=" << cpu.f.n << " C=" << cpu.f.c
              << " PC=" << hex16(cpu.pc);
}

// Невидимі символи показати як \x00, щоб у виводі було видно, що OUT таки щось надрукував.
std::string shown(const std::string& s) {
    std::string out;
    for (unsigned char c : s) {
        if (c >= 0x20 && c < 0x7F) out += (char)c;
        else out += "\\x" + hex2(c);
    }
    return out;
}

// "41,42,00" → {0x41, 0x42, 0x00}
std::vector<Byte> hex_list(const std::string& s) {
    std::vector<Byte> out;
    std::stringstream in(s);
    std::string item;
    while (std::getline(in, item, ',')) out.push_back((Byte)parse_number("0x" + item));
    return out;
}

int main(int argc, char* argv[]) {
    Memory memory;
    CPU cpu;
    cpu.mem = &memory;

    std::vector<Byte> program, data = {0x41, 0x42, 0x00};
    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("a=", 0) == 0) cpu.a = (Byte)parse_number(arg.substr(2));
            else if (arg.rfind("b=", 0) == 0) cpu.b = (Byte)parse_number(arg.substr(2));
            else if (arg.rfind("data=", 0) == 0) data = hex_list(arg.substr(5));
            else program.push_back((Byte)parse_number("0x" + arg));
        }
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 08 [a=N] [b=N] [data=41,42,00] <байти програми, напр. 22 00 08 02 00>\n";
        return 1;
    }
    if (program.empty())   // LOADH H, 0x0800; LOAD A, [H]; OUT; INCH; LOAD A, [H]; OUT; HALT
        program = {0x28, 0x00, 0x08, 0x29, 0x02, 0x2B, 0x29, 0x02, 0x00};
    for (std::size_t i = 0; i < program.size() && i < DATA_LO; ++i) memory.data[i] = program[i];
    for (std::size_t i = 0; i < data.size() && DATA_LO + i < MEM_SIZE; ++i) memory.data[DATA_LO + i] = data[i];

    std::cout << "код з 0x0000:  ";
    for (Byte x : program) std::cout << hex2(x) << ' ';
    std::cout << "\nдані з 0x0800: ";
    for (Byte x : data) std::cout << hex2(x) << ' ';
    std::cout << "\n\n" << pad("старт", 41);
    regs(cpu);
    std::cout << '\n';

    // Для трасування: байти інструкції до step(), за кінцем пам'яті — нулі.
    auto peek = [&](std::size_t addr) -> Byte { return addr < MEM_SIZE ? memory.data[addr] : 0; };
    for (int i = 0; i < 100 && !cpu.halted; ++i) {
        std::size_t at = cpu.pc;
        Byte op = peek(at);
        int size = op_size(op);
        std::string raw;
        for (int k = 0; k < size; ++k) raw += hex2(peek(at + k)) + " ";
        Byte imm = peek(at + 1);
        std::uint16_t addr = (std::uint16_t)(peek(at + 1) | (peek(at + 2) << 8));
        std::size_t printed = cpu.out.size();

        step(cpu);
        std::cout << hex16((std::uint16_t)at).substr(2) << "  " << std::left << std::setw(10) << raw
                  << std::setw(22) << text(op, imm, addr) << std::right << " → ";
        regs(cpu);
        if (cpu.out.size() > printed) std::cout << "  вивід: \"" << shown(cpu.out.substr(printed)) << '"';
        std::cout << '\n';
    }

    std::cout << "\nвивід: \"" << shown(cpu.out) << "\"\n";
    if (!cpu.error.empty()) std::cout << "помилка: " << cpu.error << " (PC=" << hex16(cpu.pc) << ")\n";

    // Дві адреси однієї комірки: так її бачить гість і так її бачить ваш C++.
    if (cpu.h < MEM_SIZE) {
        std::cout << "\nH              = " << hex16(cpu.h)
                  << "         адреса гостя: однакова на кожному запуску\n";
        std::cout << "&mem->data[H]  = " << (void*)&cpu.mem->data[cpu.h]
                  << "   адреса хоста: запустіть ще раз — буде інше число\n";
    }
}
