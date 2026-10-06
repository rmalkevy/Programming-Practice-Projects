// Дослід 7: витік — об'єкт у купі живий, а вказівника на нього вже немає. LeakSanitizer є не скрізь.
// Запуск: ./run.sh 07 3                           — тричі new в один вказівник, жодного delete
//         ASAN_OPTIONS=detect_leaks=1 ./run.sh 07 3   — попросити LeakSanitizer явно
// Lab 06, Теорія §3, M3 · Notes 06, §4 · errors.notes.md §3
#include "common.hpp"

struct Sprite {
    std::uint8_t x, y;
    std::int8_t vx, vy;
    bool alive;
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 07 <скільки new>   наприклад: 3\n";
        return 1;
    }
    int n = 0;
    try {
        n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 0 || n > 100) {
        std::cout << "від 0 до 100\n";
        return 1;
    }

    // std::endl, а не '\n': знайшовши витік, LeakSanitizer завершує процес,
    // не скинувши буфер виводу, і ненадрукований текст зник би.
    Sprite* p = nullptr;
    for (int i = 0; i < n; ++i) {
        p = new Sprite{(std::uint8_t)i, 0, 1, 0, true};   // старе значення p просто затерли
        std::cout << "new Sprite #" << i << " → " << p << std::endl;
    }
    p = nullptr;   // і останній теж
    std::cout << "\nОб'єктів у купі: " << n << " по " << sizeof(Sprite) << " байтів. Вказівників на них: 0.\n"
              << "Звільнити їх уже нікому. Що скаже LeakSanitizer — дивіться нижче (або нічого)." << std::endl;
}
