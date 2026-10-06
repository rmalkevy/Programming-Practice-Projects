// Дослід 1: `=` в умові. Присвоєння має значення, і `if` перевіряє саме його.
// Запуск: ./run.sh 01 0                 — НЕ збереться: -Werror робить попередження помилкою
//         NO_WERROR=1 ./run.sh 01 0     — збереться з попередженням; подивіться, що надрукує
//         NO_WERROR=1 ./run.sh 01 5
// Lab 04, Теорія §1 · Notes 04, §1
#include "common.hpp"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: NO_WERROR=1 ./run.sh 01 <число>   наприклад: 0, 3, 5\n";
        return 1;
    }
    int v = 0;
    try {
        v = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число: " << argv[1] << '\n';
        return 1;
    }

    int x = 3;
    std::cout << "x = " << x << ", v = " << v << "\n\n";

    // Задумано: «x дорівнює v?»
    std::cout << "if (x == v)  → " << (x == v ? "так" : "ні") << ", x = " << x << '\n';

    // Написано з однією `=`: спершу x стає v, потім if дивиться, чи v не нуль.
    if (x = v)
        std::cout << "if (x = v)   → так, x = " << x << '\n';
    else
        std::cout << "if (x = v)   → ні, x = " << x << '\n';

    std::cout << "\nПісля if змінна x уже інша: " << x << '\n';
}
