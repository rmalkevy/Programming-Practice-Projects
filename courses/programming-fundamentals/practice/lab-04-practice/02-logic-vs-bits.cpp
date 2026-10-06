// Дослід 2: `&&` і `&` — різні операції. Логічна питає «обидва не нуль?», бітова — «які біти спільні?».
// Запуск: ./run.sh 02 1 2
//         ./run.sh 02 6 3
// Lab 04, Теорія §1 · Notes 04, §1 · бітові операції — Lab 02
#include "common.hpp"

void row(const std::string& expr, int value, const std::string& note = "") {
    std::cout << "  " << std::left << std::setw(8) << expr << std::right << std::setw(4) << value;
    if (!note.empty()) std::cout << "   " << note;
    std::cout << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 02 <a> <b>   наприклад: 1 2\n";
        return 1;
    }
    int a = 0, b = 0;
    try {
        a = (int)parse_number(argv[1]);
        b = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::uint8_t ua = (std::uint8_t)a, ub = (std::uint8_t)b;
    std::cout << "a = " << a << " (" << bits(ua) << "),  b = " << b << " (" << bits(ub) << ")\n\n";

    row("a && b", a && b, "обидва не нуль?");
    row("a & b", a & b, bits((std::uint8_t)(a & b)) + "  спільні біти");
    row("a || b", a || b, "хоч один не нуль?");
    row("a | b", a | b, bits((std::uint8_t)(a | b)));
    row("!a", !a, "a — нуль?");
    row("~a", ~a, bits((std::uint8_t)~a) + "  усі біти навпаки");

    std::cout << "\nЯк умова в if:\n";
    std::cout << "  if (a && b) → " << ((a && b) ? "так" : "ні") << '\n';
    std::cout << "  if (a & b)  → " << ((a & b) ? "так" : "ні")
              << ((bool)(a && b) != (bool)(a & b) ? "   ← ось тут вони розходяться" : "") << '\n';
}
