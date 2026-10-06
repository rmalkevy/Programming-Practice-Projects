// Дослід 5: `switch` без `break` провалюється в наступний `case`. Декодер, у якому забули один break.
// Запуск: ./run.sh 05 18        — INC A
//         ./run.sh 05 19        — DEC A
//         ./run.sh 05 77        — невідомий опкод
// Опкод пишеться, як у дампі: шістнадцятковий, без 0x.
// clang це збирає мовчки. gcc з -Wextra попереджає про провалювання, і -Werror зупиняє
// збірку — з gcc запускайте з NO_WERROR=1.
// Lab 04, Теорія §2, M1 · Notes 04, §3
#include "common.hpp"

// Зламаний декодер: після INC немає break.
int broken(std::uint8_t op, int a, std::string& log) {
    switch (op) {
    case 0x18:                 // INC A
        a = a + 1;
        log += "INC ";
    case 0x19:                 // DEC A   ← сюди INC провалюється
        a = a - 1;
        log += "DEC ";
        break;
    case 0x15:                 // NOT A
        a = ~a & 0xFF;
        log += "NOT ";
        break;
    default:
        log += "unknown ";
    }
    return a;
}

// Виправлений: кожен case закінчується break, default — помилка, а не тихий NOP.
int fixed(std::uint8_t op, int a, std::string& log) {
    switch (op) {
    case 0x18:
        a = a + 1;
        log += "INC ";
        break;
    case 0x19:
        a = a - 1;
        log += "DEC ";
        break;
    case 0x15:
        a = ~a & 0xFF;
        log += "NOT ";
        break;
    default:
        log += "unknown opcode " + hex(op);
    }
    return a;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <опкод> [A]   наприклад: 18, 19, 15, 77\n";
        return 1;
    }
    std::uint8_t op = 0;
    int a = 5;
    try {
        op = (std::uint8_t)parse_number(std::string("0x") + argv[1]);
        if (argc >= 3) a = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    std::cout << "op = " << hex(op) << ", A = " << a << "\n\n";
    std::string log;
    int r = broken(op, a, log);
    std::cout << "  без break:  A = " << std::setw(3) << r << "   виконано: " << log << '\n';
    log.clear();
    r = fixed(op, a, log);
    std::cout << "  з break:    A = " << std::setw(3) << r << "   виконано: " << log << '\n';
}
