// Дослід 2: ті самі три поля в іншому порядку займають різну кількість байтів.
// Запуск: ./run.sh 02   — три порядки полів op, addr, imm і карта байтів кожного
// Lab 06, Теорія §1 · Notes 06, §1
#include "common.hpp"
#include <cstddef>
#include <vector>

using Byte = std::uint8_t;

struct OpAddrImm { Byte op; std::uint16_t addr; Byte imm; };
struct AddrOpImm { std::uint16_t addr; Byte op; Byte imm; };
struct OpImmAddr { Byte op; Byte imm; std::uint16_t addr; };

struct Field { std::string name; std::size_t offset, size; };

// Кожен байт структури підписуємо ім'ям поля; нічий байт — ··
void show(const std::string& decl, std::size_t total, const std::vector<Field>& fields) {
    std::size_t sum = 0;
    for (const Field& f : fields) sum += f.size;
    std::cout << "  " << pad(decl, 44) << "sizeof = " << total << "  (полів " << sum << ")\n    ";
    for (std::size_t i = 0; i < total; ++i) {
        std::string who = "··";
        for (const Field& f : fields)
            if (i >= f.offset && i < f.offset + f.size) who = f.name;
        std::cout << std::setw(2) << i << ':' << pad(who, 5);
    }
    std::cout << "\n\n";
}

int main() {
    std::cout << "alignof(Byte) = " << alignof(Byte) << ", alignof(uint16_t) = " << alignof(std::uint16_t)
              << ": uint16_t стає лише на парне зміщення\n\n";

    show("{ Byte op; uint16_t addr; Byte imm; }", sizeof(OpAddrImm),
         {{"op", offsetof(OpAddrImm, op), 1}, {"addr", offsetof(OpAddrImm, addr), 2},
          {"imm", offsetof(OpAddrImm, imm), 1}});
    show("{ uint16_t addr; Byte op; Byte imm; }", sizeof(AddrOpImm),
         {{"op", offsetof(AddrOpImm, op), 1}, {"addr", offsetof(AddrOpImm, addr), 2},
          {"imm", offsetof(AddrOpImm, imm), 1}});
    show("{ Byte op; Byte imm; uint16_t addr; }", sizeof(OpImmAddr),
         {{"op", offsetof(OpImmAddr, op), 1}, {"addr", offsetof(OpImmAddr, addr), 2},
          {"imm", offsetof(OpImmAddr, imm), 1}});

    std::cout << "Масив із 8 таких записів: " << sizeof(OpAddrImm[8]) << " проти "
              << sizeof(AddrOpImm[8]) << " байтів.\n";
}
