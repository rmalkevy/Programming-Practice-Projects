// Дослід 3: масив записів — кожен спрайт рухається своїми полями. Відскоку від краю тут немає навмисно.
// Запуск: ./run.sh 03 3 10 5 1 0 50 20 -2 1   — 3 кроки, два спрайти по чотири числа: x y vx vy
//         ./run.sh 03 4 61 5 1 0 1 1 -1 0     — що буде біля краю екрана 64×32?
// Lab 06, Теорія §1, M2 · Notes 06, §5
#include "common.hpp"
#include <vector>

struct Sprite {
    std::uint8_t x, y;
    std::int8_t vx, vy;
    bool alive;
};

const int SCREEN_W = 64, SCREEN_H = 32;

void print(const Sprite s[], int count) {
    for (int i = 0; i < count; ++i) {
        bool off = s[i].x >= SCREEN_W || s[i].y >= SCREEN_H;
        std::cout << "   [" << i << "] x=" << std::setw(3) << (int)s[i].x << " y=" << std::setw(3) << (int)s[i].y
                  << ' ' << pad(off ? "поза" : "", 4);
    }
    std::cout << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 6 || (argc - 2) % 4 != 0) {
        std::cout << "usage: ./run.sh 03 <кроків> <x y vx vy> [x y vx vy ...]   наприклад: 3 10 5 1 0 50 20 -2 1\n";
        return 1;
    }
    Sprite sprites[8] = {};   // агрегатна ініціалізація: усі поля всіх восьми — нулі, alive = false
    int count = 0, ticks = 0;
    try {
        ticks = (int)parse_number(argv[1]);
        for (int i = 2; i + 3 < argc && count < 8; i += 4, ++count)
            sprites[count] = Sprite{(std::uint8_t)parse_number(argv[i]), (std::uint8_t)parse_number(argv[i + 1]),
                                    (std::int8_t)parse_number(argv[i + 2]), (std::int8_t)parse_number(argv[i + 3]),
                                    true};
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::cout << "sizeof(Sprite) = " << sizeof(Sprite) << ", sizeof(sprites) = " << sizeof(sprites)
              << ", живих: " << count << "\n\n";
    std::cout << "крок  0";
    print(sprites, count);
    for (int t = 1; t <= ticks; ++t) {
        for (int i = 0; i < 8; ++i) {
            if (!sprites[i].alive) continue;   // мертві й порожні записи пропускаємо
            sprites[i].x = (std::uint8_t)(sprites[i].x + sprites[i].vx);
            sprites[i].y = (std::uint8_t)(sprites[i].y + sprites[i].vy);
        }
        std::cout << "крок " << std::setw(2) << t;
        print(sprites, count);
    }
    std::cout << "\nпоза — за межами екрана " << SCREEN_W << "×" << SCREEN_H << ". Відскок від краю — ваш M2.\n";
}
