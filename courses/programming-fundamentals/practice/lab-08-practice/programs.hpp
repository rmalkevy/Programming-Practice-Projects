// Для дослідів 05–09: п'ятнадцять рядків таблиці ISA і три програми з курсу,
// УЖЕ розкладені на поля «мітка / інструкція / операнд».
// Розкласти текст на ці поля — це ваш лексер і ваш асемблер (M1–M2); тут цього немає навмисно,
// щоб у дослідах лишились тільки адреси, мітки й байти.
#pragma once
#include <cstdint>
#include <map>
#include <string>
#include <vector>

// Рядок ISA.uk.md §5: опкод і повний розмір у байтах (на стільки рухається PC).
struct Form {
    std::uint8_t code;
    int size;
};

// Лише ті форми, що трапляються в трьох програмах нижче. Решта ISA §5 — у вашому асемблері.
// Ключ — мнемоніка разом із регістрами, як у колонці «Мнемоніка» таблиці.
const std::map<std::string, Form> FORMS = {
    {"HALT", {0x00, 1}},     {"NOP", {0x01, 1}},      {"OUTN", {0x03, 1}},
    {"DEC A", {0x19, 1}},    {"CMP A, B", {0x1A, 1}}, {"MUL A, B", {0x1B, 1}},
    {"LOADI A,", {0x20, 2}}, {"LOADI B,", {0x21, 2}},
    {"JMP", {0x30, 3}},      {"JZ", {0x31, 3}},       {"JNZ", {0x32, 3}},
    {"PUSH A", {0x50, 1}},   {"POP B", {0x53, 1}},    {"CALL", {0x54, 3}},    {"RET", {0x55, 1}},
};

struct Line {
    std::string label;   // "" — рядок без мітки
    std::string op;      // ключ у FORMS
    std::string arg;     // число або ім'я мітки; "" — операнда немає
    std::string note;    // коментар із лістингу
};

struct Program {
    std::string name;
    std::string where;                  // звідки взято лістинг
    std::vector<Line> lines;
    std::vector<std::uint8_t> listing;  // очікувані байти — з ними звіряє дослід 09
};

const std::vector<Program> PROGRAMS = {
    {"countdown", "ISA.uk.md §9",
     {
         {"", "LOADI A,", "3", ""},
         {"loop", "OUTN", "", ""},
         {"", "DEC A", "", ""},
         {"", "JNZ", "loop", ""},
         {"", "HALT", "", ""},
     },
     {0x20, 0x03, 0x03, 0x19, 0x32, 0x02, 0x00, 0x00}},

    // Байтів у Notes 08 §4 немає, лише текст; пораховано за ISA §5: JMP — 3, NOP — 1, тож done = 0x0004.
    {"forward", "Notes 08 §4",
     {
         {"", "JMP", "done", ""},
         {"", "NOP", "", ""},
         {"done", "HALT", "", ""},
     },
     {0x30, 0x04, 0x00, 0x01, 0x00}},

    {"fact", "ISA.uk.md §6",
     {
         {"", "LOADI A,", "5", "n = 5"},
         {"", "CALL", "fact", ""},
         {"", "OUTN", "", "надрукує 120"},
         {"", "HALT", "", ""},
         {"fact", "LOADI B,", "0", ""},
         {"", "CMP A, B", "", "n == 0 ?"},
         {"", "JZ", "base", ""},
         {"", "LOADI B,", "1", ""},
         {"", "CMP A, B", "", "n == 1 ?"},
         {"", "JZ", "base", ""},
         {"", "PUSH A", "", "зберегти n"},
         {"", "DEC A", "", ""},
         {"", "CALL", "fact", "A = fact(n-1)"},
         {"", "POP B", "", "B = збережене n"},
         {"", "MUL A, B", "", "A = fact(n-1) * n"},
         {"", "RET", "", ""},
         {"base", "LOADI A,", "1", ""},
         {"", "RET", "", ""},
     },
     {0x20, 0x05, 0x54, 0x07, 0x00, 0x03, 0x00, 0x21, 0x00, 0x1A, 0x31, 0x1B, 0x00, 0x21, 0x01,
      0x1A, 0x31, 0x1B, 0x00, 0x50, 0x19, 0x54, 0x07, 0x00, 0x53, 0x1B, 0x55, 0x20, 0x01, 0x55}},
};

// Знайти програму за назвою; nullptr — немає такої.
inline const Program* find_program(const std::string& name) {
    for (const Program& p : PROGRAMS)
        if (p.name == name) return &p;
    return nullptr;
}

// "LOADI A, 5", "fact:  LOADI B, 0" — як рядок виглядав у тексті.
inline std::string source(const Line& l) {
    std::string s = l.label.empty() ? "" : l.label + ":";
    while (s.size() < 7) s += ' ';
    s += l.op;
    if (!l.arg.empty()) s += " " + l.arg;
    return s;
}
