// Дослід 9: процесор зі стеком. PUSH/POP, CALL/RET і MUL; SP стартує з 0xFFF; переповнення — помилка машини.
// Запуск: ./run.sh 09                              — fact(5) з ISA.uk.md §6: 120, 60 кроків, SP знову 0xFFF
//         ./run.sh 09 a=0                          — fact(0); a=N міняє аргумент (байт 05 у 20 05)
//         ./run.sh 09 54 04 00 00 02 55 a=0x41     — CALL printA / HALT / printA: OUT / RET
//         ./run.sh 09 55                           — RET без CALL: спустошення стека
//         ./run.sh 09 set=0A:01,01,01 set=10:01,01,01 trace=10   — fact без бази: переповнення
// Байти програми й даних пишуться, як у дампі: шістнадцяткові, без 0x.
// a=N: без байтів програми — аргумент fact; з байтами — просто початкове A.
// Ще можна: b=N  data=41,42 (покласти з 0x800)  set=0A:01,01 (покласти байти з адреси 0x0A)
//           limit=N (ліміт кроків)  trace=N (скільки рядків друкувати)  top=N (скільки байтів стека показувати)
// Lab 07, Теорія §1, §3, M1–M3 · ISA.uk.md §5, група 0x5_, і §6
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const std::uint16_t DATA_LO = 0x800;
const std::uint16_t STACK_LO = 0xF00, STACK_HI = 0xFFF;

struct Memory { Byte data[MEM_SIZE] = {}; };

struct Flags { bool z = false, n = false, c = false; };

struct CPU {
    Memory* mem = nullptr;
    std::uint16_t pc = 0;
    std::uint16_t sp = STACK_HI;   // порожній спадний: SP вказує на вільний байт
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

// Стек: спершу перевірка, потім запис. Не вийшло — помилка машини, а не падіння процесу.
bool push(CPU& cpu, Byte v) {
    if (cpu.sp < STACK_LO) {
        cpu.error = "переповнення стека (SP = " + hex16(cpu.sp) + ", нижче за STACK_LO)";
        return false;
    }
    wr(cpu, cpu.sp, v);                // mem[SP] = v
    cpu.sp = (std::uint16_t)(cpu.sp - 1);
    return true;
}

bool pop(CPU& cpu, Byte& v) {
    if (cpu.sp >= STACK_HI) {
        cpu.error = "спустошення стека (SP = " + hex16(cpu.sp) + ", знімати нічого)";
        return false;
    }
    cpu.sp = (std::uint16_t)(cpu.sp + 1);
    v = rd(cpu, cpu.sp);               // SP + 1, потім читаємо
    return true;
}

int op_size(Byte op) {
    if (op == 0x20 || op == 0x21) return 2;
    if (op >= 0x22 && op <= 0x25) return 3;
    if (op == 0x28) return 3;
    if (op >= 0x30 && op <= 0x34) return 3;   // усі стрибки — опкод і адреса
    if (op == 0x54) return 3;                 // CALL — теж
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
    case 0x1B: return "MUL A, B";
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
    case 0x50: return "PUSH A";
    case 0x51: return "POP A";
    case 0x52: return "PUSH B";
    case 0x53: return "POP B";
    case 0x54: return "CALL " + hex16(addr);
    case 0x55: return "RET";
    case 0x56: return "PUSH H";
    case 0x57: return "POP H";
    }
    return "???";
}

void set_zn(CPU& cpu, Byte r) {
    cpu.f.z = r == 0;
    cpu.f.n = (r >> 7) & 1;
}

// Повертає true, якщо PC поставила сама інструкція (стрибок, CALL, RET) — тільки для трасування.
bool step(CPU& cpu) {
    if (cpu.halted) return false;
    Byte op = rd(cpu, cpu.pc);
    int size = op_size(op);
    Byte imm = size >= 2 ? rd(cpu, cpu.pc + 1) : 0;
    std::uint16_t addr = size == 3 ? rd16(cpu, cpu.pc + 1) : 0;
    if (!cpu.error.empty()) { cpu.halted = true; return false; }

    bool jump = false;   // стрибок, що спрацював, сам ставить PC
    std::uint16_t target = addr;
    int wide = 0;
    Byte hi = 0, lo = 0;
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
    case 0x1B: wide = cpu.a * cpu.b; cpu.f.c = wide > 0xFF; cpu.a = (Byte)wide; set_zn(cpu, cpu.a); break;  // MUL

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

    case 0x50: push(cpu, cpu.a); break;                                      // PUSH A
    case 0x51: pop(cpu, cpu.a); break;                                       // POP A
    case 0x52: push(cpu, cpu.b); break;                                      // PUSH B
    case 0x53: pop(cpu, cpu.b); break;                                       // POP B
    case 0x54: {                                                             // CALL
        std::uint16_t ret = (std::uint16_t)(cpu.pc + 3);                     // адреса ПІСЛЯ CALL
        if (push(cpu, (Byte)(ret & 0xFF)) && push(cpu, (Byte)(ret >> 8)))   // молодший, потім старший
            jump = true;
        break;
    }
    case 0x55:                                                               // RET
        if (pop(cpu, hi) && pop(cpu, lo)) {                                  // старший, потім молодший
            target = (std::uint16_t)((hi << 8) | lo);
            jump = true;
        }
        break;
    case 0x56:                                                               // PUSH H (opt)
        if (push(cpu, (Byte)(cpu.h & 0xFF))) push(cpu, (Byte)(cpu.h >> 8));
        break;
    case 0x57:                                                               // POP H (opt)
        if (pop(cpu, hi) && pop(cpu, lo)) cpu.h = (std::uint16_t)((hi << 8) | lo);
        break;

    default:
        cpu.error = "unknown opcode " + hex(op);
        break;
    }
    if (!cpu.error.empty()) { cpu.halted = true; return false; }

    if (jump) cpu.pc = target;                       // і більше нічого не додаємо
    else cpu.pc = (std::uint16_t)(cpu.pc + size);
    return jump;
}

void regs(const CPU& cpu) {
    std::cout << "A=" << std::setw(3) << (int)cpu.a << " B=" << std::setw(3) << (int)cpu.b
              << " H=" << hex16(cpu.h) << " Z=" << cpu.f.z << " N=" << cpu.f.n << " C=" << cpu.f.c
              << " PC=" << hex16(cpu.pc) << " SP=" << hex16(cpu.sp);
}

// Вершина стека: зайняті байти від SP + 1 до 0xFFF, верхній першим. Адресу повернення
// видно як два байти поспіль: старший, молодший — так, як її читатиме RET.
std::string stack_top(const CPU& cpu, long top) {
    std::string out;
    long shown = 0;
    for (std::size_t at = (std::size_t)cpu.sp + 1; at <= STACK_HI && at < MEM_SIZE; ++at) {
        if (shown == top) { out += " …"; break; }
        out += (shown ? " " : "") + hex2(cpu.mem->data[at]);
        ++shown;
    }
    return out.empty() ? "—" : out;
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

struct Patch { std::size_t at; std::vector<Byte> bytes; };

int main(int argc, char* argv[]) {
    Memory memory;
    CPU cpu;
    cpu.mem = &memory;

    std::vector<Byte> program, data;
    std::vector<Patch> patches;
    long limit = 100000, trace = 80, top = 6, a = -1;
    bool bad = false;
    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("a=", 0) == 0) a = parse_number(arg.substr(2)) & 0xFF;
            else if (arg.rfind("b=", 0) == 0) cpu.b = (Byte)parse_number(arg.substr(2));
            else if (arg.rfind("data=", 0) == 0) data = hex_list(arg.substr(5));
            else if (arg.rfind("set=", 0) == 0) {
                std::size_t colon = arg.find(':');
                if (colon == std::string::npos) throw std::invalid_argument(arg);
                patches.push_back({(std::size_t)parse_number("0x" + arg.substr(4, colon - 4)),
                                   hex_list(arg.substr(colon + 1))});
            }
            else if (arg.rfind("limit=", 0) == 0) limit = parse_number(arg.substr(6));
            else if (arg.rfind("trace=", 0) == 0) trace = parse_number(arg.substr(6));
            else if (arg.rfind("top=", 0) == 0) top = parse_number(arg.substr(4));
            else program.push_back((Byte)parse_number("0x" + arg));
        }
    } catch (const std::exception&) {
        bad = true;
    }
    if (bad || top < 0) {
        std::cout << "usage: ./run.sh 09 [a=N] [b=N] [data=41,42] [set=0A:01,01] [limit=N] [trace=N] [top=N] <байти програми>\n";
        return 1;
    }
    if (program.empty()) {
        // fact(n) з ISA.uk.md §6, тридцять байтів. Аргумент — другий байт (LOADI A, n).
        program = {0x20, 0x05, 0x54, 0x07, 0x00, 0x03, 0x00,
                   0x21, 0x00, 0x1A, 0x31, 0x1B, 0x00, 0x21, 0x01, 0x1A, 0x31, 0x1B, 0x00,
                   0x50, 0x19, 0x54, 0x07, 0x00, 0x53, 0x1B, 0x55, 0x20, 0x01, 0x55};
        if (a >= 0) program[1] = (Byte)a;
    } else if (a >= 0) {
        cpu.a = (Byte)a;   // своя програма: a=N — просто початкове A
    }
    for (std::size_t i = 0; i < program.size() && i < DATA_LO; ++i) memory.data[i] = program[i];
    for (std::size_t i = 0; i < data.size() && DATA_LO + i < MEM_SIZE; ++i) memory.data[DATA_LO + i] = data[i];
    for (const Patch& p : patches)
        for (std::size_t i = 0; i < p.bytes.size() && p.at + i < MEM_SIZE; ++i) memory.data[p.at + i] = p.bytes[i];

    std::cout << "код з 0x0000:  ";
    for (std::size_t i = 0; i < program.size(); ++i) std::cout << hex2(memory.data[i]) << ' ';
    if (!data.empty()) {
        std::cout << "\nдані з 0x0800: ";
        for (Byte x : data) std::cout << hex2(x) << ' ';
    }
    std::cout << "\n\n      " << pad("старт", 33);
    regs(cpu);
    std::cout << "  стек: " << stack_top(cpu, top) << '\n';

    auto peek = [&](std::size_t addr) -> Byte { return addr < MEM_SIZE ? memory.data[addr] : 0; };
    long steps = 0;
    std::uint16_t deepest = cpu.sp;
    // run: for (;;) з лімітом кроків — інакше зламаний JMP чи RET повісить процес.
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
        if (cpu.sp < deepest) deepest = cpu.sp;
        if (steps <= trace) {
            std::string what = at < MEM_SIZE ? text(op, peek(at + 1), addr) : "(поза пам'яттю)";
            if (at >= MEM_SIZE) raw = "-- ";
            std::cout << std::setw(4) << steps << "  " << hex16((std::uint16_t)at).substr(2) << "  "
                      << std::left << std::setw(10) << raw << pad(what, 17)
                      << std::right << " → ";
            regs(cpu);
            std::string note;
            if (jumped) note = op == 0x54 ? "виклик" : op == 0x55 ? "повернення" : "стрибок";
            if (cpu.out.size() > printed) note += "вивід: \"" + shown(cpu.out.substr(printed)) + '"';
            std::string st = stack_top(cpu, top);
            std::cout << "  стек: " << (note.empty() ? st : pad(st, (std::size_t)(3 * top + 2)) + note) << '\n';
        } else if (steps == trace + 1) {
            std::cout << "   ... далі без трасування\n";
        }
    }

    std::cout << "\nкроків: " << steps << "\nвивід: \"" << shown(cpu.out) << "\"\nрегістри: ";
    regs(cpu);
    std::cout << "\nстек: " << (cpu.sp == STACK_HI ? "порожній" : stack_top(cpu, top))
              << "  (найглибше SP = " << hex16(deepest) << ", байтів на стеку: " << STACK_HI - deepest << ")\n";
    if (!cpu.error.empty()) std::cout << "помилка: " << cpu.error << " на PC=" << hex16(cpu.pc) << '\n';
    else if (!cpu.halted) std::cout << "зупинено лімітом кроків (" << limit << "): HALT так і не настав\n";
}
