// Дослід 5: одна інструкція → байти. Опкод, потім операнд; 16-бітний — молодшим байтом уперед.
// Запуск: ./run.sh 05 JMP 0x0123        — 30 23 01, як у CHECKS.md
//         ./run.sh 05 HALT              — один байт 00
//         ./run.sh 05 LOADI A, 300      — операнд не влазить у байт: що тепер?
// Lab 08, Теорія §2, M2 · Notes 08, §4 · ISA.uk.md §4–5 · порядок байтів — Lab 3
#include "common.hpp"
#include "programs.hpp"

using Byte = std::uint8_t;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <інструкція> [число]   наприклад: JMP 0x0123  або  LOADI A, 65\n"
                  << "відомі форми (лише ці " << FORMS.size() << " з ISA §5):";
        for (const auto& f : FORMS) std::cout << "  " << f.first;
        std::cout << '\n';
        return 1;
    }
    std::string all = argv[1];
    for (int i = 2; i < argc; ++i) all += std::string(" ") + argv[i];

    // Уся фраза — форма без операнда, або остання частина — операнд.
    std::string op = all, arg;
    if (!FORMS.count(op) && argc > 2) {
        arg = argv[argc - 1];
        op = all.substr(0, all.size() - arg.size() - 1);
    }
    auto it = FORMS.find(op);
    if (it == FORMS.end()) {
        std::cout << "форми \"" << op << "\" у цій маленькій таблиці немає (./run.sh 05 — список)\n";
        return 1;
    }
    Form f = it->second;
    std::cout << pad(all + " ", 18) << "→ опкод " << hex(f.code) << ", розмір " << f.size << " (ISA §5)\n";

    if (f.size == 1 && !arg.empty()) {
        std::cout << "у " << op << " операнда немає, а написано \"" << arg << "\"\n";
        return 1;
    }
    if (f.size > 1 && arg.empty()) {
        std::cout << op << " без операнда: розмір " << f.size << ", а другий байт узяти нема звідки\n";
        return 1;
    }

    std::vector<Byte> bytes = {f.code};
    if (f.size > 1) {
        long v = 0;
        try {
            v = parse_number(arg);
        } catch (const std::exception&) {
            std::cout << "\"" << arg << "\" — не число. Якщо це мітка, її адресу дасть перший прохід (досліди 07, 09).\n";
            return 1;
        }
        if (f.size == 2) {
            Byte imm = (Byte)v;
            std::cout << "  imm8:  (Byte)" << v << " = " << hex(imm) << '\n';
            if (v < 0 || v > 0xFF)
                std::cout << "  " << v << " не влазить у байт, і приведення мовчки загорнуло його в " << (int)imm
                          << ".\n  Помилка чи загортання? Такого правила в ISA немає: вирішуєте ви і пишете в README.\n";
            bytes.push_back(imm);
        } else {
            std::uint16_t a = (std::uint16_t)v;
            Byte lo = (Byte)(a & 0xFF), hi = (Byte)(a >> 8);
            std::cout << "  addr16 = " << hex16(a) << ":  молодший a & 0xFF = " << hex(lo)
                      << ", старший a >> 8 = " << hex(hi) << " — молодший іде першим\n";
            if (v < 0 || v > 0xFFFF)
                std::cout << "  " << v << " не влазить у 16 бітів; приведення мовчки дало " << hex16(a) << ".\n";
            else if (v > 0xFFF)
                std::cout << "  У 16 бітів влазить, але пам'ять — лише до 0x0FFF. Чи пропустить таке ваш асемблер?\n";
            bytes.push_back(lo);
            bytes.push_back(hi);
        }
    }

    std::cout << "\nбайти:";
    for (Byte b : bytes) std::cout << ' ' << hex2(b);
    std::cout << '\n';
}
