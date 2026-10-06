// Дослід 2: p + 1 рухає на один ЕЛЕМЕНТ, а не на один байт.
// Запуск: ./run.sh 02        — три кроки
//         ./run.sh 02 6      — шість кроків
// Lab 03, Теорія §2 · Notes 03, §2
#include "common.hpp"

const int MAX_STEPS = 15;

// Пройти вказівником типу T на n кроків і показати, на скільки байтів він зсунувся.
template <typename T>
void walk(const std::string& type, int n) {
    T a[MAX_STEPS + 1] = {};
    T* p = a;
    std::cout << "  " << std::left << std::setw(10) << type << std::right << std::setw(6)
              << sizeof(T) << "   ";
    for (int k = 0; k <= n; ++k) {
        long bytes = (const char*)(p + k) - (const char*)p;   // різниця в байтах
        std::cout << std::setw(5) << ("+" + std::to_string(bytes));
    }
    std::cout << "     (p + " << n << ") - p = " << (p + n) - p << '\n';   // різниця в елементах
}

int main(int argc, char* argv[]) {
    int n = 3;
    try {
        if (argc >= 2) n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 02 [кроків 1.." << MAX_STEPS << "]\n";
        return 1;
    }
    if (n < 1 || n > MAX_STEPS) {
        std::cout << "кроків — від 1 до " << MAX_STEPS << '\n';
        return 1;
    }

    std::cout << "На скільки байтів p + k відходить від p:\n\n";
    std::cout << "  тип       sizeof   ";
    for (int k = 0; k <= n; ++k) std::cout << std::setw(5) << ("p+" + std::to_string(k));
    std::cout << '\n';
    walk<char>("char", n);
    walk<std::uint8_t>("Byte", n);
    walk<std::uint16_t>("uint16_t", n);
    walk<int>("int", n);
    walk<double>("double", n);

    // Ті самі адреси в шістнадцятковому: видно, що p + 1 для int — це +4 до числа.
    int a[2] = {10, 20};
    int* p = a;
    std::cout << "\nint a[2] = {10, 20};  int* p = a;\n";
    std::cout << "  p     = " << (void*)p << "   *p       = " << *p << '\n';
    std::cout << "  p + 1 = " << (void*)(p + 1) << "   *(p + 1) = " << *(p + 1) << '\n';
}
