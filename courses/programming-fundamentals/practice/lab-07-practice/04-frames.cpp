// Дослід 4: у кожного виклику fact свій кадр і своє n — інша коробка за іншою адресою.
// Запуск: ./run.sh 04 3     — fact(3) із друком туди й назад, як у Notes §2
//         ./run.sh 04 6
// Lab 07, Теорія §1, §3 · Notes 07, §2
#include "common.hpp"

const char* first_n = nullptr;   // адреса n у найзовнішнішому виклику — від неї рахуємо зсув

std::string indent(int n, int top) { return std::string(2 * (top - n), ' '); }

int fact(int n, int top) {
    const char* here = (const char*)&n;
    if (first_n == nullptr) first_n = here;
    std::cout << indent(n, top) << '>' << n << "   &n = " << (const void*)&n
              << "   зсув від першого n: " << (here - first_n) << '\n';
    if (n <= 1) return 1;                       // база
    int r = n * fact(n - 1, top);               // менший випадок
    std::cout << indent(n, top) << '<' << n << "   r = " << r << '\n';
    return r;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 04 <n>   наприклад: 3\n";
        return 1;
    }
    int n = 0;
    try {
        n = (int)parse_number(argv[1]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }
    if (n < 0 || n > 12) {
        std::cout << "n — від 0 до 12 (13! вже не влазить в int)\n";
        return 1;
    }

    int r = fact(n, n);
    std::cout << "fact(" << n << ") = " << r << '\n';
}
