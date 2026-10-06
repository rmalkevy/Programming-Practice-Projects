// Дослід 5: 0.1 + 0.2 != 0.3. Більшість десяткових дробів у двійковий запис не влазять.
// Запуск: ./run.sh 05                  — 0.1 + 0.2 проти 0.3
//         ./run.sh 05 0.5 0.25 0.75    — дроби зі знаменником-степенем двійки: точно
// Lab 01, Теорія §3, M4.2 · Notes 01, §3
#include "common.hpp"
#include <cmath>

double parse_double(const std::string& s) {
    std::size_t used = 0;
    double v = std::stod(s, &used);
    if (used != s.size()) throw std::invalid_argument(s);
    return v;
}

int main(int argc, char* argv[]) {
    double a = 0.1, b = 0.2, c = 0.3;
    try {
        if (argc >= 4) {
            a = parse_double(argv[1]);
            b = parse_double(argv[2]);
            c = parse_double(argv[3]);
        }
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 05 [a b c]   наприклад: 0.1 0.2 0.3\n";
        return 1;
    }

    double sum = a + b;
    std::cout << "a + b                 = " << sum << "   ← cout за замовчуванням округлює до 6 цифр\n";
    std::cout << std::setprecision(17);
    std::cout << "a + b, 17 цифр        = " << sum << '\n';
    std::cout << "c, 17 цифр            = " << c << '\n';
    std::cout << std::boolalpha;
    std::cout << "a + b == c            → " << (sum == c) << '\n';
    std::cout << "|a + b - c| < 1e-9    → " << (std::fabs(sum - c) < 1e-9) << "   ← порівняння з допуском\n";

    // Додати a десять разів: помилка округлення накопичується.
    float fsum = 0;
    double dsum = 0;
    for (int i = 0; i < 10; ++i) {
        fsum += (float)a;
        dsum += a;
    }
    std::cout << "\na + a + ... + a, десять разів:\n";
    std::cout << "  float   " << fsum << '\n';
    std::cout << "  double  " << dsum << '\n';
    std::cout << "  10 * a  " << 10 * a << '\n';

    // Те саме в цілих «сотих»: копійки, пікселі, адреси — завжди цілі.
    long cents = std::lround(a * 100);
    std::cout << "\nу цілих сотих: " << cents << " · 10 = " << cents * 10 << " (точно)\n";
}
