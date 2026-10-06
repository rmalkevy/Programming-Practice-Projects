// Дослід 7: лінійний пошук — цикл із виходом. Кожне порівняння видно.
// Запуск: ./run.sh 07 4 3 1 4 1 5     — шукаємо 4 у 3 1 4 1 5
//         ./run.sh 07 9 3 1 4 1 5     — промах
//         ./run.sh 07 6 1 3 5 7 9     — відсортована ділянка: можна зупинитись раніше
// Lab 04, Теорія §3, M4 · Notes 04, §5
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;

// Як команда find із лаби: перший i в [lo, hi), де mem[i] == needle; промах — hi.
std::size_t find(const std::vector<Byte>& mem, std::size_t lo, std::size_t hi, Byte needle, int& looks) {
    looks = 0;
    for (std::size_t i = lo; i < hi; ++i) {
        ++looks;
        bool hit = mem[i] == needle;
        std::cout << "  i = " << i << ":  " << std::setw(3) << (int)mem[i] << " == " << (int)needle
                  << " ?  " << (hit ? "так → return " + std::to_string(i) : "ні") << '\n';
        if (hit) return i;
    }
    std::cout << "  i = " << hi << ":  i < hi хибне → цикл скінчився, return hi = " << hi << '\n';
    return hi;
}

// Для відсортованої ділянки: щойно mem[i] > needle, далі шукати немає сенсу.
std::size_t find_sorted(const std::vector<Byte>& mem, std::size_t lo, std::size_t hi, Byte needle, int& looks) {
    looks = 0;
    for (std::size_t i = lo; i < hi; ++i) {
        ++looks;
        if (mem[i] == needle) return i;
        if (mem[i] > needle) return hi;
    }
    return hi;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 07 <що шукаємо> <байти ...>   наприклад: 4 3 1 4 1 5\n";
        return 1;
    }
    Byte needle = 0;
    std::vector<Byte> mem;
    try {
        needle = (Byte)parse_number(argv[1]);
        for (int i = 2; i < argc; ++i) mem.push_back((Byte)parse_number(argv[i]));
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::cout << "шукаємо " << (int)needle << " у:";
    for (Byte b : mem) std::cout << ' ' << (int)b;
    std::cout << "\n\n";

    int looks = 0;
    std::size_t at = find(mem, 0, mem.size(), needle, looks);
    std::cout << "\nрезультат: " << at << (at == mem.size() ? "  (== hi, тобто не знайшли)" : "")
              << ", порівнянь: " << looks << '\n';

    bool sorted = true;
    for (std::size_t i = 1; i < mem.size(); ++i)
        if (mem[i - 1] > mem[i]) sorted = false;
    if (sorted) {
        int fast = 0;
        std::size_t at2 = find_sorted(mem, 0, mem.size(), needle, fast);
        std::cout << "\nДілянка відсортована. Зупинка на першому mem[i] > " << (int)needle
                  << ": результат " << at2 << ", порівнянь: " << fast << '\n';
    }
}
