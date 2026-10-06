// Дослід 6: асемблер в один прохід видає байти одразу — і спотикається на першій мітці, яка стоїть нижче.
// Запуск: ./run.sh 06 countdown   — мітка вище: один прохід справляється
//         ./run.sh 06 forward     — JMP done: адреси done ще ніхто не бачив
//         ./run.sh 06 fact        — CALL fact і обидва JZ base дивляться вниз
// Lab 08, Теорія §2 · Notes 08, §4 · ISA.uk.md §6
#include "common.hpp"
#include "programs.hpp"

using Byte = std::uint8_t;

int main(int argc, char* argv[]) {
    const Program* prog = argc > 1 ? find_program(argv[1]) : nullptr;
    if (!prog) {
        std::cout << "usage: ./run.sh 06 <countdown | forward | fact>\n";
        return 1;
    }
    std::cout << prog->name << " (" << prog->where << "), один прохід згори донизу:\n\n";
    std::cout << "адр.  байти       текст\n";

    std::map<std::string, std::uint16_t> labels;   // мітки, які вже траплялись
    std::vector<std::string> missing;              // операнди, які лишились ?? ??
    std::map<std::string, int> asked;              // мітки, які питали, поки їх ще не було
    std::uint16_t pc = 0;
    for (const Line& l : prog->lines) {
        if (!l.label.empty()) labels[l.label] = pc;
        Form f = FORMS.at(l.op);

        std::string raw = hex2(f.code) + " ";
        if (f.size == 2) {
            raw += hex2((Byte)parse_number(l.arg)) + " ";
        } else if (f.size == 3) {
            auto it = labels.find(l.arg);
            if (it != labels.end()) {
                raw += hex2((Byte)(it->second & 0xFF)) + " " + hex2((Byte)(it->second >> 8)) + " ";
            } else {
                raw += "?? ?? ";
                missing.push_back(hex16(pc).substr(2) + "  " + l.op + " " + l.arg);
                ++asked[l.arg];
            }
        }
        std::string why;
        if (!l.label.empty()) {
            why = l.label + " = " + hex16(pc);
            if (asked.count(l.label)) why += " — запізно для рядків вище";
        } else if (raw.find('?') != std::string::npos) {
            why = l.arg + " ще не траплялась";
        }
        std::cout << hex16(pc).substr(2) << "  " << std::left << std::setw(10) << raw << std::right << "  "
                  << (why.empty() ? source(l) : pad(source(l), 22) + "  ; " + why) << '\n';
        pc = (std::uint16_t)(pc + f.size);
    }

    if (missing.empty()) {
        std::cout << "\nУсі мітки стояли вище за свої стрибки, тож одного проходу вистачило.\n";
        return 0;
    }
    std::cout << "\nОперандів, не заповнених за один прохід: " << missing.size() << "\n";
    for (const std::string& m : missing) std::cout << "  " << m << '\n';
    std::cout << "Наприкінці адреси вже відомі:";
    for (const auto& kv : labels) std::cout << "  " << kv.first << " = " << hex16(kv.second);
    std::cout << "\nале байти на місці ?? ?? уже видано. Тому асемблер спершу проходить увесь текст\n"
              << "і збирає мітки (дослід 07), а байти видає другим проходом (дослід 09).\n";
}
