// Дослід 3: sizeof(p) — ширина адреси, sizeof(*p) — розмір того, на що вона вказує.
// Запуск: ./run.sh 03
// Lab 03, Теорія §4 · Notes 03, §3
#include "common.hpp"

using Byte = std::uint8_t;
struct Memory { Byte data[4096]; };   // як у проєкті ember

void line(const std::string& expr, std::size_t n, const std::string& note = "") {
    std::cout << "  " << pad(expr, 26) << std::setw(5) << n
              << "  " << note << '\n';
}

// Масив у параметрі функції — це вже вказівник: sizeof бачить лише адресу.
void inside(const int* a) {
    line("sizeof(a) у функції", sizeof(a), "← адреса, а не масив; довжину треба передавати окремо");
}

int main() {
    std::cout << "Розміри об'єктів і розміри адрес:\n";
    line("sizeof(char)", sizeof(char));
    line("sizeof(int)", sizeof(int));
    line("sizeof(double)", sizeof(double));
    line("sizeof(char*)", sizeof(char*));
    line("sizeof(int*)", sizeof(int*));
    line("sizeof(double*)", sizeof(double*));
    line("sizeof(void*)", sizeof(void*), "← усі адреси однакової ширини");

    int x = 0;
    int* p = &x;
    std::cout << "\nint x;  int* p = &x;\n";
    line("sizeof(p)", sizeof(p), "ширина адреси");
    line("sizeof(*p)", sizeof(*p), "те, на що вона вказує");

    Memory m{};
    Memory* mem = &m;
    std::cout << "\nMemory m;  Memory* mem = &m;      (як у CPU з проєкту)\n";
    line("sizeof(mem)", sizeof(mem), "CPU тримає лише це");
    line("sizeof(*mem)", sizeof(*mem), "а вказує на всю коробку");

    int a[10] = {};
    std::cout << "\nint a[10];\n";
    line("sizeof(a)", sizeof(a), "10 · sizeof(int)");
    line("sizeof(a) / sizeof(a[0])", sizeof(a) / sizeof(a[0]), "кількість елементів");
    inside(a);
}
