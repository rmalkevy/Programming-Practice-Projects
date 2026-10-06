// Дослід 7: кожен рівень рекурсії бере ще шматок стека. Стек скінченний, і без бази він закінчується.
// Запуск: ./run.sh 07 1000                       — база на глибині 1000: скільки стека це коштує
//         ./run.sh 07 -1                         — база є, але недосяжна: ASan ловить stack-overflow
//         FLAGS=-DNO_BASE ./run.sh 07 0          — бази немає взагалі: компілятор не збере
// Lab 07, Теорія §3 («без базового випадку стек переповниться») · Notes 07, §4
#include "common.hpp"

// __builtin_frame_address(0) — де на справжньому стеку лежить кадр цього виклику.
// Не &n: ASan на Linux переносить локальні змінні в «фальшивий стек» (див. дослід 4).
const char* first = nullptr;   // кадр першого виклику

void report(long n, const char* frame) {
    // std::endl, а не '\n': коли ASan зупинить процес, буфер виводу вже не допишеться.
    std::cout << "  глибина " << std::setw(7) << n << "   стека з'їдено " << std::setw(9)
              << (first - frame) << " байтів" << std::endl;
}

long down(long n, long stop) {
    const char* frame = (const char*)__builtin_frame_address(0);
    if (first == nullptr) first = frame;
    bool round = n == 1 || n == 10 || n == 100 || n == 1000 || n % 10000 == 0;
    if (round) report(n, frame);
#ifdef NO_BASE
    (void)stop;
#else
    if (n == stop) {                 // база
        if (!round) report(n, frame);
        return 1;
    }
#endif
    return 1 + down(n + 1, stop);    // «1 +» робить виклик не останньою дією: справжня глибина
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 07 <глибина бази>   наприклад: 1000   (-1 — база недосяжна)\n";
        return 1;
    }
    long stop = 0;
    try {
        stop = parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    long r = down(1, stop);
    std::cout << "повернулись: " << r << " рівнів\n";
}
