// Дослід 4: список токенів росте вузол за вузлом — append, обхід через next, destroy. Видно адреси кожного вузла.
// Запуск: ./run.sh 04 ADD A B         — три вузли, як у Notes 08 §3
//         ./run.sh 04 leak ADD A B    — те саме без destroy: хто помітить витік?
// Lab 08, Теорія §3 · Notes 08, §3 · new і delete — Lab 6
#include "common.hpp"

struct Token {
    std::string text;
    Token* next = nullptr;
};

void append(Token*& head, Token*& tail, const std::string& t) {
    auto* n = new Token{t, nullptr};
    if (!head) head = tail = n;
    else { tail->next = n; tail = n; }
}

void destroy(Token* head) {
    while (head) { Token* n = head->next; delete head; head = n; }
}

std::string addr(const void* p) {
    if (!p) return "nullptr";
    std::ostringstream out;
    out << p;
    return out.str();
}

int main(int argc, char* argv[]) {
    int from = 1;
    bool leak = argc > 1 && std::string(argv[1]) == "leak";
    if (leak) from = 2;
    if (argc <= from) {
        std::cout << "usage: ./run.sh 04 [leak] <слова ...>   наприклад: ADD A B\n";
        return 1;
    }

    Token *head = nullptr, *tail = nullptr;
    std::cout << "старт:  head = " << addr(head) << ", tail = " << addr(tail) << "\n\n";
    for (int i = from; i < argc; ++i) {
        append(head, tail, argv[i]);
        std::cout << "append(\"" << argv[i] << "\"):  head = " << addr(head) << ", tail = " << addr(tail) << '\n';
    }

    std::cout << "\nобхід: for (Token* p = head; p; p = p->next)\n";
    std::cout << "  вузол за адресою      text    next\n";
    for (Token* p = head; p; p = p->next)
        std::cout << "  " << std::left << std::setw(20) << addr(p) << "  " << std::setw(6) << p->text << "  "
                  << addr(p->next) << std::right << '\n';

    if (leak) {
        std::cout << "\ndestroy(head) не викликано: вузли лишились у купі, а вказівника на них уже ніхто не тримає.\n";
        return 0;
    }
    destroy(head);
    std::cout << "\ndestroy(head): усі вузли звільнено. head досі " << addr(head)
              << " — це адреса, якої вже немає; розіменовувати її не можна.\n";
}
