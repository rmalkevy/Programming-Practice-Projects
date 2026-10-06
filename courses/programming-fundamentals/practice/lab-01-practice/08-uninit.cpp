// Дослід 8: що лежить у пам'яті, яку ніхто не ініціалізував. Ті самі {} з memory.hpp.
// Запуск: ./run.sh 08
// Читати неініціалізоване — UB. Тут це навмисно, як у M4.4, і лише для того, щоб побачити.
// Lab 01, Теорія §5, M4.4
#include "common.hpp"

using Byte = std::uint8_t;
const std::size_t SIZE = 16;

struct Zeroed { Byte data[SIZE]{}; };   // як у скелеті
struct Raw { Byte data[SIZE]; };        // без {}

void line(const std::string& name, const Byte* p) {
    std::cout << "  " << pad(name, 28);
    for (std::size_t i = 0; i < SIZE; ++i) std::cout << hex2(p[i]) << ' ';
    std::cout << '\n';
}

void on_stack() {
    Zeroed z;
    Raw r;
    line("стек, Zeroed z;", z.data);
    line("стек, Raw r;", r.data);
}

int main() {
    std::cout << "Перші " << SIZE << " байтів:\n";
    on_stack();

    Zeroed* hz = new Zeroed;
    Raw* hr = new Raw;
    line("купа, new Zeroed", hz->data);
    line("купа, new Raw", hr->data);
    delete hz;
    delete hr;
}
