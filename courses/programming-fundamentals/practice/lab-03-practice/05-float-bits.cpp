// Дослід 5: байти float. Перетворення (int)f і погляд на біти через memcpy — різні речі.
// Запуск: ./run.sh 05 1.0
//         ./run.sh 05 1 0.1 -2 0.5
// Lab 03, Теорія §3 · Notes 03, §3
#include "common.hpp"
#include <cstring>

void show(float f) {
    std::uint32_t u;
    std::memcpy(&u, &f, sizeof(u));   // визначений спосіб; *(std::uint32_t*)&f — UB

    std::uint8_t b[4];
    std::memcpy(b, &f, sizeof(b));

    unsigned sign = u >> 31;
    unsigned exponent = (u >> 23) & 0xFF;   // маска і зсув із Lab 2
    unsigned mantissa = u & 0x7FFFFF;

    std::cout << std::setprecision(9) << f << '\n';
    std::cout << "  (int)f                   = " << (long long)f << "   ← перетворення: значення без дробової частини\n";
    std::cout << "  біти як uint32_t         = " << u << "   ← ті самі 32 біти, прочитані як ціле\n";
    std::cout << "  шістнадцятковий          = 0x" << std::hex << std::uppercase << std::setw(8)
              << std::setfill('0') << u << std::dec << std::setfill(' ') << '\n';
    std::cout << "  знак | порядок | мантиса = " << sign << " | ";
    for (int i = 7; i >= 0; --i) std::cout << ((exponent >> i) & 1);
    std::cout << " | ";
    for (int i = 22; i >= 0; --i) std::cout << ((mantissa >> i) & 1);
    std::cout << "\n  порядок                  = " << exponent << " - 127 = " << (int)exponent - 127 << '\n';
    std::cout << "  байти в пам'яті          = ";
    for (std::uint8_t x : b) std::cout << hex2(x) << ' ';
    std::cout << "  ← молодший уперед, як у досліді 04\n\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <дробове число> [ще ...]   наприклад: 1.0 0.1 -2\n";
        return 1;
    }
    for (int i = 1; i < argc; ++i) {
        try {
            std::size_t used = 0;
            float f = std::stof(argv[i], &used);
            if (used != std::string(argv[i]).size()) throw std::invalid_argument(argv[i]);
            show(f);
        } catch (const std::exception&) {
            std::cout << argv[i] << "\n  не можу прочитати як число\n\n";
        }
    }
}
