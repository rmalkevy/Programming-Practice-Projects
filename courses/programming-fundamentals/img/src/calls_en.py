"""Translate img/calls.uk.svg into English: python3 calls_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()

# Text between tags: Ukrainian fragment -> English. Each must occur at least once.
T = {
    "Виклик, повернення і стек": "Call, return and the stack",
    "Виклик і повернення: стек": "Call and return: the stack",
    " — це стрибок, який пам'ятає, куди повернутись. Пам'ятає він на стеку.":
        " is a jump that remembers where to come back to. It remembers on the stack.",
    "— розділ Теорії Lab 07": "— section of the Lab 07 theory",
    "старий байт": "old byte",
    "кадри ": "frames ",
    "кадр ": "frame ",
    "кадр": "frame",
    " в ": " in ",
    ": стек крок за кроком": ": the stack step by step",
    "Лістинг з ISA §6, тільки ": "The listing from ISA §6, only with ",
    ". Номери кроків — з трасування ": ". Step numbers come from the trace of ",
    " у практиці Lab 07.": " in the Lab 07 practice.",
    "← сюди RET": "← RET to here",
    "зберегти n": "save n",
    "крок 2": "step 2", "крок 11": "step 11", "крок 27": "step 27", "крок 30": "step 30", "крок 34": "step 34",
    "виклик fact(3)": "call fact(3)", "виклик fact(2)": "call fact(2)",
    "fact(1): база": "fact(1): base case", "назад у main": "back in main",
    " кладе адресу ": " pushes the address ",
    "після себе": "after itself",
    ": молодший байт, потім старший (": ": low byte first, then high (",
    " знімає їх у зворотному порядку. ": " pops them in reverse order. ",
    " зберігає ": " saves ",
    ": наступний виклик зітре ": ": the next call will overwrite ",
    " і ": " and ",
    " не стирають байтів, лише піднімають ": " erase nothing, they only raise ",
    ". Сірі комірки — старі значення: їх перезапише наступний ": ". Grey cells are old values, to be overwritten by the next ",
    "Після ": "After ",
    " знову ": " is back at ",
    ": кожен ": ": every ",
    " має свій ": " has its ",
    ", кожен ": ", every ",
    " — свій ": " its ",
    ". Конвенція: аргумент і результат в ": ". Convention: argument and result in ",
    "2. Кожен виклик — свій ": "2. Every call has its own ",
    "// база": "// base case",
    "// менший випадок": "// smaller case",
    "база: 1": "base: 1",
    "повертає 6": "returns 6", "повертає 2": "returns 2", "повертає 1": "returns 1",
    "Три різні ": "Three different ",
    " у трьох різних кадрах; кожен живе, доки його виклик не поверне.":
        " in three different frames; each lives until its call returns.",
    "Глобальна ": "A global ",
    " замість параметра — одна коробка на всіх, і ": " instead of a parameter: one box for every call, and ",
    "3. Як значення потрапляють усередину": "3. How values get in",
    "копія": "copy",
    "адреса: ": "address: ",
    "своєї коробки немає:": "it has no box of its own:",
    " — ще одне ім'я для ": " is another name for ",
    " — як ": " is like ",
    ", тільки для читання: запис через нього не збереться.": ", but read-only: writing through it does not compile.",
    "4. Стек як тип: той самий LIFO, інша лічба": "4. The stack as a type: the same LIFO, counted differently",
    "порожній": "empty",
    "Stack (хост)": "Stack (host)",
    "вказує на": "points to",
    "останній зайнятий": "last used",
    "наступний вільний": "next free",
    "росте": "grows",
    "вгору: data[0], data[1]…": "up: data[0], data[1]…",
    "вниз: 0xFFF, 0xFFE…": "down: 0xFFF, 0xFFE…",
    "переповнення": "overflow",
    "push при top == CAP − 1": "push when top == CAP − 1",
    "SP нижче 0xF00": "SP below 0xF00",
    "спустошення": "underflow",
    "pop при top == −1": "pop when top == −1",
    "зняття при SP ≥ 0xFFF": "pop at SP ≥ 0xFFF",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)

for ua, en in [("Заголовок і легенда", "Title and legend"), ("1. fact(3) в ember", "1. fact(3) in ember"),
               ("2. Кожен виклик — свій n", "2. Every call has its own n"), ("3. Параметри", "3. Parameters"),
               ("4. Стек як тип", "4. The stack as a type")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Four panels for the Lab 07 theory. 1: fact(3) in ember from the ISA §6 listing: five snapshots of the stack "
        "0xFFF…0xFF7 at trace steps 2, 11, 27, 30 and 34; CALL pushes the return address, PUSH A saves n, frames of "
        "fact(3), fact(2), fact(1); POP and RET only raise SP and the old bytes stay. 2: in C++ every call of fact has "
        "its own n, and the values come back as 1, 2, 6. 3: passing by value, by pointer and by reference. "
        "4: the stack as a type: top is the last used slot, SP is the next free one.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
