// Дослід 6: один new, три способи його закінчити — правильно, читання після delete, подвійний delete.
// Запуск: ./run.sh 06 ok 42       — new, читання, delete, p = nullptr
//         ./run.sh 06 uaf 42      — читання після delete: звіт ASan heap-use-after-free
//         ./run.sh 06 double 42   — delete двічі: звіт ASan attempting double-free
// Lab 06, Теорія §3, M3 · Notes 06, §3 · errors.notes.md §3
#include "common.hpp"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "usage: ./run.sh 06 <ok|uaf|double> <число>   наприклад: uaf 42\n";
        return 1;
    }
    std::string mode = argv[1];
    if (mode != "ok" && mode != "uaf" && mode != "double") {
        std::cout << "режим має бути ok, uaf або double\n";
        return 1;
    }
    int value = 0;
    try {
        value = (int)parse_number(argv[2]);
    } catch (const std::exception&) {
        std::cout << "не можу прочитати як число\n";
        return 1;
    }

    int* p = new int{value};
    std::cout << "new int{" << value << "}: p = " << p << ", *p = " << *p << std::endl;

    delete p;
    std::cout << "delete p:  p = " << p << " — адреса та сама, а об'єкта вже немає" << std::endl;

    if (mode == "ok") {
        p = nullptr;
        std::cout << "p = nullptr: тепер видно, що p нікуди не вказує" << std::endl;
    } else if (mode == "uaf") {
        std::cout << "читаю *p після delete..." << std::endl;
        std::cout << "*p = " << *p << std::endl;     // завислий вказівник
    } else {
        std::cout << "delete p ще раз..." << std::endl;
        delete p;                                       // подвійне звільнення
    }
    std::cout << "кінець main" << std::endl;
}
