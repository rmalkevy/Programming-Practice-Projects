// Дослід 9: два проходи разом — спершу таблиця міток, потім байти — і звірка з лістингом із курсу байт у байт.
// Запуск: ./run.sh 09 fact        — 30 байтів, мають збігтись із ISA.uk.md §6 усі
//         ./run.sh 09 forward     — те, на чому спіткнувся дослід 06
//         ./run.sh 09 countdown   — ISA.uk.md §9
// Лише 15 форм і три програми, вже розкладені на поля: лексера, розбору рядка й повідомлень
// про синтаксичні помилки тут немає — це і є ваш асемблер (M2).
// Lab 08, Теорія §2, M2 · Notes 08, §4 · CHECKS.md, Lab 8
#include "common.hpp"
#include "programs.hpp"

using Byte = std::uint8_t;
using Labels = std::map<std::string, std::uint16_t>;

// Прохід 1: лише адреси міток.
Labels pass1(const std::vector<Line>& lines) {
    Labels labels;
    std::uint16_t pc = 0;
    for (const Line& l : lines) {
        if (!l.label.empty()) labels[l.label] = pc;
        pc = (std::uint16_t)(pc + FORMS.at(l.op).size);
    }
    return labels;
}

// Прохід 2: байти. Тепер кожна мітка вже відома — або її немає взагалі.
bool pass2(const std::vector<Line>& lines, const Labels& labels, std::vector<Byte>& out,
           std::vector<std::size_t>& starts) {
    for (std::size_t n = 0; n < lines.size(); ++n) {
        const Line& l = lines[n];
        Form f = FORMS.at(l.op);
        starts.push_back(out.size());
        out.push_back(f.code);
        if (f.size == 2) {
            out.push_back((Byte)parse_number(l.arg));
        } else if (f.size == 3) {
            auto it = labels.find(l.arg);
            if (it == labels.end()) {
                std::cout << "рядок " << n + 1 << ": невідома мітка '" << l.arg << "'\n";
                return false;
            }
            out.push_back((Byte)(it->second & 0xFF));   // молодший уперед
            out.push_back((Byte)(it->second >> 8));
        }
    }
    return true;
}

int main(int argc, char* argv[]) {
    const Program* prog = argc > 1 ? find_program(argv[1]) : nullptr;
    if (!prog) {
        std::cout << "usage: ./run.sh 09 <countdown | forward | fact>\n";
        return 1;
    }

    Labels labels = pass1(prog->lines);
    std::cout << "прохід 1, мітки:";
    for (const auto& kv : labels) std::cout << "  " << kv.first << " = " << hex16(kv.second);
    std::cout << "\nпрохід 2, байти:\n\n";

    std::vector<Byte> out;
    std::vector<std::size_t> starts;
    if (!pass2(prog->lines, labels, out, starts)) return 1;

    const std::vector<Byte>& want = prog->listing;
    std::cout << "адр.  зібрано     " << pad(prog->where, 14) << "текст\n";
    for (std::size_t n = 0; n < prog->lines.size(); ++n) {
        std::size_t from = starts[n];
        std::size_t to = n + 1 < starts.size() ? starts[n + 1] : out.size();
        std::string got, ref;
        for (std::size_t k = from; k < to; ++k) {
            got += hex2(out[k]) + " ";
            ref += k < want.size() ? hex2(want[k]) + " " : "-- ";
        }
        const Line& l = prog->lines[n];
        std::cout << hex16((std::uint16_t)from).substr(2) << "  " << std::left << std::setw(10) << got << "  "
                  << std::setw(12) << ref << std::right << "  " << source(l);
        std::string gap(source(l).size() < 20 ? 20 - source(l).size() : 1, ' ');
        if (got != ref) std::cout << gap << "← не те";
        else if (!l.note.empty()) std::cout << gap << "; " << l.note;
        std::cout << '\n';
    }

    std::size_t same = 0, first_bad = out.size();
    for (std::size_t k = 0; k < out.size() && k < want.size(); ++k) {
        if (out[k] == want[k]) ++same;
        else if (first_bad == out.size()) first_bad = k;
    }
    std::cout << "\nзбіглося " << same << " з " << want.size() << " очікуваних байтів (" << prog->where << ")";
    if (out.size() != want.size()) std::cout << "; зібрано " << out.size() << " байтів, а в лістингу " << want.size();
    std::cout << '\n';
    if (first_bad < out.size())
        std::cout << "перше розходження на " << hex16((std::uint16_t)first_bad) << ": зібрано " << hex2(out[first_bad])
                  << ", у лістингу " << hex2(want[first_bad]) << '\n';
}
