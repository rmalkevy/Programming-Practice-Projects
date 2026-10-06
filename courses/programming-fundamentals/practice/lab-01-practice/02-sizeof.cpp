// Дослід 2: тип — це розмір. Скільки байтів і який діапазон на ЦІЙ машині.
// Запуск: ./run.sh 02
// Lab 01, Теорія §2 · Notes 01, §1
#include "common.hpp"
#include <cstddef>
#include <limits>

template <typename T>
void row(const std::string& name, const std::string& note = "") {
    std::cout << "  " << pad(name, 15) << std::setw(5) << sizeof(T) << std::setw(6) << sizeof(T) * 8
              << "  " << std::setw(22) << +std::numeric_limits<T>::lowest()
              << "  " << std::setw(22) << +std::numeric_limits<T>::max();
    if (!note.empty()) std::cout << "  " << note;
    std::cout << '\n';
}

int main() {
    // Заголовок: кириличні слова вирівнюємо вручну, бо setw рахує байти, а не літери.
    std::cout << "  " << pad("тип", 15) << " байт бітів" << std::string(16, ' ') << "найменше"
              << std::string(15, ' ') << "найбільше\n";
    row<char>("char", "← знаковий чи ні, вирішує платформа");
    row<std::uint8_t>("std::uint8_t", "← комірка ember");
    row<std::int8_t>("std::int8_t");
    row<std::uint16_t>("std::uint16_t", "← адреса ember");
    row<short>("short");
    row<int>("int");
    row<unsigned>("unsigned");
    row<long>("long", "← на Windows 4");
    row<long long>("long long");
    row<std::size_t>("std::size_t");
    row<float>("float", "~" + std::to_string(std::numeric_limits<float>::digits10) + " цифр");
    row<double>("double", "~" + std::to_string(std::numeric_limits<double>::digits10) + " цифр");
    std::cout << "  " << pad("void*", 15) << std::setw(5) << sizeof(void*) << std::setw(6)
              << sizeof(void*) * 8 << "  ← ширина адреси (Lab 3)\n";
}
