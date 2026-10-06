// Дослід 5: глобальна змінна — одна коробка на всі виклики. Рекурсія, що тримає n у ній, губить n.
// Запуск: ./run.sh 05 4
// Lab 07, Теорія §2 («через глобальні змінні результат не повертають»), §3 · Notes 07, §1
#include "common.hpp"

int fact_local(int n) {
    if (n <= 1) return 1;
    int r = fact_local(n - 1);
    return n * r;                       // n — своє в цьому кадрі
}

int g_n = 0;                            // одна на всю програму

int fact_global(int n) {
    g_n = n;
    std::cout << "  >" << n << "   g_n = " << g_n << "   &g_n = " << &g_n << '\n';
    if (g_n <= 1) return 1;
    int r = fact_global(g_n - 1);       // виклик перезапише g_n
    std::cout << "  <" << n << "   g_n = " << g_n << "   r = " << r << '\n';
    return g_n * r;                     // g_n — те, що лишив останній виклик
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <n>   наприклад: 4\n";
        return 1;
    }
    int n = 0;
    try {
        n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 0 || n > 12) {
        std::cout << "n — від 0 до 12\n";
        return 1;
    }

    std::cout << "n у локальній змінній: fact(" << n << ") = " << fact_local(n) << "\n\n";
    std::cout << "n у глобальній g_n:\n";
    int r = fact_global(n);
    std::cout << "fact(" << n << ") = " << r << '\n';
}
