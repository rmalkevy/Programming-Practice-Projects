"""Translate img/control.uk.svg into English: python3 control_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()
M = '<tspan class="mono">'

# Whole lines whose word order changes in English: exact substring -> English.
R = [
    ('Операнд ' + M + 'JNZ</tspan> — ' + M + '02 00</tspan>: це ' + M + '0x0002</tspan>, молодший байт уперед.',
     'The ' + M + 'JNZ</tspan> operand ' + M + '02 00</tspan> is ' + M + '0x0002</tspan>, low byte first.'),
    ('Стрибок спрацював — ' + M + 'PC</tspan> = операнд, розмір не додається. Ні — ' + M + 'PC += 3</tspan>.',
     'Jump taken: ' + M + 'PC</tspan> = operand, the size is not added. Not taken: ' + M + 'PC += 3</tspan>.'),
    ('Вивід ' + M + '3 2 1</tspan>. ' + M + 'LOADI</tspan> прапорців не чіпає — ' + M + 'Z</tspan> виставляє ' + M + 'DEC</tspan>.',
     'Output ' + M + '3 2 1</tspan>. ' + M + 'LOADI</tspan> leaves the flags alone; ' + M + 'DEC</tspan> sets ' + M + 'Z</tspan>.'),
    (M + 'for</tspan> — це ' + M + 'while</tspan> з лічильником. ' + M + 'for (;;)</tspan> — ' + M + 'JMP</tspan> без умови:',
     M + 'for</tspan> is a ' + M + 'while</tspan> with a counter. ' + M + 'for (;;)</tspan> is a ' + M + 'JMP</tspan> with no condition,'),
    ('тому ' + M + 'run</tspan> має ліміт кроків.', 'which is why ' + M + 'run</tspan> has a step limit.'),
    ('</tspan> і ' + M + '||</tspan> можуть не дивитись праворуч', '</tspan> and ' + M + '||</tspan> may skip the right side'),
    ('з ' + M + '-Werror</tspan> не збереться.', 'with ' + M + '-Werror</tspan> it does not compile.'),
    ('4. Лінійний пошук: ' + M + 'H</tspan> — це ' + M + 'i</tspan>', '4. Linear search: ' + M + 'H</tspan> is ' + M + 'i</tspan>'),
    (M + 'H</tspan> — це ' + M + 'i</tspan>, ' + M + 'INCH</tspan> — ' + M + '++i</tspan>, ' + M + 'CMP</tspan> — ' + M + '==</tspan>, '
     + M + 'JZ</tspan> — ' + M + 'if</tspan>. Шукаємо ' + M + 'B = 0x41</tspan>.',
     M + 'H</tspan> is ' + M + 'i</tspan>, ' + M + 'INCH</tspan> is ' + M + '++i</tspan>, ' + M + 'CMP</tspan> is ' + M + '==</tspan>, '
     + M + 'JZ</tspan> is ' + M + 'if</tspan>. We look for ' + M + 'B = 0x41</tspan>.'),
    ('А якщо ' + M + '0x41</tspan> у даних немає?', 'And if ' + M + '0x41</tspan> is not in the data?'),
    (M + 'H</tspan> іде далі: ' + M + '0x0804</tspan>, ' + M + '0x0805</tspan>, … Як зупинити цикл на ' + M + 'hi</tspan>',
     M + 'H</tspan> keeps going: ' + M + '0x0804</tspan>, ' + M + '0x0805</tspan>, … How to stop the loop at ' + M + 'hi</tspan>'),
    ('5. ' + M + 'switch</tspan>: без ' + M + 'break</tspan> виконання провалюється',
     '5. ' + M + 'switch</tspan>: without ' + M + 'break</tspan>, execution falls through'),
    (M + 'default:</tspan> — невідомий опкод (' + M + '0x77</tspan>) це помилка, а не тиша.',
     M + 'default:</tspan> an unknown opcode (' + M + '0x77</tspan>) is an error, not silence.'),
]
for a, b in R:
    assert a in s, "MISSING: " + a
    s = s.replace(a, b)

# Text between tags: Ukrainian fragment -> English.
T = {
    "Керування: перевірки і стрибки": "Control: checks and jumps",
    " — це порівняння і стрибки. Цикл — це стрибок назад.": " are comparisons and jumps. A loop is a jump back.",
    "— розділ Теорії Lab 04": "— section of the Lab 04 theory",
    "стрибок назад": "jump back", "стрибок уперед": "jump forward",
    "1. Цикл — це стрибок назад: відлік 3, 2, 1 в ": "1. A loop is a jump back: counting 3, 2, 1 in ",
    "Програма з ISA §9. Трасування — ": "The program from ISA §9. Trace: ",
    " у практиці Lab 04: 11 кроків.": " in the Lab 04 practice, 11 steps.",
    "ітерація": "iteration", "OUTN друкує": "OUTN prints", "A після DEC": "A after DEC",
    "назад на 0x0002": "back to 0x0002", "далі: 0x0007, HALT": "on to 0x0007, HALT",
    "Те саме в C++ — перевірка в кінці:": "The same in C++, with the check at the end:",
    "2. Форми — це перевірки і стрибки": "2. The forms are checks and jumps",
    "then-гілка": "then branch", "else: else-гілка": "else: else branch", "тіло": "body", "top: тіло": "top: body",
    "читається, лише якщо ліва true": "read only if the left is true",
    "рахується, лише якщо ліва false": "evaluated only if the left is false",
    "ліва false → одразу false, *p не читаємо": "left false → false at once, *p is never read",
    "ліва true → одразу true, b не рахуємо": "left true → true at once, b is never evaluated",
    "Логічне — не бітове:": "Logical is not bitwise:",
    " — присвоєння, а не порівняння;": " is an assignment, not a comparison;",
    "і як сказати про промах — вирішуєте ви в M4.": "and how to report a miss is your call in M4.",
    " друкує ": " prints ",
    "без break": "without break", "з break": "with break",
    "break немає — далі": "no break, keeps going", "не виконується": "not executed",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)

for ua, en in [("Заголовок і легенда", "Title and legend"), ("1. Відлік у ember", "1. Countdown in ember"),
               ("2. Форми керування", "2. Control forms"), ("3. Коротке замикання", "3. Short-circuit"),
               ("4. Лінійний пошук", "4. Linear search")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Five panels for the Lab 04 theory. 1: the countdown from ISA §9: eight bytes of code, JNZ jumps back to 0x0002 "
        "while Z = 0, and three iterations print 3, 2, 1. 2: if/else, while and do … while as blocks with conditional "
        "jumps forward and unconditional jumps back. 3: &amp;&amp; and || skip the right side once the answer is known; "
        "1 &amp;&amp; 2 is true, 1 &amp; 2 is 0. 4: a linear search for 0x41 in the data 10 20 41 30: H walks the cells, "
        "CMP finds a match at 0x0802, output 2; what happens without a match is a question for M4. 5: switch without "
        "break: INC falls through into DEC and A stays 5.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
s = s.replace('<title id="title">Керування: перевірки і стрибки</title>', '<title id="title">Control: checks and jumps</title>')
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
