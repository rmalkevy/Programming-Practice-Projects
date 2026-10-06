// Дослід 7: бульбашка — два вкладені цикли й обмін сусідів. Кожне порівняння видно.
// Запуск: ./run.sh 07 4 1 3 2        — приклад із Notes 05, §4
//         ./run.sh 07 1 2 3 4 5      — уже відсортовано: скільки порівнянь, скільки обмінів?
// Lab 05, Теорія §4 · Notes 05, §4
#include "common.hpp"

using Byte = std::uint8_t;
const int MAX = 16;

void swap(Byte* a, Byte* b) {
    Byte tmp = *a;
    *a = *b;
    *b = tmp;
}

// Надрукувати масив; пару, яку зараз порівнюємо, — у дужках.
void print(const Byte* a, int n, int mark) {
    for (int k = 0; k < n; ++k)
        std::cout << (k == mark ? '[' : ' ') << std::setw(3) << (int)a[k] << (k == mark + 1 ? ']' : ' ');
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 07 <числа 0..255, до " << MAX << " штук>   наприклад: 4 1 3 2\n";
        return 1;
    }
    Byte a[MAX] = {};
    int n = argc - 1;
    if (n > MAX) n = MAX;
    try {
        for (int k = 0; k < n; ++k) a[k] = (Byte)parse_number(argv[k + 1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    int compares = 0, swaps = 0;
    for (int i = 0; i < n; ++i) {
        int last = n - i - 1;   // скільки пар порівнюємо: праві i комірок уже на місці
        std::cout << "прохід " << i + 1 << ":\n";
        if (last <= 0) std::cout << "  порівнювати вже нічого\n";
        for (int j = 0; j < last; ++j) {
            ++compares;
            bool bigger = a[j] > a[j + 1];
            std::cout << "  ";
            print(a, n, j);
            if (bigger) {
                swap(&a[j], &a[j + 1]);
                ++swaps;
                std::cout << "   → обмін → ";
                print(a, n, j);
            }
            std::cout << '\n';
        }
    }

    std::cout << "\nрезультат:";
    for (int k = 0; k < n; ++k) std::cout << ' ' << (int)a[k];
    std::cout << "\nпорівнянь: " << compares << ", обмінів: " << swaps << '\n';
}
