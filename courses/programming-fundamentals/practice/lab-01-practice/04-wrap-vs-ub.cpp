// Дослід 4: беззнакове загортання визначене, знакове переповнення — UB.
// Запуск: ./run.sh 04            — байт від 253 вгору, int від INT_MAX - 2 вгору
//         ./run.sh 04 2 -1       — байт від 2 вниз, int від INT_MIN + 2 вниз
// Lab 01, Теорія §3, M4.1 · Notes 01, §2
#include "common.hpp"
#include <climits>

// Задумано: «x + 1 більше за x?» Для int це правда, поки немає переповнення, —
// і компілятор має право вважати, що переповнення не буває.
bool bigger(int x) { return x + 1 > x; }

int main(int argc, char* argv[]) {
    long start = 253, step = 1;
    try {
        if (argc >= 2) start = parse_number(argv[1]);
        if (argc >= 3) step = parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 04 [початок байта] [крок: 1 або -1]\n";
        return 1;
    }
    if (step != 1 && step != -1) {
        std::cout << "крок — 1 або -1\n";
        return 1;
    }

    std::uint8_t u = (std::uint8_t)start;
    std::cout << "std::uint8_t, крок " << step << ":\n  ";
    for (int i = 0; i < 6; ++i) {
        std::cout << (int)u << "  ";
        u = (std::uint8_t)(u + step);   // за модулем 256 — мова це обіцяє
    }

    int s = step > 0 ? INT_MAX - 2 : INT_MIN + 2;
    std::cout << "\n\nint, крок " << step << ":\n";
    for (int i = 0; i < 4; ++i) {
        std::cout << "  " << s << std::endl;
        s = s + (int)step;              // на третьому кроці — переповнення: UB
    }

    std::cout << "\nbigger(INT_MAX) = " << bigger(INT_MAX) << "   (INT_MAX + 1 > INT_MAX ?)\n";
}
