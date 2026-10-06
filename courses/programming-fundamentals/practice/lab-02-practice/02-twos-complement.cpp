// Дослід 2: доповняльний код. Той самий байт — два числа; зміна знаку — це ~x + 1.
// Запуск: ./run.sh 02            — таблиця біля межі знаку
//         ./run.sh 02 5          — розібрати одне число (можна -5, 0xFF, 128 ...)
// Lab 02, Теорія §2 · Notes 02, §2
#include "common.hpp"

// Таблиця: ті самі вісім бітів, прочитані як uint8_t і як int8_t.
void table() {
    std::cout << "біти        uint8_t  int8_t\n";
    std::uint8_t rows[] = {0x00, 0x01, 0x7E, 0x7F, 0x80, 0x81, 0xFE, 0xFF};
    for (std::uint8_t x : rows) {
        std::cout << bits(x) << "   " << std::setw(5) << (int)x
                  << "   " << std::setw(5) << (int)(std::int8_t)x;
        if (x == 0x7F) std::cout << "   ← найбільше додатне int8_t";
        if (x == 0x80) std::cout << "   ← старший біт = 1: далі «від'ємні»";
        std::cout << '\n';
    }
}

void negate(long value) {
    std::uint8_t x = (std::uint8_t)value;
    std::uint8_t inv = (std::uint8_t)~x;       // перевернути всі біти
    std::uint8_t neg = (std::uint8_t)(inv + 1); // і додати одиницю

    std::cout << "  x        " << bits(x)   << "   як uint8_t " << std::setw(3) << (int)x
              << ",  як int8_t " << std::setw(4) << (int)(std::int8_t)x << '\n';
    std::cout << "  ~x       " << bits(inv) << '\n';
    std::cout << "  ~x + 1   " << bits(neg) << "   як uint8_t " << std::setw(3) << (int)neg
              << ",  як int8_t " << std::setw(4) << (int)(std::int8_t)neg << '\n';

    // Пастка: перед ~ байт непомітно стає int (32 біти), і ~ перевертає всі 32.
    std::cout << "\n  (int)(~x)          = " << (int)(~x) << "    ← x став int ще до ~\n";
    std::cout << "  (uint8_t)(~x)      = " << (int)(std::uint8_t)(~x) << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        table();
        return 0;
    }
    try {
        negate(parse_number(argv[1]));
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число: " << argv[1] << '\n';
        return 1;
    }
}
