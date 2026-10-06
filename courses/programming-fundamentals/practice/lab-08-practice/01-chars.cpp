// Дослід 1: рядок асемблера — це лише байти символів. Що з них чим є, вирішує лексер, а не процесор.
// Запуск: ./run.sh 01 'LOADI A, 0x41 ; коментар'   — кожен байт рядка і його клас
//         ./run.sh 01 'ADD A, B'                    — а що побачив би step, якби читав текст напряму
// Lab 08, Теорія §1 · Notes 08, §1
#include "common.hpp"
#include <cctype>

// Той самий поділ, що в циклі lex() з M1: куди піде лексер, якщо курсор стоїть на цьому символі.
std::string kind(unsigned char c) {
    if (c >= 0x80) return "не ASCII (байт літери UTF-8) → помилка";
    if (std::isalpha(c) || c == '_') return "літера → ident()";
    if (std::isdigit(c)) return "цифра → number()";
    if (c == ' ' || c == '\t' || c == '\r') return "пробіл → пропустити";
    if (c == ';') return "початок коментаря";
    if (c == ',' || c == ':' || c == '[' || c == ']') return "пунктуація → свій токен";
    if (c == '\n') return "кінець рядка → Newline";
    return "невідомо → помилка";
}

std::string glyph(unsigned char c) {
    if (c == ' ') return "' '";
    if (c == '\t') return "\\t";
    if (c == '\n') return "\\n";
    if (c >= 0x20 && c < 0x7F) return std::string(1, (char)c);
    return "·";
}

// Чи є такий опкод у таблиці ISA.uk.md §5 (лише діапазони, без назв).
bool in_isa(unsigned char op) {
    return op <= 0x04 || (op >= 0x10 && op <= 0x1B) || (op >= 0x20 && op <= 0x2D) ||
           (op >= 0x30 && op <= 0x34) || (op >= 0x40 && op <= 0x43) || (op >= 0x50 && op <= 0x57) ||
           op == 0x60;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 01 '<рядок асемблера>'   наприклад: 'LOADI A, 0x41 ; коментар'\n";
        return 1;
    }
    std::string line = argv[1];
    for (int i = 2; i < argc; ++i) line += std::string(" ") + argv[i];
    line += '\n';   // у файлі кожен рядок закінчується '\n'

    std::cout << "   i  байт  символ  куди піде lex(), якщо курсор стоїть тут\n";
    bool in_comment = false;
    for (std::size_t i = 0; i < line.size(); ++i) {
        unsigned char c = (unsigned char)line[i];
        if (c == '\n') in_comment = false;
        std::string what = in_comment ? "усередині коментаря → пропустити" : kind(c);
        if (c == ';') in_comment = true;
        std::cout << std::setw(4) << i << "  " << hex2(c) << "    " << pad(glyph(c), 6) << "  " << what << '\n';
    }
    std::cout << "\nБайтів: " << line.size() << ". Токенів тут ще немає: їх зробить лексер, проходячи ці байти курсором i.\n";

    unsigned char first = (unsigned char)line[0];
    std::cout << "Якби step читав цей текст як код, першим опкодом був би " << hex(first)
              << " ('" << glyph(first) << "'): "
              << (in_isa(first) ? "такий опкод в ISA є, тож машина мовчки виконала б щось зовсім інше.\n"
                                : "такого опкоду в ISA немає, машина зупинилась би з unknown opcode.\n");
}
