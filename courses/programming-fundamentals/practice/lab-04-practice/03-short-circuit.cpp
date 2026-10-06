// Дослід 3: коротке замикання. `&&` не викликає праву частину, якщо ліва вже хибна.
// Запуск: ./run.sh 03 0 1     — f() поверне false, g() поверне true
//         ./run.sh 03 1 0
// Lab 04, Теорія §1 · Notes 04, §2
#include "common.hpp"

bool f_result = false, g_result = false;
std::string calls;   // хто з функцій встиг відпрацювати

bool f() { calls += "f "; return f_result; }
bool g() { calls += "g "; return g_result; }

void show(const std::string& expr, bool result) {
    std::cout << "  " << std::left << std::setw(20) << expr << std::right << "= " << result
              << "   викликано: " << calls << '\n';
    calls.clear();
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 03 <що поверне f: 0/1> <що поверне g: 0/1>   наприклад: 0 1\n";
        return 1;
    }
    try {
        f_result = parse_number(argv[1]) != 0;
        g_result = parse_number(argv[2]) != 0;
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::cout << "f() → " << f_result << ",  g() → " << g_result << "\n\n";
    bool r = f() && g();
    show("f() && g()", r);
    r = f() || g();
    show("f() || g()", r);

    // `&` і `|` — бітові операції: обидві частини рахуються завжди (порядок не визначений).
    // Прямо на bool clang це не збере (-Wbitwise-instead-of-logical), тому через int.
    r = (int)f() & (int)g();
    show("(int)f() & (int)g()", r);
    r = (int)f() | (int)g();
    show("(int)f() | (int)g()", r);
}
