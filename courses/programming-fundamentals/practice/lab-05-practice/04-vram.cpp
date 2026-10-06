// Дослід 4: екран — це 256 байтів пам'яті з 0xA00. Вісім байтів дампу — це один рядок пікселів.
// Запуск: ./run.sh 04 80                              — один байт 0x80 на 0xA00
//         ./run.sh 04 00 66 FF FF 7E 3C 18 00         — вісім байтів підряд: що з них вийде?
//         ./run.sh 04 stride=8 00 66 FF FF 7E 3C 18 00 — ті самі байти з кроком 8
// Байти пишуться, як у дампі: шістнадцяткові, без 0x. Ще можна: at=0xA10 (куди класти перший).
// Lab 05, Теорія §2 · Notes 05, «У проєкті ember» · ISA.uk.md §7
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;
const std::size_t MEM_SIZE = 4096;
const int VRAM_LO = 0xA00, VRAM_SIZE = 256, ROW_BYTES = 8;

struct Memory { Byte data[MEM_SIZE] = {}; };

// Рядок y відеопам'яті: вісім байтів, як у дампі, а поруч — ті самі байти пікселями.
// Пікселі рахуються формулою з даного show(): байт y * 8 + x / 8, біт 7 - x % 8.
void row(const Memory& mem, int y) {
    int start = VRAM_LO + y * ROW_BYTES;
    std::cout << hex16((std::uint16_t)start).substr(2) << " ";
    for (int i = 0; i < ROW_BYTES; ++i) std::cout << ' ' << hex2(mem.data[start + i]);
    std::cout << "   ";
    for (int x = 0; x < 64; ++x) {
        Byte cell = mem.data[VRAM_LO + y * 8 + (x / 8)];
        bool lit = (cell >> (7 - (x % 8))) & 1;
        std::cout << (lit ? '#' : '.');
        if (x % 8 == 7 && x != 63) std::cout << ' ';
    }
    std::cout << "  y=" << y << '\n';
}

int main(int argc, char* argv[]) {
    std::vector<Byte> bytes;
    long at = VRAM_LO, stride = 1;
    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg.rfind("at=", 0) == 0) at = parse_number(arg.substr(3));
            else if (arg.rfind("stride=", 0) == 0) stride = parse_number(arg.substr(7));
            else bytes.push_back((Byte)parse_number("0x" + arg));
        }
    } catch (const std::exception&) {
        bytes.clear();
    }
    if (bytes.empty() || stride < 1) {
        std::cout << "usage: ./run.sh 04 [at=0xA00] [stride=1] <байти>   наприклад: 80\n";
        return 1;
    }

    Memory mem;
    std::cout << "Пишемо з " << hex16((std::uint16_t)at) << " з кроком " << stride << ":\n";
    for (std::size_t i = 0; i < bytes.size(); ++i) {
        long addr = at + (long)i * stride;
        std::cout << "  mem[" << hex16((std::uint16_t)addr) << "] = " << hex2(bytes[i]);
        if (addr < 0 || addr >= (long)MEM_SIZE) { std::cout << "   — за межею пам'яті, пропущено\n"; continue; }
        mem.data[addr] = bytes[i];
        if (addr < VRAM_LO || addr >= VRAM_LO + VRAM_SIZE) std::cout << "   — не відеопам'ять";
        std::cout << '\n';
    }

    // Друкуємо рядки до останнього непорожнього: решта екрана — нулі.
    int last = 0;
    for (int i = 0; i < VRAM_SIZE; ++i)
        if (mem.data[VRAM_LO + i] != 0) last = i / ROW_BYTES;
    std::cout << "\nадр.  байти (дамп)                екран: біт 7 кожного байта — лівий піксель його вісімки\n";
    for (int y = 0; y <= last; ++y) row(mem, y);
    if (last < 31) std::cout << "... рядки " << last + 1 << "–31 порожні (там нулі)\n";
}
