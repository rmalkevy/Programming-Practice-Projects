// Дослід 6: ADD, зібраний із бітів. Так додає суматор у справжньому ALU.
// Запуск: ./run.sh 06 200 100       — додати, по рядку на кожен біт
//         ./run.sh 06 sub 5 7       — відняти тим самим суматором: a + ~b + 1
// Lab 02, Теорія §2, §5 · Notes 02, §5
#include "common.hpp"

// Повний суматор на 8 бітів. Біт суми — XOR трьох бітів, перенесення — «хоча б два з трьох».
std::uint8_t add8(std::uint8_t a, std::uint8_t b, bool carry_in, bool& carry_out) {
    std::cout << "біт  a  b  перенос→  сума  →перенос\n";
    std::uint8_t sum = 0;
    bool carry = carry_in;
    for (int i = 0; i < 8; ++i) {
        bool ai = (a >> i) & 1;
        bool bi = (b >> i) & 1;
        bool s = ai ^ bi ^ carry;
        bool next = (ai && bi) || (ai && carry) || (bi && carry);
        std::cout << " " << i << "   " << ai << "  " << bi << "      " << carry
                  << "      " << s << "       " << next << '\n';
        if (s) sum = (std::uint8_t)(sum | (1u << i));
        carry = next;
    }
    carry_out = carry;
    return sum;
}

void flags(std::uint8_t r, bool c) {
    std::cout << "Z=" << (r == 0) << " N=" << ((r >> 7) & 1) << " C=" << c << '\n';
}

int main(int argc, char* argv[]) {
    bool sub = argc >= 2 && std::string(argv[1]) == "sub";
    int first = sub ? 2 : 1;
    if (argc < first + 2) {
        std::cout << "usage: ./run.sh 06 <a> <b>   або   ./run.sh 06 sub <a> <b>\n";
        return 1;
    }
    std::uint8_t a = 0, b = 0;
    try {
        a = (std::uint8_t)parse_number(argv[first]);
        b = (std::uint8_t)parse_number(argv[first + 1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    if (!sub) {
        bool c = false;
        std::uint8_t r = add8(a, b, false, c);
        std::cout << "\n    " << bits(a) << "  " << std::setw(3) << (int)a
                  << "\n+   " << bits(b) << "  " << std::setw(3) << (int)b
                  << "\n= " << c << ' ' << bits(r) << "  " << std::setw(3) << (int)r
                  << "   (дев'ятий біт ліворуч — це C)\n\n";
        std::cout << "по бітах:       " << (int)r << '\n';
        std::cout << "uint8_t(a + b): " << (int)(std::uint8_t)(a + b) << '\n';
        std::cout << "int a + b:      " << (a + b) << " = 256·" << c << " + " << (int)r << '\n';
        flags(r, c);
    } else {
        // Віднімання — це додавання від'ємного: a - b = a + (~b + 1).
        // «+1» заходить як початкове перенесення, тож окремий віднімач не потрібен.
        std::uint8_t nb = (std::uint8_t)~b;
        std::cout << "a - b = a + ~b + 1,   ~b = " << bits(nb) << "\n"
                  << "(у стовпчику b нижче стоїть ~b, а перенос на старті — та сама +1)\n\n";
        bool c = false;
        std::uint8_t r = add8(a, nb, true, c);
        bool borrow = !c;   // суматор каже «перенесення», ISA хоче «позику» — це протилежне
        std::cout << "\nпо бітах:       " << (int)r << "  (як int8_t " << (int)(std::int8_t)r << ")\n";
        std::cout << "uint8_t(a - b): " << (int)(std::uint8_t)(a - b) << '\n';
        std::cout << "перенос суматора " << c << " → позика = " << borrow << '\n';
        flags(r, borrow);
    }
}
