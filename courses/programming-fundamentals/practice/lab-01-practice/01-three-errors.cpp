// Дослід 1: три види помилок. Компілятор відмовився, компілятор підозрює, програма вже біжить.
// Запуск: ./run.sh 01 10 2                      — усе гаразд
//         FLAGS=-DSYNTAX ./run.sh 01 10 2       — синтаксична помилка: програми не існує
//         FLAGS=-DWARNING ./run.sh 01 10 2      — попередження, яке -Werror робить помилкою
//         FLAGS=-DWARNING NO_WERROR=1 ./run.sh 01 10 2   — те саме попередження, але програма є
//         ./run.sh 01 10 0                      — помилка виконання: ділення на нуль
// Lab 01, Теорія §1 · errors.notes.md
#include "common.hpp"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 01 <a> <b>   наприклад: 10 2, потім 10 0\n";
        return 1;
    }
    int a = 0, b = 0;
    try {
        a = (int)parse_number(argv[1]);
        b = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

#ifdef SYNTAX
    int c = a + b      // забули крапку з комою: компілятор не перекладе цей текст
#endif
#ifdef WARNING
    int unused = a;    // законно, але підозріло: навіщо змінна, яку ніхто не читає?
#endif

    // b приходить з командного рядка, тож компілятор не знає, що це нуль. Знає лише UBSan.
    std::cout << a << " / " << b << " = " << std::flush;
    std::cout << a / b << '\n';
    std::cout << "програма дійшла до кінця\n";
}
