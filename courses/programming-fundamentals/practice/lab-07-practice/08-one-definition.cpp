// Дослід 8: оголошення — обіцянка, визначення — виконання. Лінкер шукає рівно одне визначення на всю програму.
// Запуск: ./run.sh 08 5                                   — одне визначення: працює
//         FLAGS=extra-push.cpp ./run.sh 08 5              — два визначення в двох .cpp: помилка лінкера
//         FLAGS=-DNO_DEF ./run.sh 08 5                    — жодного: компілятор задоволений, лінкер — ні
//         FLAGS="-DNO_DEF extra-push.cpp" ./run.sh 08 5   — визначення в іншому .cpp: працює
// Lab 07, Теорія §4 · Notes 07, §3
#include "common.hpp"

// Оголошення: так рядок виглядав би в stack.hpp. Тіла немає — лише «така функція десь є».
bool push(int v);

#ifndef NO_DEF
// Визначення: тіло. Має бути в рівно одному .cpp програми.
bool push(int v) {
    std::cout << "push(" << v << ") з 08-one-definition.cpp\n";
    return true;
}
#endif

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 08 <число>   наприклад: 5\n";
        return 1;
    }
    int v = 0;
    try {
        v = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    std::cout << "main кличе push(" << v << ")\n";
    push(v);
}
