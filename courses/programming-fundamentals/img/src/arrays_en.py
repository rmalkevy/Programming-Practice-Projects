"""Translate img/arrays.uk.svg into English: python3 arrays_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()

# Text between tags: Ukrainian fragment -> English. Each must occur at least once.
T = {
    "Масиви, екран і рядки": "Arrays, the screen and strings",
    "Масив — це пам'ять підряд плюс правило, де лежить i-й елемент. Решта — наслідки цього правила.":
        "An array is memory in a row plus a rule for where element i lives. The rest follows from that rule.",
    "— розділ Теорії Lab 05": "— section of the Lab 05 theory",
    "значення": "value", "за краєм масиву": "past the end", "нуль": "zero",
    "1. Масив — пам'ять плюс правило": "1. An array is memory plus a rule",
    "// решта — нулі": "// the rest are zeros",
    " — це ": " is ",
    ": адреса першого елемента плюс ": ": the address of the first element plus ",
    " кроків (Lab 3).": " steps (Lab 3).",
    " — уже не масив: ASan зупинить програму.": " is no longer the array: ASan stops the program.",
    "У функцію ": "Passed to a function, ",
    " приходить як вказівник, тому розмір передають окремо:": " arrives as a pointer, so the size is passed separately:",
    "2. Два виміри — це один вимір і крок": "2. Two dimensions are one dimension and a stride",
    "рядок лежить у пам'яті поруч": "a row sits together in memory",
    "у пам'яті:": "in memory:",
    "Обхід рядками йде підряд; колонками — стрибками по 4 елементи": "Walking by rows goes in order; by columns it jumps 4 elements",
    "(16 байтів для ": "(16 bytes for ",
    "). Переплутана формула ": "). The swapped formula ",
    " дає інший елемент.": " gives a different element.",
    "3. Піксель — це біт: екран 64 × 32 у 256 байтах": "3. A pixel is a bit: a 64 × 32 screen in 256 bytes",
    "Піксель ": "Pixel ",
    ". Формули — з ISA §7; ті самі числа друкує ": ". Formulas from ISA §7; the same numbers come from ",
    " у практиці Lab 05.": " in the Lab 05 practice.",
    "піксель ": "pixel ",
    ": рядок 2, байт 1 цього рядка": ": row 2, byte 1 of that row",
    "8 байтів на рядок × 32 рядки, з ": "8 bytes per row × 32 rows, from ",
    " — пікселі x = 8…15 рядка 2": " — pixels x = 8…15 of row 2",
    "біт": "bit",
    "адреса = 0xA00 + y·8 + x/8": "address = 0xA00 + y·8 + x/8",
    "       = 0xA00 + 16 + 1 = 0xA11": "        = 0xA00 + 16 + 1 = 0xA11",
    "біт    = 7 − x%8 = 7 − 5 = 2": "bit     = 7 − x%8 = 7 − 5 = 2",
    "маска  = 1 &lt;&lt; 2 = 0x04": "mask    = 1 &lt;&lt; 2 = 0x04",
    "горить = (mem[0xA11] &gt;&gt; 2) &amp; 1": "lit     = (mem[0xA11] &gt;&gt; 2) &amp; 1",
    "Засвітити ": "Set ",
    ", погасити ": ", clear ",
    ": трійка з Lab 2.": ": the Lab 2 trio.",
    "Забули «7 −»: біт 5 замість 2": "Forgot the “7 −”: bit 5 instead of 2",
    "з «7 −»: світиться x = 13": "with “7 −”: x = 13 lights up",
    "без: x = 10 — дзеркально у вісімці": "without: x = 10, mirrored in its byte",
    "Рядок 2 у дампі, з ": "Row 2 in the dump, from ",
    "4. Рядок: довжина за домовленістю": "4. A string: length by convention",
    "strlen іде до першого 0": "strlen walks to the first 0",
    "sizeof(s) = 4 — буфер": "sizeof(s) = 4, the buffer",
    "\"ABCD\" у char s[4]": "\"ABCD\" in char s[4]",
    "нуля немає": "no zero",
    "strlen іде за край — ASan": "strlen walks off the end: ASan",
    "5. Бульбашка: міняємо сусідів": "5. Bubble sort: swap neighbours",
    "прохід 1": "pass 1", "прохід 2": "pass 2", "прохід 3": "pass 3",
    "обмін →": "swap →",
    "без обміну": "no swap",
    "6 порівнянь, 4 обміни. Після проходу найбільше з решти — на місці.":
        "6 comparisons, 4 swaps. After each pass the largest of the rest is in place.",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)

for ua, en in [("Заголовок і легенда", "Title and legend"), ("1. Масив", "1. Array"), ("2. Два виміри", "2. Two dimensions"),
               ("3. Екран", "3. Screen"), ("4. Рядки", "4. Strings"), ("5. Бульбашка", "5. Bubble sort")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Five panels for the Lab 05 theory. 1: Byte buf[8] = {1, 2, 3}, eight cells with the rest zero; buf[i] is "
        "*(buf + i); buf[8] is past the end. 2: int m[3][4] as a table and as memory, k = r * 4 + c, m[1][2] is k = 6. "
        "3: a 64 × 32 screen in 256 bytes from 0xA00: pixel (13, 2) is byte 0xA11, bit 2, mask 0x04; without “7 −” "
        "x = 10 lights up instead. 4: char s[4] = \"HI\" and strlen up to the first zero; \"ABCD\" with no room for "
        "the zero. 5: bubble sort on 4 1 3 2: six comparisons, four swaps.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
s = s.replace('<title id="title">Масиви, екран і рядки</title>', '<title id="title">Arrays, the screen and strings</title>')
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
