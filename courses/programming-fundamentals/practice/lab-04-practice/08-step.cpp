// Дослід 8: процесор, який стрибає. step() — повний switch за опкодом, JMP/JZ/JNZ/CMP, ліміт кроків.
// Запуск: ./run.sh 08                          — зворотний відлік з ISA.uk.md §9: 3 2 1
//         ./run.sh 08 20 05 03 19 32 02 00 00  — те саме від 5
//         ./run.sh 08 30 00 00                 — JMP сам на себе: спрацює ліміт кроків
//         ./run.sh 08 20 05 77                 — невідомий опкод
// Байти програми й даних пишуться, як у дампі: шістнадцяткові, без 0x.
// Ще можна: a=N b=N  data=41,42 (покласти з 0x800)  limit=N (ліміт кроків)  trace=N (скільки рядків друкувати)
// Lab 04, Теорія §2–3, M1–M4 · ISA.uk.md §5, група 0x3_
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const std::uint16_t DATA_LO = 0x800;

struct Memory { Byte data[MEM_SIZE] = {}; };

struct Flags { bool z = false, n = false, c = false; };

struct CPU {
    Memory* mem = nullptr;
    std::uint16_t pc = 0;
    std::uint16_t h = 0;
    Byte a = 0, b = 0;
    Flags f;
    bool halted = false;
    std::string error;
    std::string out;
};

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

std::uint16_t rd16(CPU& cpu, std::size_t addr) {
    Byte lo = rd(cpu, addr);
    Byte hi = rd(cpu, addr + 1);
    return (std::uint16_t)(lo | (hi << 8));
}

int op_size(Byte op) {
    if (op == 0x20 || op == 0x21) return 2;
    if (op >= 0x22 && op <= 0x25) return 3;
    if (op == 0x28) return 3;
    if (op >= 0x30 && op <= 0x34) return 3;   // усі стрибки — опкод і адреса
    return 1;
}

std::string text(Byte op, Byte imm, std::uint16_t addr) {
    switch (op) {
    case 0x00: return "HALT";
    case 0x01: return "NOP";
    case 0x02: return "OUT";
    case 0x03: return "OUTN";
    case 0x10: return "ADD A, B";
    case 0x11: return "SUB A, B";
    case 0x12: return "AND A, B";
    case 0x13: return "OR A, B";
    case 0x14: return "XOR A, B";
    case 0x15: return "NOT A";
    case 0x16: return "SHL A";
    case 0x17: return "SHR A";
    case 0x18: return "INC A";
    case 0x19: return "DEC A";
    case 0x1A: return "CMP A, B";
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
    case 0x30: return "JMP " + hex16(addr);
    case 0x31: return "JZ " + hex16(addr);
    case 0x32: return "JNZ " + hex16(addr);
    case 0x33: return "JC " + hex16(addr);
    case 0x34: return "JNC " + hex16(addr);
    }
    return "???";
}

void set_zn(CPU& cpu, Byte r) {
    cpu.f.z = r == 0;
    cpu.f.n = (r >> 7) & 1;
}

// Повертає true, якщо стрибок спрацював (тільки для трасування).
bool step(CPU& cpu) {
    if (cpu.halted) return false;
    Byte op = rd(cpu, cpu.pc);
    int size = op_size(op);
    Byte imm = size >= 2 ? rd(cpu, cpu.pc + 1) : 0;
    std::uint16_t addr = size == 3 ? rd16(cpu, cpu.pc + 1) : 0;
    if (!cpu.error.empty()) { cpu.halted = true; return false; }

    bool jump = false;   // стрибок, що спрацював, сам ставить PC
    int wide = 0;
    switch (op) {
    case 0x00: cpu.halted = true; break;                                     // HALT
    case 0x01: break;                                                        // NOP
    case 0x02: cpu.out += (char)cpu.a; break;                                // OUT
    case 0x03: cpu.out += std::to_string(cpu.a) + " "; break;                // OUTN

    case 0x10: wide = cpu.a + cpu.b; cpu.f.c = wide > 0xFF; cpu.a = (Byte)wide; set_zn(cpu, cpu.a); break;
    case 0x11: cpu.f.c = cpu.a < cpu.b; cpu.a = (Byte)(cpu.a - cpu.b); set_zn(cpu, cpu.a); break;
    case 0x12: cpu.a &= cpu.b; cpu.f.c = false; set_zn(cpu, cpu.a); break;
    case 0x13: cpu.a |= cpu.b; cpu.f.c = false; set_zn(cpu, cpu.a); break;
    case 0x14: cpu.a ^= cpu.b; cpu.f.c = false; set_zn(cpu, cpu.a); break;
    case 0x15: cpu.a = (Byte)~cpu.a; cpu.f.c = false; set_zn(cpu, cpu.a); break;
    case 0x16: cpu.f.c = (cpu.a >> 7) & 1; cpu.a = (Byte)(cpu.a << 1); set_zn(cpu, cpu.a); break;
    case 0x17: cpu.f.c = cpu.a & 1; cpu.a = (Byte)(cpu.a >> 1); set_zn(cpu, cpu.a); break;
    case 0x18: cpu.a = (Byte)(cpu.a + 1); set_zn(cpu, cpu.a); break;         // INC: C не чіпає
    case 0x19: cpu.a = (Byte)(cpu.a - 1); set_zn(cpu, cpu.a); break;         // DEC: C не чіпає
    case 0x1A: cpu.f.c = cpu.a < cpu.b; set_zn(cpu, (Byte)(cpu.a - cpu.b)); break;   // CMP: A не змінюється

    case 0x20: cpu.a = imm; break;                                           // LOAD* прапорці не чіпають
    case 0x21: cpu.b = imm; break;
    case 0x22: cpu.a = rd(cpu, addr); break;
    case 0x23: cpu.b = rd(cpu, addr); break;
    case 0x24: wr(cpu, addr, cpu.a); break;
    case 0x25: wr(cpu, addr, cpu.b); break;
    case 0x26: cpu.a = cpu.b; break;
    case 0x27: cpu.b = cpu.a; break;
    case 0x28: cpu.h = addr; break;
    case 0x29: cpu.a = rd(cpu, cpu.h); break;
    case 0x2A: wr(cpu, cpu.h, cpu.a); break;
    case 0x2B: cpu.h = (std::uint16_t)(cpu.h + 1); break;
    case 0x2C: cpu.h = (std::uint16_t)(cpu.h - 1); break;
    case 0x2D: cpu.a = (Byte)(cpu.h & 0xFF); break;

    case 0x30: jump = true; break;                                           // JMP
    case 0x31: jump = cpu.f.z; break;                                        // JZ
    case 0x32: jump = !cpu.f.z; break;                                       // JNZ
    case 0x33: jump = cpu.f.c; break;                                        // JC  (opt)
    case 0x34: jump = !cpu.f.c; break;                                       // JNC (opt)

    default:
        cpu.error = "unknown opcode " + hex(op);
        break;
    }
    if (!cpu.error.empty()) { cpu.halted = true; return false; }

    if (jump) cpu.pc = addr;                         // і більше нічого не додаємо
    else cpu.pc = (std::uint16_t)(cpu.pc + size);
    return jump;
}

void regs(const CPU& cpu) {
    std::cout << "A=" << std::setw(3) << (int)cpu.a << " B=" << std::setw(3) << (int)cpu.b
              << " H=" << hex16(cpu.h) << " Z=" << cpu.f.z << " N=" << cpu.f.n << " C=" << cpu.f.c
              << " PC=" << hex16(cpu.pc);
}

std::string shown(const std::string& s) {
    std::string out;
    for (unsigned char c : s) {
        if (c >= 0x20 && c < 0x7F) out += (char)c;
        else out += "\\x" + hex2(c);
    }
    return out;
}

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

    std::vector<Byte> program, data;
    long limit = 100000, trace = 40;
    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("a=", 0) == 0) cpu.a = (Byte)parse_number(arg.substr(2));
            else if (arg.rfind("b=", 0) == 0) cpu.b = (Byte)parse_number(arg.substr(2));
            else if (arg.rfind("data=", 0) == 0) data = hex_list(arg.substr(5));
            else if (arg.rfind("limit=", 0) == 0) limit = parse_number(arg.substr(6));
            else if (arg.rfind("trace=", 0) == 0) trace = parse_number(arg.substr(6));
            else program.push_back((Byte)parse_number("0x" + arg));
        }
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 08 [a=N] [b=N] [data=41,42] [limit=N] [trace=N] <байти програми>\n";
        return 1;
    }
    if (program.empty())   // LOADI A, 3; loop: OUTN; DEC A; JNZ loop; HALT
        program = {0x20, 0x03, 0x03, 0x19, 0x32, 0x02, 0x00, 0x00};
    for (std::size_t i = 0; i < program.size() && i < DATA_LO; ++i) memory.data[i] = program[i];
    for (std::size_t i = 0; i < data.size() && DATA_LO + i < MEM_SIZE; ++i) memory.data[DATA_LO + i] = data[i];

    std::cout << "код з 0x0000:  ";
    for (Byte x : program) std::cout << hex2(x) << ' ';
    if (!data.empty()) {
        std::cout << "\nдані з 0x0800: ";
        for (Byte x : data) std::cout << hex2(x) << ' ';
    }
    std::cout << "\n\n      " << pad("старт", 35);
    regs(cpu);
    std::cout << '\n';

    auto peek = [&](std::size_t addr) -> Byte { return addr < MEM_SIZE ? memory.data[addr] : 0; };
    long steps = 0;
    // run: for (;;) з лімітом кроків — інакше зламаний JMP повісить процес.
    for (;;) {
        if (cpu.halted) break;
        if (steps >= limit) break;
        std::size_t at = cpu.pc;
        Byte op = peek(at);
        int size = op_size(op);
        std::string raw;
        for (int k = 0; k < size; ++k) raw += hex2(peek(at + k)) + " ";
        std::uint16_t addr = (std::uint16_t)(peek(at + 1) | (peek(at + 2) << 8));
        std::size_t printed = cpu.out.size();

        bool jumped = step(cpu);
        ++steps;
        if (steps <= trace) {
            std::cout << std::setw(4) << steps << "  " << hex16((std::uint16_t)at).substr(2) << "  "
                      << std::left << std::setw(10) << raw << std::setw(17) << text(op, peek(at + 1), addr)
                      << std::right << " → ";
            regs(cpu);
            if (jumped) std::cout << "  стрибок";
            if (cpu.out.size() > printed) std::cout << "  вивід: \"" << shown(cpu.out.substr(printed)) << '"';
            std::cout << '\n';
        } else if (steps == trace + 1) {
            std::cout << "   ... далі без трасування\n";
        }
    }

    std::cout << "\nкроків: " << steps << "\nвивід: \"" << shown(cpu.out) << "\"\nрегістри: ";
    regs(cpu);
    std::cout << '\n';
    if (!cpu.error.empty()) std::cout << "помилка: " << cpu.error << " на PC=" << hex16(cpu.pc) << '\n';
    else if (!cpu.halted) std::cout << "зупинено лімітом кроків (" << limit << "): HALT так і не настав\n";
}
