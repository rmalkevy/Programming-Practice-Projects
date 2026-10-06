// Дослід 6: локальна змінна помирає разом із кадром. Адреса, яку з нього винесли, вказує на чужий кадр.
// Запуск: ./run.sh 06 42                                            — адреса через проміжну змінну
//         FLAGS=-DDIRECT ./run.sh 06 42                             — return &local; компілятор не пропустить
//         ASAN_OPTIONS=detect_stack_use_after_return=1 ./run.sh 06 42   — попросити ASan стерегти мертві кадри
// Lab 07, Теорія §1 («помирають разом із поверненням») · Notes 07, §1
#include "common.hpp"

int* keep(int v) {
    int local = v;
#ifdef DIRECT
    return &local;
#else
    int* p = &local;   // та сама адреса, але компілятор уже не стежить, звідки вона
    return p;
#endif
}

// Інший виклик з того самого місця: його кадр ляже туди, де був кадр keep.
// Нічого не друкує — сам друк теж викликає функції й перезаписує стек.
const void* other_mine = nullptr;
int other(int w) {
    int mine = w;
    other_mine = &mine;
    return mine;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 06 <число>   наприклад: 42\n";
        return 1;
    }
    int v = 0;
    try {
        v = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    int* p = keep(v);
    int before = *p;             // кадр keep уже не існує, але його ще ніхто не зайняв
    other(v + 1000);
    int after = *p;              // а тепер на тому місці побував кадр other
    std::cout << "keep(" << v << ") повернула p = " << p << '\n'
              << "other(" << v + 1000 << "): &mine = " << other_mine
              << (other_mine == p ? "   ← та сама адреса" : "") << '\n'
              << "*p до other:   " << before << '\n'
              << "*p після other: " << after << '\n';
}
