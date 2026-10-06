// Дослід 5: три часи життя — статичний, автоматичний (стек) і динамічний (купа). Адреси видають, де хто живе.
// Запуск: ./run.sh 05 3   — глибина вкладених викликів і кількість new
// Lab 06, Теорія §3 · Notes 06, Ідея
#include "common.hpp"
#include <vector>

int global_counter = 0;   // статичний: є до main і після main

std::string addr(const void* p) {
    std::ostringstream out;
    out << p;
    return out.str();
}

void row(const std::string& what, const void* p, const std::string& note = "") {
    std::cout << "  " << pad(what, 26) << std::setw(16) << addr(p) << "  " << note << '\n';
}

// Кожен виклик має власну локальну змінну — свою коробку на стеку.
void dive(int depth, int max) {
    int local = depth;
    row("local у dive(" + std::to_string(depth) + ")", &local);
    if (depth < max) dive(depth + 1, max);
}   // тут local зникає

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <n>   наприклад: 3\n";
        return 1;
    }
    int n = 0;
    try {
        n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 1 || n > 10) {
        std::cout << "n має бути від 1 до 10\n";
        return 1;
    }

    static int calls = 0;     // теж статичний, хоч і оголошений у функції
    ++calls;
    std::cout << "Статичні:\n";
    row("global_counter", &global_counter, "живе весь час роботи програми");
    row("static calls у main", &calls);

    std::cout << "\nАвтоматичні (стек), виклик у виклику:\n";
    int in_main = 0;
    row("in_main", &in_main, "зникне на виході з main");
    dive(1, n);

    std::cout << "\nДинамічні (купа), new int:\n";
    std::vector<int*> heap;
    for (int i = 0; i < n; ++i) {
        heap.push_back(new int{i});
        row("new int{" + std::to_string(i) + "}", heap.back(), i == 0 ? "живе, поки не зробите delete" : "");
    }
    for (int* p : heap) delete p;   // кожному new — свій delete
    std::cout << "\n  усі " << n << " delete зроблено; вказівники у векторі тепер завислі\n";
}
