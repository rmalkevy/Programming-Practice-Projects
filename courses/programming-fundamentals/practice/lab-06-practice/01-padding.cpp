// Дослід 1: sizeof структури більший за суму полів — між полями лежать вирівнювальні байти.
// Запуск: ./run.sh 01 65 300   — c = 65, n = 300: дамп усіх байтів структури
// Lab 06, Теорія §1 · Notes 06, §1
#include "common.hpp"
#include <cstddef>
#include <cstring>

struct P {
    char c;
    int n;
};

// Чи належить байт i полю, що починається на off і має size байтів?
bool owns(std::size_t i, std::size_t off, std::size_t size) {
    return i >= off && i < off + size;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 01 <c> <n>   наприклад: 65 300\n";
        return 1;
    }
    P p;
    // Спершу заллємо всю структуру байтом 0xEE — так буде видно,
    // які байти не належать жодному полю.
    std::memset(&p, 0xEE, sizeof(p));
    try {
        p.c = (char)parse_number(argv[1]);
        p.n = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::cout << "struct P { char c; int n; };\n\n";
    std::cout << "  sizeof(char) + sizeof(int) = " << sizeof(char) + sizeof(int) << '\n';
    std::cout << "  sizeof(P)                  = " << sizeof(P) << '\n';
    std::cout << "  alignof(int)               = " << alignof(int)
              << "   ← адреса int має ділитися на це число\n\n";

    std::cout << "  " << pad("поле", 6) << pad("offsetof", 10) << "sizeof\n";
    std::cout << "  " << pad("c", 6) << pad(std::to_string(offsetof(P, c)), 10) << sizeof(p.c) << '\n';
    std::cout << "  " << pad("n", 6) << pad(std::to_string(offsetof(P, n)), 10) << sizeof(p.n) << '\n';
    std::cout << "\n  &p.n - &p.c = "
              << (const char*)&p.n - &p.c << " байти\n\n";

    // Структура — це просто байти поспіль. Подивимось на кожен.
    const unsigned char* raw = (const unsigned char*)&p;
    std::cout << "  зміщення:";
    for (std::size_t i = 0; i < sizeof(p); ++i) std::cout << std::setw(4) << i;
    std::cout << "\n  байт:    ";
    for (std::size_t i = 0; i < sizeof(p); ++i) std::cout << "  " << hex2(raw[i]);
    std::cout << "\n  чий:     ";
    for (std::size_t i = 0; i < sizeof(p); ++i) {
        if (owns(i, offsetof(P, c), sizeof(char))) std::cout << "   c";
        else if (owns(i, offsetof(P, n), sizeof(int))) std::cout << "   n";
        else std::cout << "  ··";
    }
    std::cout << "\n\n  ·· — вирівнювальні байти (padding): у них досі 0xEE, бо жодне поле їх не займає.\n";
}
