// Дослід 3: готові функції читають число «скільки вийде» і мовчать про решту. number() так не може.
// Запуск: ./run.sh 03                        — стандартний набір: 65 0x41 0b101 0xGG 0x 12ab 010 300
//         ./run.sh 03 0xGG 12ab 0b101       — свої рядки
// Lab 08, Теорія §1, M1 · Notes 08, §2
#include "common.hpp"
#include <cstdlib>
#include <vector>

int main(int argc, char* argv[]) {
    std::vector<std::string> inputs;
    for (int i = 1; i < argc; ++i) inputs.push_back(argv[i]);
    if (inputs.empty()) inputs = {"65", "0x41", "0b101", "0xGG", "0x", "12ab", "010", "300"};

    std::cout << "рядок         atoi(s)   strtol(s, &end, 0)    stoi(s, &pos, 0)\n";
    for (const std::string& s : inputs) {
        int a = std::atoi(s.c_str());

        char* end = nullptr;
        long l = std::strtol(s.c_str(), &end, 0);   // база 0: сама впізнає 0x… і 0…
        std::size_t used = (std::size_t)(end - s.c_str());

        std::string st;
        try {
            std::size_t pos = 0;
            int v = std::stoi(s, &pos, 0);
            st = std::to_string(v) + "  (pos = " + std::to_string(pos) + ")";
        } catch (const std::invalid_argument&) {
            st = "invalid_argument";
        } catch (const std::out_of_range&) {
            st = "out_of_range";
        }

        std::cout << pad(s, 12) << std::setw(9) << a << "   "
                  << std::setw(6) << l << "  з'їла " << used << " з " << s.size() << "   " << st;
        if (used == 0) std::cout << "   ← нуль, хоча числа не було";
        else if (used < s.size()) std::cout << "   ← решту \"" << s.substr(used) << "\" мовчки покинуто";
        std::cout << '\n';
    }

    std::cout << "\nНа 0xGG, 0x і 12ab жодна з трьох не відмовляє: «з'їла N з M» треба перевіряти самим.\n"
              << "А в лексері число закінчується не кінцем рядка, а пробілом, комою чи '\\n' —\n"
              << "тож і «з'їла все» там нічого не доводить. Що вважати числом, вирішує ваша number().\n";
}
