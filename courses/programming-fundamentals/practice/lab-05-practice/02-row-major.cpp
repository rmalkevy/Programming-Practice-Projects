// Дослід 2: двовимірної пам'яті немає. m[r][c] — це комірка номер r * 4 + c в одному ряду.
// Запуск: ./run.sh 02 1 2     — m[1][2] і flat[1 * 4 + 2]: та сама адреса
//         ./run.sh 02 0 5     — колонка за кінцем рядка
// Lab 05, Теорія §2 · Notes 05, §2
#include "common.hpp"

const int ROWS = 3, COLS = 4;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 02 <рядок> <колонка>   наприклад: 1 2\n";
        return 1;
    }
    long r = 0, c = 0;
    try {
        r = parse_number(argv[1]);
        c = parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    // Значення — це «рядок і колонка» десятковими цифрами: m[1][2] = 12.
    int m[ROWS][COLS] = {{0, 1, 2, 3}, {10, 11, 12, 13}, {20, 21, 22, 23}};
    const int* flat = &m[0][0];

    std::cout << "int m[3][4] — як таблиця:\n";
    for (int y = 0; y < ROWS; ++y) {
        std::cout << "  ";
        for (int x = 0; x < COLS; ++x) std::cout << std::setw(4) << m[y][x];
        std::cout << '\n';
    }
    std::cout << "\nі як пам'ять (flat[k], у дужках — зсув у байтах):";
    for (int k = 0; k < ROWS * COLS; ++k) {
        if (k % COLS == 0) std::cout << "\n  ";
        std::cout << "[" << k << "]=" << flat[k] << " (" << k * (int)sizeof(int) << ")  ";
    }
    std::cout << '\n';

    std::cout << "\nОбхід «рядки зовні» — зсуви в байтах: ";
    for (int y = 0; y < ROWS; ++y)
        for (int x = 0; x < COLS; ++x) std::cout << (&m[y][x] - flat) * (int)sizeof(int) << ' ';
    std::cout << "\nОбхід «колонки зовні» — зсуви в байтах: ";
    for (int x = 0; x < COLS; ++x)
        for (int y = 0; y < ROWS; ++y) std::cout << (&m[y][x] - flat) * (int)sizeof(int) << ' ';
    std::cout << "\n\n";

    long k = r * COLS + c;
    std::cout << "r = " << r << ", c = " << c << ":\n";
    std::cout << "  k = r * 4 + c = " << k << '\n';
    if (k >= 0 && k < ROWS * COLS)
        std::cout << "  flat[k]   = " << flat[k] << "   адреса " << (const void*)(flat + k) << '\n';
    else
        std::cout << "  flat[k]   — поза всіма 12 комірками\n";
    long swapped = c * ROWS + r;   // так рахують, якщо переплутати, що лежить поруч
    if (swapped >= 0 && swapped < ROWS * COLS)
        std::cout << "  c * 3 + r = " << swapped << ", flat[" << swapped << "] = " << flat[swapped]
                  << "   (переплутана формула)\n";
    const int* p = &m[r][c];
    std::cout << "  m[r][c]   = " << *p << "   адреса " << (const void*)p << '\n';
}
