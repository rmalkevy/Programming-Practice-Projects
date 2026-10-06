// Дослід 6: цілочисельне ділення відкидає дріб. Де int, де double — і в який бік перетворення.
// Запуск: ./run.sh 06 5 2
//         ./run.sh 06 -7 2
// Lab 01, Теорія §2 · Notes 01, §4
#include "common.hpp"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 06 <a> <b>   наприклад: 5 2\n";
        return 1;
    }
    int a = 0, b = 0;
    try {
        a = (int)parse_number(argv[1]);
        b = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (b == 0) {
        std::cout << "ділення на нуль — це дослід 01\n";
        return 1;
    }

    std::cout << "int a = " << a << ", int b = " << b << "\n\n";
    std::cout << "  a / b               = " << a / b << "     ← обидва int: дріб відкинуто (до нуля)\n";
    std::cout << "  a % b               = " << a % b << "     ← остача; знак як у a\n";
    std::cout << "  (a / b) * b + a % b = " << (a / b) * b + a % b << "     ← завжди дає a назад\n";
    std::cout << "  a / (double)b       = " << a / (double)b << "   ← один double: увесь вираз у double\n";
    std::cout << "  (double)(a / b)     = " << (double)(a / b) << "     ← пізно: дріб уже відкинули\n";
    std::cout << "  a / 2.0             = " << a / 2.0 << "   ← 2.0 — це double-літерал\n";
}
