// Дослід 4: `p && *p == 3` — коротке замикання як охорона. Порядок частин має значення.
// Запуск: ./run.sh 04 3        — p вказує на число 3
//         ./run.sh 04 null     — p == nullptr
// Lab 04, Теорія §1 · Notes 04, §2 · nullptr — Lab 03, Теорія §1
#include "common.hpp"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 04 <число | null>   наприклад: 3, 5, null\n";
        return 1;
    }
    int x = 0;
    int* p = nullptr;
    std::string arg = argv[1];
    if (arg != "null") {
        try {
            x = (int)parse_number(arg);
        } catch (const std::exception&) {
            std::cout << "не можу прочитати як число: " << arg << '\n';
            return 1;
        }
        p = &x;
    }
    std::cout << (p ? "p = &x, *p = " + std::to_string(*p) : std::string("p = nullptr")) << "\n\n";

    // Спершу перевірка, потім розіменування: якщо p == nullptr, *p не виконається.
    std::cout << "p != nullptr && *p == 3   → " << std::flush;
    std::cout << (p != nullptr && *p == 3) << '\n';

    // Ті самі дві частини навпаки: *p виконується першим, навіть якщо p == nullptr.
    std::cout << "*p == 3 && p != nullptr   → " << std::flush;
    std::cout << (*p == 3 && p != nullptr) << '\n';
}
