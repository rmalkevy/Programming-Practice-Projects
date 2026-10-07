"""Translate img/types.uk.svg into English: python3 types_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()

# Text between tags: Ukrainian fragment -> English. Each must occur at least once.
T = {
    "Коробка байтів: помилки й типи": "A box of bytes: errors and types",
    "Ви пишете текст, машина виконує байти. Тип каже, скільки байтів і що з ними можна робити.":
        "You write text; the machine runs bytes. A type says how many bytes and what you may do with them.",
    "— розділ Теорії Lab 01": "— section of the Lab 01 theory",
    "1. Виконується не той текст, який ви написали": "1. What runs is not the text you wrote",
    "текст": "text", "компілятор": "compiler", "програма": "program", "машинний код": "machine code",
    "запуск": "run", "ASan, UBSan стежать": "ASan, UBSan watching", "вивід": "output",
    "синтаксична помилка": "syntax error", "попередження": "warning", "помилка виконання": "runtime error",
    "компілятор відмовився перекладати — програми немає": "the compiler refused to translate: no program",
    "з -Werror підозра стає помилкою — програми теж немає": "with -Werror a suspicion is an error: no program either",
    "програма є і вже біжить — ловить санітайзер": "the program exists and runs; a sanitizer catches it",
    "2. Тип — це розмір і набір операцій": "2. A type is a size and a set of operations",
    "Числа — з ": "Numbers from ",
    " на 64-бітному Mac. Своє число друкуйте, а не завчайте.": " on a 64-bit Mac. Print your own, don't memorise.",
    "0 … 255 — комірка ember": "0 … 255, an ember cell",
    "0 … 65535 — адреса ember": "0 … 65535, an ember address",
    "~15 десяткових цифр": "~15 decimal digits",
    "ширина адреси (Lab 3)": "the width of an address (Lab 3)",
    "Один байт — чотири записи:": "One byte, four notations:",
    "ті самі біти; розповідь веде тип": "the same bits; the type tells the story",
    ": велика й мала літера різняться одним бітом 5.": ": upper and lower case differ in one bit, bit 5.",
    "3. Переповнення, рухома кома й інша брехня": "3. Overflow, floating point and other lies",
    ", +1: загортається, і це визначено": ", +1: wraps around, and that is defined",
    ", +1 після ": ", +1 past ",
    ": невизначена поведінка": ": undefined behavior",
    "Компілятор може вважати, що цього не буває: ": "The compiler may assume it never happens: ",
    " — «завжди true».": " is “always true”.",
    ": більшість десяткових дробів не вміщаються": ": most decimal fractions don't fit",
    "; з допуском ": "; with a tolerance ",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)

for ua, en in [("Заголовок і легенда", "Title and legend"), ("1. Три види помилок", "1. Three kinds of errors"),
               ("2. Тип — це розмір", "2. A type is a size"), ("3. Переповнення й рухома кома", "3. Overflow and floating point")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Three panels for the Lab 01 theory. 1: the path from text to a run and where three kinds of errors stop it: "
        "a syntax error and a warning under -Werror stop in the compiler, so there is no program; a runtime error happens "
        "while it runs, like 10 / 0 under UBSan. 2: a type is a size: uint8_t, uint16_t, int, double and void* as 1, 2, "
        "4, 8 and 8 bytes with their ranges; the byte 01000001 is 65, 0x41 and 'A', and 'A' ^ 32 is 'a'. 3: uint8_t wraps "
        "255 → 0, int at INT_MAX + 1 is undefined behavior; 0.1 + 0.2 is not 0.3.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
s = s.replace('<title id="title">Коробка байтів: помилки й типи</title>', '<title id="title">A box of bytes: errors and types</title>')
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
