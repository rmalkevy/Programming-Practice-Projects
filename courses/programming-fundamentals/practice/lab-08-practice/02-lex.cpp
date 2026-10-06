// Дослід 2: каркас лексера з M1 як є — токени з номерами рядків або помилка з номером рядка. number() ще заглушка.
// Запуск: ./run.sh 02 'loop: JMP loop'   — рядок із CHECKS.md
//         ./run.sh 02 bad.asm            — файл: помилка на третьому рядку
//         ./run.sh 02 hello.asm          — перше ж число: заглушка number() з каркаса
// Lab 08, Теорія §1, M1 · Notes 08, §1–2
#include "common.hpp"
#include <cctype>
#include <fstream>

// ---- token.hpp: вузол із Теорії §3 ----
struct Token {
    enum class Kind { Ident, Number, Comma, Colon, LBracket, RBracket, Newline, Eof };
    Kind kind;
    std::string text;      // або зріз (вказівник + довжина) у вихідний текст
    int line;
    Token* next;           // nullptr у кінці
};

// ---- lexer.cpp: дослівно з M1, разом із заглушкою number() ----

// Стан лексера: текст, курсор, номер рядка і список, який ми будуємо.
struct Lexer {
    const std::string& src;
    std::size_t i = 0;
    int line = 1;
    Token* head = nullptr;
    Token* tail = nullptr;
    std::string error;  // непорожній, щойно лексер щось відхилив
};

// Додати вузол у кінець списку (Notes 08 §3).
static void emit(Lexer& lx, Token::Kind kind, const std::string& text) {
    Token* t = new Token{kind, text, lx.line, nullptr};
    if (!lx.head) {
        lx.head = lx.tail = t;
    } else {
        lx.tail->next = t;
        lx.tail = t;
    }
}

// Записати помилку з номером рядка. Повертає false, щоб зручно писати
// `return fail(lx, "...");`
static bool fail(Lexer& lx, const std::string& msg) {
    lx.error = "line " + std::to_string(lx.line) + ": " + msg;
    return false;
}

void destroy(Token* head) {
    while (head) {
        Token* next = head->next;
        delete head;
        head = next;
    }
}

// ВАШЕ (Lab 8, M1). Курсор lx.i стоїть на цифрі.
// З'їсти число — `0x` і шістнадцяткові цифри, `0b` і двійкові, або десяткові —
// і видати його: emit(lx, Token::Kind::Number, текст_числа).
// Зіпсоване число — `0xGG`, `0x` без жодної цифри, `12ab` — це
// `return fail(lx, "bad number");`, а не тихий нуль.
static bool number(Lexer& lx) {
    // TODO(lab-08): поки що кожне число — помилка. Замініть цей рядок.
    return fail(lx, "number() is not written yet");
}

Token* lex(const std::string& src, std::string& error) {
    Lexer lx{src, 0, 1, nullptr, nullptr, ""};
    while (lx.i < src.size()) {
        char c = src[lx.i];
        if (c == ' ' || c == '\t' || c == '\r') {
            ++lx.i;                                   // пробіли не токени
        } else if (c == ';') {
            while (lx.i < src.size() && src[lx.i] != '\n') ++lx.i;  // коментар
        } else if (c == '\n') {
            emit(lx, Token::Kind::Newline, "\\n");
            ++lx.line;
            ++lx.i;
        } else if (std::isalpha((unsigned char)c) || c == '_') {
            std::size_t start = lx.i;
            while (lx.i < src.size() &&
                   (std::isalnum((unsigned char)src[lx.i]) || src[lx.i] == '_')) {
                ++lx.i;
            }
            emit(lx, Token::Kind::Ident, src.substr(start, lx.i - start));
        } else if (std::isdigit((unsigned char)c)) {
            if (!number(lx)) break;
        } else if (c == ',') { emit(lx, Token::Kind::Comma, ",");    ++lx.i; }
        else if (c == ':')   { emit(lx, Token::Kind::Colon, ":");    ++lx.i; }
        else if (c == '[')   { emit(lx, Token::Kind::LBracket, "["); ++lx.i; }
        else if (c == ']')   { emit(lx, Token::Kind::RBracket, "]"); ++lx.i; }
        else {
            fail(lx, std::string("unexpected character '") + c + "'");
            break;
        }
    }
    if (!lx.error.empty()) {
        destroy(lx.head);
        error = lx.error;
        return nullptr;
    }
    emit(lx, Token::Kind::Eof, "");
    return lx.head;
}

// ---- далі тільки друк: так виглядає вивід `lex` у CHECKS.md ----

std::string name(Token::Kind k) {
    switch (k) {
    case Token::Kind::Ident: return "Ident";
    case Token::Kind::Number: return "Number";
    case Token::Kind::Comma: return "Comma";
    case Token::Kind::Colon: return "Colon";
    case Token::Kind::LBracket: return "LBracket";
    case Token::Kind::RBracket: return "RBracket";
    case Token::Kind::Newline: return "Newline";
    case Token::Kind::Eof: return "Eof";
    }
    return "?";
}

std::string shown(const Token* t) {
    if (t->kind == Token::Kind::Ident || t->kind == Token::Kind::Number) return name(t->kind) + "(" + t->text + ")";
    return name(t->kind);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 02 '<рядок асемблера>'  або  ./run.sh 02 <файл.asm>\n";
        return 1;
    }
    std::string first = argv[1];
    std::string src;
    if (argc == 2 && first.size() > 4 && first.substr(first.size() - 4) == ".asm") {
        std::ifstream file(first);
        if (!file) {
            std::cout << "не можу відкрити " << first << '\n';
            return 1;
        }
        std::ostringstream all;
        all << file.rdbuf();
        src = all.str();
    } else {
        src = first;
        for (int i = 2; i < argc; ++i) src += std::string(" ") + argv[i];
        src += '\n';   // рядок із командного рядка закінчуємо так, як у файлі
    }

    std::string error;
    Token* head = lex(src, error);
    if (!head) {
        std::cout << "лексер відмовив: " << error << '\n';
        return 1;
    }

    std::cout << "рядок  вид       текст\n";
    for (Token* t = head; t; t = t->next)
        std::cout << std::setw(5) << t->line << "  " << std::left << std::setw(8) << name(t->kind) << "  "
                  << std::right << t->text << '\n';
    std::cout << '\n';
    for (Token* t = head; t; t = t->next) std::cout << shown(t) << (t->next ? " " : "\n");
    destroy(head);
}
