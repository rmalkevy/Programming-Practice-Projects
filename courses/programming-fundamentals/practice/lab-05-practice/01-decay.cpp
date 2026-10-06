// Дослід 1: масив — це комірки поспіль і правило «i-й лежить через i кроків». У функції розмір губиться.
// Запуск: ./run.sh 01 3     — buf[3] і *(buf + 3): та сама комірка
//         ./run.sh 01 8     — на один за кінцем: звіт санітайзерів
// Lab 05, Теорія §1 · Notes 05, §1
#include "common.hpp"

using Byte = std::uint8_t;

// Можна написати `const int p[]` чи навіть `const int p[3]` — це все одно `const int* p`:
// масив у параметрі зводиться до вказівника. Тому кількість передають окремо.
void inside(const int* p, std::size_t count) {
    std::cout << "  inside(ints, 3): sizeof(p) = " << sizeof(p) << ", а count = " << count
              << " — лише тому, що його передали окремо\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 01 <i>   наприклад: 3\n";
        return 1;
    }
    long i = 0;
    try {
        i = parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    Byte buf[8] = {1, 2, 3};   // решта занулена
    int ints[3] = {10, 20, 30};

    std::cout << "Byte buf[8] = {1, 2, 3};\n  ";
    for (int k = 0; k < 8; ++k) std::cout << "buf[" << k << "]=" << (int)buf[k] << "  ";
    std::cout << "\n\n";

    std::cout << "  sizeof(buf)      = " << sizeof(buf) << "   (8 комірок по 1 байту; що це й розмір вказівника — збіг)\n";
    std::cout << "  sizeof(ints)     = " << sizeof(ints) << "  (int ints[3]: 3 по " << sizeof(int) << ")\n";
    std::cout << "  sizeof(&ints[0]) = " << sizeof(&ints[0]) << "   (вказівник, хоч на що він показує)\n";
    std::cout << "  sizeof(ints) / sizeof(ints[0]) = " << sizeof(ints) / sizeof(ints[0]) << '\n';
    inside(ints, sizeof(ints) / sizeof(ints[0]));

    std::cout << "\ni = " << i << ":\n";
    std::cout << "  buf        = " << (const void*)buf << '\n';
    std::cout << "  buf + i    = " << (const void*)(buf + i) << "   (зсув: i · sizeof(Byte) = " << i << ")\n";
    std::cout << "  buf[i]     = " << std::flush << (int)buf[i] << '\n';
    std::cout << "  *(buf + i) = " << std::flush << (int)*(buf + i) << '\n';
}
