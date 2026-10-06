// Дослід 6: функція отримує копію. Змінити змінну того, хто викликав, можна лише через адресу.
// Запуск: ./run.sh 06 3 7
// Lab 03, Теорія §1 · Notes 03, §4 · далі — Lab 07 (кадри стека)
#include "common.hpp"

void inc_copy(int x) {
    std::cout << "    у inc_copy:  &x = " << &x << "   ← інша коробка\n";
    x = x + 1;
}

void inc_ptr(int* p) {
    std::cout << "    у inc_ptr:    p = " << p << "   ← та сама коробка\n";
    *p = *p + 1;
}

void swap_copy(int a, int b) {
    int t = a;
    a = b;
    b = t;   // обміняли копії; копії зникнуть разом із функцією
}

void swap_ptr(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 06 <a> <b>   наприклад: 3 7\n";
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

    std::cout << "a = " << a << ", &a = " << &a << "\n\n";
    std::cout << "inc_copy(a):\n";
    inc_copy(a);
    std::cout << "  a = " << a << '\n';
    std::cout << "inc_ptr(&a):\n";
    inc_ptr(&a);
    std::cout << "  a = " << a << "\n\n";

    std::cout << "a = " << a << ", b = " << b << '\n';
    swap_copy(a, b);
    std::cout << "swap_copy(a, b)    → a = " << a << ", b = " << b << '\n';
    swap_ptr(&a, &b);
    std::cout << "swap_ptr(&a, &b)   → a = " << a << ", b = " << b << '\n';
}
