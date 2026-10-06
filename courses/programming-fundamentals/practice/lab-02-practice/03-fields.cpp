// Дослід 3: маска і зсув. Як із одного байта дістати поля і як керувати одним бітом.
// Запуск: ./run.sh 03 0xB9        — розібрати байт на поля
//         ./run.sh 03 0xB9 3      — плюс виставити / скинути / перемкнути / перевірити біт 3
// Lab 02, Теорія §4–5 · Notes 02, §3
#include "common.hpp"

// Показати один крок: вираз, його біти й (необов'язково) що з цього вийшло.
void line(const std::string& expr, std::uint8_t v, const std::string& note = "") {
    std::cout << "  " << std::left << std::setw(16) << expr << std::right
              << bits(v) << "  " << note << '\n';
}

// Навчальний формат із теорії §4:  opcode:4 | dest:2 | src:2
void fields(std::uint8_t ins) {
    std::cout << "Формат opcode:4 | dest:2 | src:2\n";
    line("ins", ins, hex(ins));
    std::cout << '\n';

    std::uint8_t opcode = (ins >> 4) & 0x0F;
    line("ins >> 4", ins >> 4);
    line("  & 0x0F", opcode, "opcode = " + std::to_string(opcode));

    std::uint8_t dest = (ins >> 2) & 0x03;
    line("ins >> 2", ins >> 2, "← зверху ще висить opcode");
    line("  & 0x03", dest, "dest = " + std::to_string(dest));

    std::uint8_t src = ins & 0x03;
    line("ins", ins, "← зсувати не треба, поле вже внизу");
    line("  & 0x03", src, "src = " + std::to_string(src));
}

// Справжня нумерація ember (ISA.uk.md §4): старший півбайт — група.
void ember_group(std::uint8_t op) {
    const char* groups[] = {"керування й вивід", "ALU", "пересилання даних", "стрибки",
                            "екран", "стек і виклики", "система"};
    int group = (op >> 4) & 0x0F;
    int index = op & 0x0F;
    std::cout << "\nЯк опкод ember: group = (op >> 4) & 0x0F = " << group
              << ", index = op & 0x0F = " << index << "  →  ";
    if (group <= 6) std::cout << "група 0x" << std::hex << std::uppercase << group
                              << "_ (" << groups[group] << ")" << std::dec;
    else std::cout << "вільна група — для ваших розширень";

    // Інструкції Lab 2: група 0x0_ (індекси 0–1) і група 0x1_ (індекси 0–9).
    const char* ctrl[] = {"HALT", "NOP"};
    const char* alu[] = {"ADD", "SUB", "AND", "OR", "XOR", "NOT", "SHL", "SHR", "INC", "DEC"};
    if (group == 0 && index <= 1) std::cout << ", це " << ctrl[index];
    if (group == 1 && index <= 9) std::cout << ", це " << alu[index];
    std::cout << '\n';
}

// Трійка операцій над одним бітом (теорія §4) плюс перемикання.
void one_bit(std::uint8_t flags, int n) {
    std::uint8_t mask = (std::uint8_t)(1u << n);
    std::cout << "\nБіт " << n << ", маска 1u << " << n << ":\n";
    line("mask", mask, hex(mask));
    line("~mask", (std::uint8_t)~mask);
    std::cout << '\n';
    line("flags", flags);
    line("flags |  mask", flags | mask, "виставити");
    line("flags & ~mask", flags & ~mask, "скинути");
    line("flags ^  mask", flags ^ mask, "перемкнути");
    line("flags &  mask", flags & mask,
         std::string("перевірити → ") + ((flags & mask) != 0 ? "виставлений" : "скинутий"));
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 03 <байт> [номер біта 0..7]   наприклад: 0xB9 3\n";
        return 1;
    }
    try {
        std::uint8_t x = (std::uint8_t)parse_number(argv[1]);
        fields(x);
        ember_group(x);
        if (argc >= 3) {
            long n = parse_number(argv[2]);
            if (n < 0 || n > 7) {
                std::cout << "\nномер біта — від 0 до 7\n";
                return 1;
            }
            one_bit(x, (int)n);
        }
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
}
