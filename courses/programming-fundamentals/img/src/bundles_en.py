"""Translate img/bundles.uk.svg into English: python3 bundles_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()

# Text between tags: Ukrainian fragment -> English. Each must occur at least once.
T = {
    "Структури, час життя і купа": "Structs, lifetimes and the heap",
    "Поля лежать поруч — з дірками для вирівнювання. Де лежить сама змінна, вирішує її час життя.":
        "Fields sit side by side, with gaps for alignment. Where the variable itself lives depends on its lifetime.",
    "— розділ Теорії Lab 06": "— section of the Lab 06 theory",
    "нічиї байти": "unowned bytes",
    "звільнена пам'ять": "freed memory",
    " — поля поруч, у яких є імена": ": fields side by side, with names",
    "зміщення": "offset",
    "а полів — 1 + 4 = 5": "but the fields are 1 + 4 = 5",
    " стає на зміщення,": " sits at an offset",
    "кратне 4: ": "divisible by 4: ",
    "Вирівнювальні байти нічиї: у дампі там досі те, що лежало (": "Padding bytes belong to no field: the dump still shows what was there (",
    "Порядок полів змінює розмір:": "Field order changes the size:",
    "Масив із 8 таких записів: 48 проти 32 байтів.": "An array of 8 such records: 48 bytes against 32.",
    " — цілі з типом": ": integers with a type",
    "сирий байт": "raw byte",
    "розібраний опкод": "decoded opcode",
    "— не збирається": "— does not compile",
    " нічого не перевіряє:": " checks nothing:",
    "невідомий байт ловить ": "an unknown byte is caught by ",
    "це помилка, а не тихий ": "it is an error, not a silent ",
    "3. Три часи життя: де живе змінна і як довго": "3. Three lifetimes: where a variable lives and for how long",
    "Адреси — з ": "Addresses from ",
    " у практиці Lab 06. У вас будуть інші, але три ділянки так само далеко одна від одної.":
        " in the Lab 06 practice. Yours will differ, but the three areas will be just as far apart.",
    "Статична / глобальна": "Static / global",
    "Автоматична (стек)": "Automatic (stack)",
    "Динамічна (купа)": "Dynamic (heap)",
    "ember: Memory, якщо глобальний (не робіть)": "ember: Memory, if made global (don't)",
    "ember: CPU cpu у main": "ember: CPU cpu in main",
    "ember: купа гостя 0xC00–0xEFF": "ember: the guest heap 0xC00–0xEFF",
    "увесь час роботи": "the whole run",
    "до виходу з блока": "until the block ends",
    "до delete — блок уже скінчився": "until delete; the block has ended",
    "старт": "start",
    "кінець": "end",
    "4. Завислий вказівник і витік — протилежні": "4. A dangling pointer and a leak are opposites",
    "Вказівник без об'єкта": "A pointer without an object",
    "звільнено": "freed",
    "delete p; знову → double-free": "delete p; again → double-free",
    "Об'єкт без вказівника": "An object without a pointer",
    "витік: на 1 уже ніхто не вказує": "leak: nothing points at 1 any more",
    "LeakSanitizer — на Linux; macOS мовчить": "LeakSanitizer on Linux; macOS stays quiet",
    "5. Купа ": "5. The ",
    " іде лише вперед": " only moves forward",
    "перший блок, 4 байти": "first block, 4 bytes",
    "другий, 2": "second, 2",
    "вільно до 0xEFF": "free up to 0xEFF",
    " немає: вершина купи тільки росте.": " is missing on purpose: the heap top only grows.",
    "Не влізло — ": "Doesn't fit: ",
    ", а ": ", and ",
    " не змінюється.": " stays the same.",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)
# «5. Купа ember: ALLOC …» reads "5. The ember heap: ALLOC only moves forward" in English.
s = s.replace('>5. The <tspan class="mono">ember</tspan>: <tspan class="mono">ALLOC</tspan>',
              '>5. The <tspan class="mono">ember</tspan> heap: <tspan class="mono">ALLOC</tspan>')

for ua, en in [("Заголовок і легенда", "Title and legend"), ("3. Три часи життя", "3. Three lifetimes"),
               ("4. Завислий вказівник і витік", "4. Dangling pointer and leak"), ("5. Купа ember", "5. The ember heap")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Five panels for the Lab 06 theory. 1: struct P { char c; int n; } takes 8 bytes though its fields take 5: "
        "three padding bytes sit between c and n; the same fields op, addr, imm in three orders take 6, 4 and 4 bytes. "
        "2: enum class Op: the byte 0x18 becomes Op::Inc only through a cast. 3: three lifetimes, static, stack and heap, "
        "with addresses from the practice run and a timeline. 4: a dangling pointer is a pointer without an object, a "
        "leak is an object without a pointer. 5: the ember heap: ALLOC hands out 0x0C00 for 4 bytes and 0x0C04 for 2, "
        "the heap top is 0x0C06, and there is no FREE.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
s = s.replace('<title id="title">Структури, час життя і купа</title>', '<title id="title">Structs, lifetimes and the heap</title>')
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
