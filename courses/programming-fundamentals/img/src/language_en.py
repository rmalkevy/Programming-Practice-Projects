"""Translate img/language.uk.svg into English: python3 language_en.py IN.uk.svg OUT.svg"""
import re
import sys

s = open(sys.argv[1]).read()
M = '<tspan class="mono">'

# Whole lines whose word order changes in English: exact substring -> English.
R = [
    ('Вставте ' + M + 'NOP</tspan> вище ' + M + 'base</tspan> у ' + M + 'fact</tspan> — зсунуться обидва ' + M + 'JZ base</tspan>.',
     'Insert a ' + M + 'NOP</tspan> above ' + M + 'base</tspan> in ' + M + 'fact</tspan> and both ' + M + 'JZ base</tspan> operands shift.'),
]
for a, b in R:
    assert a in s, "MISSING: " + a
    s = s.replace(a, b)

# Text between tags: Ukrainian fragment -> English.
T = {
    "Від тексту до байтів": "From text to bytes",
    "Текст програми — теж байти. Лексер робить із них токени, асемблер — байти коду.":
        "Program text is bytes too. The lexer turns it into tokens, the assembler into code bytes.",
    "— розділ Теорії Lab 08": "— section of the Lab 08 theory",
    "1. Від тексту до ": "1. From text to ",
    "текст, байти символів": "text, bytes of characters",
    "лексер": "lexer", "список токенів": "token list", "асемблер": "assembler",
    "прохід 1 · прохід 2": "pass 1 · pass 2", "байти в Memory": "bytes in Memory",
    " збирає й виконує; просто ": " assembles and runs; plain ",
    " — REPL, як і раніше.": " is the REPL, as before.",
    "2. Символи — це ще не токени": "2. Characters are not tokens yet",
    "Курсор ": "The cursor ",
    " іде байтами рядка ": " walks the bytes of ",
    " і на кожному вирішує, куди далі:": " and decides at each where to go:",
    "літера → ident()": "letter → ident()",
    "цифра → number()": "digit → number()",
    ": , [ ] → свій токен": ": , [ ] → its own token",
    "пробіл → пропустити": "space → skip",
    "; → коментар до кінця рядка": "; → comment to end of line",
    "Окремо вирішується лише байт, з якого починається лексема: ": "Only the byte that starts a lexeme is decided on its own: ",
    " цілком забере ": " is taken whole by ",
    "Лексема за лексемою — токени рядка ": "Lexeme by lexeme, the tokens of ",
    "Граматика рядка": "Grammar of a line",
    " — мітка, ": " is the label, ",
    " — мнемоніка, ": " the mnemonic, ",
    " — операнд-мітка": " a label operand",
    "Вивід лексера, як у CHECKS.md:": "Lexer output, as in CHECKS.md:",
    "3. Список: довжину не оголошують, а з'ясовують": "3. A list: the length is found, not declared",
    "рядок 1": "line 1",
    "// порожній: head = tail = t": "// empty: head = tail = t",
    "обхід:   for (Token* t = head; t; t = t-&gt;next)": "walk:    for (Token* t = head; t; t = t-&gt;next)",
    "кінець:  пройти й delete кожен вузол": "finish:  walk it and delete every node",
    "Файл буває будь-якої довжини — тому список, а не масив. Забули ":
        "A file can be any length, hence a list, not an array. Forget ",
    " — витік.": " and it leaks.",
    "4. Два проходи: мітка нижче за стрибок": "4. Two passes: a label below the jump",
    "Програма ": "The ",
    " з Notes 08 §4; досліди ": " program from Notes 08 §4; experiments ",
    " і ": " and ",
    " у практиці Lab 08.": " in the Lab 08 practice.",
    "адр.": "addr", "текст": "text", "один прохід": "one pass", "два проходи": "two passes",
    "Прохід 1:": "Pass 1:", " адреса = сума розмірів: ": " address = sum of sizes: ",
    "Прохід 2:": "Pass 2:", " видати байти, підставивши ": " emit the bytes, filling in ",
    "Мітка вище стрибка відома одразу; нижче — лише після проходу 1.":
        "A label above the jump is known at once; one below only after pass 1.",
}
for ua, en in T.items():
    a, b = ">" + ua + "<", ">" + en + "<"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, b)

for ua, en in [("Заголовок і легенда", "Title and legend"), ("1. Конвеєр", "1. Pipeline"),
               ("2. Символи і токени", "2. Characters and tokens"), ("3. Список токенів", "3. Token list"),
               ("4. Два проходи", "4. Two passes")]:
    a = "<!-- " + ua + " -->"
    assert a in s, "MISSING: " + ua
    s = s.replace(a, "<!-- " + en + " -->")

desc = ("Four panels for the Lab 08 theory. 1: the pipeline: a .asm file, the lexer, a token list, the two-pass "
        "assembler, bytes in Memory, CPU.run. 2: the line LOADI A, 0x41 ; x is bytes, and the lexer's cursor classifies "
        "each one as letter, digit, punctuation, space or comment; the line loop: JMP loop becomes the tokens Ident(loop) "
        "Colon Ident(JMP) Ident(loop) Newline Eof. 3: the tokens in a linked list with head, tail and next. 4: the forward "
        "program: in one pass the operand of JMP done stays ?? ?? because the label is below; pass 1 finds done = 0x0004 "
        "and pass 2 emits 30 04 00.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
s = s.replace('<title id="title">Від тексту до байтів</title>', '<title id="title">From text to bytes</title>')
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], "w").write(s)
