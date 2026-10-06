// Дослід 5: C-рядок — це байти до першого нуля. Слово з n літер займає n + 1 байт.
// Запуск: ./run.sh 05 HI      — у буфері char s[4] вистачає місця на '\0'
//         ./run.sh 05 ABC     — рівно впритул
//         ./run.sh 05 ABCD    — нуль уже не вміщається: що зробить strlen?
// Lab 05, Теорія §3 · Notes 05, §3
#include "common.hpp"
#include <cstring>

const int N = 4;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "usage: ./run.sh 05 <слово латиницею>   наприклад: HI\n";
        return 1;
    }
    const char* word = argv[1];

    char s[N];
    int i = 0;
    for (; i < N && word[i] != '\0'; ++i) s[i] = word[i];   // скопіювати, скільки влізе
    if (i < N) s[i] = '\0';                                // і нуль — якщо для нього лишилось місце
    for (int k = i + 1; k < N; ++k) s[k] = '\0';

    std::cout << "char s[" << N << "];  слово \"" << word << "\", літер скопійовано: " << i << "\n\n";
    std::cout << "  індекс:";
    for (int k = 0; k < N; ++k) std::cout << "    " << (char)('0' + k);   // '0' + k — це цифра k
    std::cout << "\n  байт:  ";
    for (int k = 0; k < N; ++k) std::cout << std::setw(5) << (int)(unsigned char)s[k];
    std::cout << "\n  символ:";
    for (int k = 0; k < N; ++k) {
        if (s[k] == '\0') std::cout << "   \\0";
        else std::cout << "    " << s[k];
    }
    std::cout << "\n\n  sizeof(s) = " << sizeof(s) << "   (це розмір буфера, він не залежить від слова)\n";
    std::cout << "  strlen(s) = " << std::flush << std::strlen(s) << "   (рахує до першого нуля)\n";
    std::cout << "  s         = \"" << s << "\"\n";
}
