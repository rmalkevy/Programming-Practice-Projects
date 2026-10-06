// Дослід 6: область видимості й час життя. Дві коробки з іменем x; static переживає виклик.
// Запуск: ./run.sh 06        — три виклики
//         ./run.sh 06 5
// Lab 04, Теорія §4 · Notes 04, §4
#include "common.hpp"

// Що пам'ятає функція між викликами.
void tick(int call) {
    int fresh = 0;          // автоматична: створюється заново на кожному виклику
    static int kept = 0;    // static: створюється один раз і живе до кінця програми
    fresh = fresh + 1;
    kept = kept + 1;
    std::cout << "  виклик " << call << ":  fresh = " << fresh << ",  kept = " << kept
              << "   &kept = " << &kept << '\n';
}

int main(int argc, char* argv[]) {
    int n = 3;
    try {
        if (argc >= 2) n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "usage: ./run.sh 06 [скільки викликів]\n";
        return 1;
    }

    int x = 1;
    std::cout << "Зовнішній x = " << x << ",  &x = " << &x << '\n';
    {
        int x = 10;   // затінення: це інша змінна з тим самим ім'ям
        std::cout << "  внутрішній x = " << x << ", &x = " << &x << "   ← інша коробка\n";
        x = x + 5;
        std::cout << "  внутрішній x = " << x << " після x = x + 5\n";
    }
    std::cout << "Зовнішній x = " << x << "   ← його ніхто не чіпав\n\n";

    std::cout << "tick() " << n << " раз(и):\n";
    for (int i = 1; i <= n; ++i) tick(i);
}
