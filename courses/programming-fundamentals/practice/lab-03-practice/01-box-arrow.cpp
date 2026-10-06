// Дослід 1: коробка і стрілка. x — ім'я, &x — місце, p — папірець із номером місця.
// Запуск: ./run.sh 01 65 66     — x = 65, потім *p = 66
// Lab 03, Теорія §1 · Notes 03, §1
#include "common.hpp"

void row(const std::string& expr, const std::string& value, const std::string& note) {
    std::cout << "  " << std::left << std::setw(6) << expr << std::setw(16) << value
              << std::right << note << '\n';
}

std::string addr(const void* p) {
    std::ostringstream out;
    out << p;
    return out.str();
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 01 <x> <нове значення>   наприклад: 65 66\n";
        return 1;
    }
    int x = 0, v = 0;
    try {
        x = (int)parse_number(argv[1]);
        v = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    int* p = &x;
    std::cout << "int x = " << x << ";\nint* p = &x;\n\n";
    row("x", std::to_string(x), "що лежить у коробці");
    row("&x", addr(&x), "де лежить коробка");
    row("p", addr(p), "те саме число, що &x: p тримає адресу");
    row("*p", std::to_string(*p), "піти за адресою і взяти, що там");
    row("&p", addr(&p), "у p теж є своя коробка, і в неї своя адреса");

    *p = v;   // пишемо не в p, а туди, куди p вказує
    std::cout << "\n*p = " << v << ";\n\n";
    row("x", std::to_string(x), "змінився, хоча імені x у рядку вище немає");
    row("p", addr(p), "не змінився: стрілка та сама");

    // Стрілку можна перевести на іншу коробку.
    int y = 0;
    p = &y;
    *p = v + 1;
    std::cout << "\nint y = 0;\np = &y;\n*p = " << v + 1 << ";\n\n";
    row("x", std::to_string(x), "уже не чіпаємо");
    row("y", std::to_string(y), "");
    row("p", addr(p), "тепер дорівнює &y");
}
