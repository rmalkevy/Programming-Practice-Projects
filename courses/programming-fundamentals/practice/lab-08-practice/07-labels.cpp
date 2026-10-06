// Дослід 7: перший прохід нічого не видає — лише додає розміри й записує, яка мітка на якій адресі.
// Запуск: ./run.sh 07 fact          — таблиця міток: fact = 0x0007, base = 0x001B, як в ISA §6
//         ./run.sh 07 fact nop=5    — вставити NOP перед 5-м рядком: що зсунулось?
// Lab 08, Теорія §2 · Notes 08, §4 · ISA.uk.md §6
#include "common.hpp"
#include "programs.hpp"

using Labels = std::map<std::string, std::uint16_t>;

// Прохід 1: адреса кожного рядка — сума розмірів усіх рядків вище.
Labels pass1(const std::vector<Line>& lines, bool print) {
    Labels labels;
    std::uint16_t pc = 0;
    for (const Line& l : lines) {
        if (!l.label.empty()) labels[l.label] = pc;
        int size = FORMS.at(l.op).size;
        if (print)
            std::cout << hex16(pc).substr(2) << "   +" << size << "    " << source(l)
                      << (l.note == "вставлено" ? "    ← вставлено" : "") << '\n';
        pc = (std::uint16_t)(pc + size);
    }
    if (print) std::cout << hex16(pc).substr(2) << "         (кінець; розмір програми: " << pc << ")\n";
    return labels;
}

int main(int argc, char* argv[]) {
    const Program* prog = argc > 1 ? find_program(argv[1]) : nullptr;
    if (!prog) {
        std::cout << "usage: ./run.sh 07 <countdown | forward | fact> [nop=N]\n";
        return 1;
    }
    std::vector<Line> lines = prog->lines;
    long at = 0;
    if (argc > 2) {
        std::string a = argv[2];
        try {
            if (a.rfind("nop=", 0) != 0) throw std::invalid_argument(a);
            at = parse_number(a.substr(4));
        } catch (const std::exception&) {
            at = -1;
        }
        if (at < 1 || at > (long)lines.size() + 1) {
            std::cout << "nop=N: N — номер рядка від 1 до " << lines.size() + 1 << '\n';
            return 1;
        }
        lines.insert(lines.begin() + (at - 1), Line{"", "NOP", "", "вставлено"});
    }

    std::cout << prog->name << " (" << prog->where << "), прохід 1: жодного байта, лише адреси\n\n";
    std::cout << "адр.  розмір  текст\n";
    Labels now = pass1(lines, true);

    std::cout << "\nТаблиця міток:\n";
    if (at == 0) {
        for (const auto& kv : now) std::cout << "  " << pad(kv.first, 6) << hex16(kv.second) << '\n';
        return 0;
    }
    Labels before = pass1(prog->lines, false);
    std::cout << "  мітка   було    стало\n";
    for (const auto& kv : now)
        std::cout << "  " << pad(kv.first, 6) << "  " << hex16(before.at(kv.first)) << "  " << hex16(kv.second)
                  << (before.at(kv.first) != kv.second ? "   зсунулась" : "") << '\n';

    int changed = 0;
    for (const Line& l : lines)
        if (now.count(l.arg) && now.at(l.arg) != before.at(l.arg)) ++changed;
    std::cout << "\nОдин NOP, один байт — а операндів, у яких тепер інші байти: " << changed
              << ".\nРуками їх треба знайти й переписати всі; асемблер просто проходить ще раз.\n";
}
