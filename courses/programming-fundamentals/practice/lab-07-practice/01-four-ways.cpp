// Дослід 1: чотири способи передати число. Змінити змінну того, хто викликав, можуть лише T* і T&.
// Запуск: ./run.sh 01 1                        — чотири функції, кожна пробує додати 1
//         FLAGS=-DWRITE_CONST ./run.sh 01 1    — запис через const T&: не збереться
// Lab 07, Теорія §2 · Notes 07, §1 · копія проти вказівника — Lab 03, дослід 6
#include "common.hpp"

void by_value(int x) {
    std::cout << "    &x = " << &x;
    x = x + 1;
}

void by_pointer(int* p) {
    std::cout << "     p = " << p;
    *p = *p + 1;
}

void by_ref(int& r) {
    std::cout << "    &r = " << &r;
    r = r + 1;
}

void by_const_ref(const int& r) {
    std::cout << "    &r = " << &r;
#ifdef WRITE_CONST
    r = r + 1;   // const T& — лише читати
#endif
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 01 <число>   наприклад: 1\n";
        return 1;
    }
    int start = 0;
    try {
        start = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    int a = start, b = start, c = start, d = start;
    std::cout << "у main:  &a = " << &a << "  &b = " << &b << "\n"
              << "         &c = " << &c << "  &d = " << &d << "\n\n";

    std::cout << pad("by_value(a)", 20);
    by_value(a);
    std::cout << "    a = " << a << '\n';

    std::cout << pad("by_pointer(&b)", 20);
    by_pointer(&b);
    std::cout << "    b = " << b << '\n';

    std::cout << pad("by_ref(c)", 20);
    by_ref(c);
    std::cout << "    c = " << c << '\n';

    std::cout << pad("by_const_ref(d)", 20);
    by_const_ref(d);
    std::cout << "    d = " << d << '\n';

    std::cout << "\nразом: " << a << ' ' << b << ' ' << c << ' ' << d << '\n';
}
