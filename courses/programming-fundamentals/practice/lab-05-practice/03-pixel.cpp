// Дослід 3: піксель (x, y) — це один біт: адреса байта 0xA00 + y * 8 + x / 8, номер біта 7 - x % 8.
// Запуск: ./run.sh 03 0 0      — лівий верхній кут
//         ./run.sh 03 13 2     — який байт, який біт; і де був би піксель без «7 -»
//         ./run.sh 03 70 1     — за межами екрана: куди потрапила б формула без перевірки
// Lab 05, Теорія §2 · Notes 05, «Ідея» · ISA.uk.md §7
#include "common.hpp"

const int VRAM_LO = 0xA00, W = 64, H = 32, ROW_BYTES = W / 8;

// Вісім пікселів одного байта, як їх малює show(): біт 7 — найлівіший.
void strip(std::uint8_t cell, int first_x) {
    std::cout << "    x:";
    for (int i = 0; i < 8; ++i) std::cout << std::setw(3) << first_x + i;
    std::cout << "\n      ";
    for (int i = 0; i < 8; ++i) std::cout << "  " << (((cell >> (7 - i)) & 1) ? '#' : '.');
    std::cout << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 03 <x> <y>   наприклад: 13 2\n";
        return 1;
    }
    long x = 0, y = 0;
    try {
        x = parse_number(argv[1]);
        y = parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (x < 0 || y < 0) {
        std::cout << "x і y тут невід'ємні\n";
        return 1;
    }

    long addr = VRAM_LO + y * ROW_BYTES + x / 8;
    int bit = 7 - (int)(x % 8);
    std::uint8_t mask = (std::uint8_t)(1u << bit);

    std::cout << "(x, y) = (" << x << ", " << y << ")\n\n";
    std::cout << "  адреса байта = 0xA00 + y * 8 + x / 8 = 0xA00 + " << y * ROW_BYTES << " + " << x / 8
              << " = " << hex16((std::uint16_t)addr) << "  (" << addr << ")\n";
    std::cout << "  номер біта   = 7 - x % 8 = 7 - " << x % 8 << " = " << bit << '\n';
    std::cout << "  маска        = 1 << " << bit << " = " << bits(mask) << " = " << hex(mask) << "\n\n";

    bool on_screen = x < W && y < H;
    if (on_screen) {
        std::cout << "  Байт " << hex16((std::uint16_t)addr) << " — це пікселі x = " << x / 8 * 8 << ".."
                  << x / 8 * 8 + 7 << " рядка y = " << y << ". Якщо в ньому лише маска " << hex(mask) << ":\n";
        strip(mask, (int)(x / 8 * 8));

        // Якщо виставити біт x % 8, а show() читає біт 7 - x % 8, піксель «віддзеркалиться» у своїй вісімці.
        std::uint8_t wrong = (std::uint8_t)(1u << (x % 8));
        long seen = x / 8 * 8 + (7 - x % 8);
        std::cout << "\n  Без «7 -»: біт " << x % 8 << ", маска " << bits(wrong) << " — і show() засвітить x = "
                  << seen << ", а не " << x << ":\n";
        strip(wrong, (int)(x / 8 * 8));
        return 0;
    }

    std::cout << "  За межами екрана (64 × 32): PLOT виставляє C і нічого не змінює.\n";
    std::cout << "  Без перевірки меж формула все одно дала б адресу " << hex16((std::uint16_t)addr) << ":\n";
    if (addr >= VRAM_LO && addr < VRAM_LO + W * H / 8) {
        long off = addr - VRAM_LO;
        std::cout << "  це ще відеопам'ять — піксель (" << (off % ROW_BYTES) * 8 + (7 - bit) << ", "
                  << off / ROW_BYTES << "), зовсім інший.\n";
    } else if (addr < 4096) {
        std::cout << "  це вже не екран, а запас за ним (0xB00 і далі) — на екрані нічого не видно.\n";
    } else {
        std::cout << "  це взагалі за кінцем пам'яті (4096 байтів).\n";
    }
}
