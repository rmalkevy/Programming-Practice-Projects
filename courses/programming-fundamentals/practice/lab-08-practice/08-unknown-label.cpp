// Дослід 8: невідома мітка в другому проході. labels[name] мовчки дає 0 і ще й дописує мітку; find() каже «немає».
// Запуск: ./run.sh 08 base    — мітка є: 0x001B
//         ./run.sh 08 bsae    — одруківка: що поверне [] і що find()?
// Lab 08, Теорія §2 («JMP без цілі — помилки») · Notes 08, §4
#include "common.hpp"
#include "programs.hpp"

using Byte = std::uint8_t;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 08 <ім'я мітки>   наприклад: base або bsae\n";
        return 1;
    }
    std::string name = argv[1];

    // Прохід 1 для fact з ISA §6 (як у досліді 07).
    std::map<std::string, std::uint16_t> labels;
    std::uint16_t pc = 0;
    for (const Line& l : find_program("fact")->lines) {
        if (!l.label.empty()) labels[l.label] = pc;
        pc = (std::uint16_t)(pc + FORMS.at(l.op).size);
    }
    auto show = [&]() {
        std::cout << "  у таблиці " << labels.size() << ":";
        for (const auto& kv : labels) std::cout << "  " << kv.first << " = " << hex16(kv.second);
        std::cout << '\n';
    };
    std::cout << "Таблиця міток fact після першого проходу:\n";
    show();

    std::cout << "\nДругий прохід дійшов до  JZ " << name << "\n\n";

    std::cout << "1) labels.find(\"" << name << "\"):\n";
    auto it = labels.find(name);
    if (it != labels.end())
        std::cout << "  знайдено: " << hex16(it->second) << '\n';
    else
        std::cout << "  == labels.end() — такої мітки немає. Тут асемблер і має зупинитись із номером рядка.\n";
    show();

    std::cout << "\n2) labels[\"" << name << "\"]:\n";
    std::uint16_t a = labels[name];
    std::cout << "  повернуло " << hex16(a) << (it == labels.end() ? ", жодного слова про помилку" : "") << '\n';
    show();
    std::cout << "  байти: 31 " << hex2((Byte)(a & 0xFF)) << ' ' << hex2((Byte)(a >> 8)) << "  — JZ " << hex16(a);
    if (it == labels.end())
        std::cout << ": стрибок на початок програми.\n"
                  << "  Програма збереться без жодної помилки, а впаде вже під час run, далеко від цього рядка.\n";
    else
        std::cout << '\n';
}
