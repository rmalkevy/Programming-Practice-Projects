// Дослід 4: enum class не змішується з int; приведення (Op)byte нічого не перевіряє — це робить switch.
// Запуск: ./run.sh 04 0x18 0x19 0x77   — розібрати байти як Op
//         FLAGS=-DMIX ./run.sh 04      — ті самі рядки без приведення: помилка компілятора
// Lab 06, Теорія §2, M1 · Notes 06, §2
#include "common.hpp"
#include <vector>

using Byte = std::uint8_t;

// Лише кілька опкодів для показу. Повний перелік зі значеннями з ISA.uk.md — ваш M1.
enum class Op : Byte {
    Halt = 0x00,
    Nop  = 0x01,
    Inc  = 0x18,
    Dec  = 0x19,
    Jnz  = 0x32,
};

// Старий спосіб для порівняння: звичайний enum мовчки стає int.
enum OldOp { OLD_INC = 0x18, OLD_DEC = 0x19 };

std::string name(Op op) {
    switch (op) {
    case Op::Halt: return "HALT";
    case Op::Nop:  return "NOP";
    case Op::Inc:  return "INC A";
    case Op::Dec:  return "DEC A";
    case Op::Jnz:  return "JNZ";
    default:       return "unknown opcode";
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 04 <байти ...>   наприклад: 0x18 0x19 0x77\n";
        return 1;
    }
    std::vector<Byte> bytes;
    try {
        for (int i = 1; i < argc; ++i) bytes.push_back((Byte)parse_number(argv[i]));
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

#ifdef MIX
    Op wrong = 0x18;        // int → Op без приведення
    int raw = Op::Inc;      // Op → int без приведення
    if (wrong == 0x18) std::cout << raw << '\n';
#endif

    int old = OLD_INC + 1;   // звичайний enum: компілятор мовчить
    std::cout << "звичайний enum: OLD_INC + 1 = " << old << " — це вже просто int, і ніхто не заперечив\n\n";

    std::cout << "  " << pad("байт", 7) << pad("(Op)байт", 11) << "switch\n";
    for (Byte b : bytes) {
        Op op = (Op)b;                       // приведення: просто ті самі біти з іншим типом
        std::cout << "  " << pad(hex(b), 7) << pad(std::to_string((int)op), 11) << name(op) << '\n';
    }
    std::cout << "\n(Op)байт збереже будь-яке число 0…255, навіть те, якому немає імені.\n"
                 "Чи це справжній опкод, вирішує лише default у switch.\n";
}
