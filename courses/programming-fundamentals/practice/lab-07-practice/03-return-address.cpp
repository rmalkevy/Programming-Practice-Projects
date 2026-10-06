// Дослід 3: виклик — це стрибок, який пам'ятає. Та сама функція з різних місць отримує різні адреси повернення.
// Запуск: ./run.sh 03       — три виклики one() з трьох місць demo()
//         ./run.sh 03 2     — те саме, але one() зайде в себе ще на два рівні
// Lab 07, Теорія §1 · ISA.uk.md §6 (CALL кладе P + 3)
#include "common.hpp"

// Адреси функцій хоста змінюються від запуску до запуску, тому друкуємо ще й зсув
// від початку функції, всередині якої лежить адреса: «demo + 52».
std::string where(const void* p);

void one(int depth, const char* from) {
    // __builtin_return_address(0) — адреса, яку CALL цього виклику поклав на стек:
    // інструкція ПІСЛЯ виклику в тому, хто викликав.
    const void* ret = __builtin_return_address(0);
    std::cout << "  " << pad(from, 10) << "one(" << depth << ")  повернеться на " << ret << "  = " << where(ret) << '\n';
    if (depth > 0) one(depth - 1, "з one");
}

void demo(int depth) {
    one(depth, "рядок 1");
    one(depth, "рядок 2");
    one(depth, "рядок 3");
}

std::string where(const void* p) {
    long to_one = (long)((const char*)p - (const char*)(void*)&one);
    long to_demo = (long)((const char*)p - (const char*)(void*)&demo);
    // Адреса лежить у тій функції, що починається найближче перед нею.
    if (to_demo >= 0 && (to_one < 0 || to_demo < to_one)) return "demo + " + std::to_string(to_demo);
    if (to_one >= 0) return "one + " + std::to_string(to_one);
    return "?";
}

int main(int argc, char* argv[]) {
    int depth = 0;
    if (argc >= 2) {
        try {
            depth = (int)parse_number(argv[1]);
        } catch (const std::exception&) {
            std::cout << "не можу прочитати як число\n";
            return 1;
        }
        if (depth < 0 || depth > 5) {
            std::cout << "usage: ./run.sh 03 [глибина 0..5]\n";
            return 1;
        }
    }
    std::cout << "one  починається з " << (void*)&one << "\n"
              << "demo починається з " << (void*)&demo << "\n\n";
    demo(depth);
}
