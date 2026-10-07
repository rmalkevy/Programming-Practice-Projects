"""Translate img/bits.uk.svg into English: python3 bits_en.py IN.uk.svg OUT.svg"""
import sys, re
s = open(sys.argv[1]).read()
M = '<tspan class="mono">'
R = [
 ('<title id="title">Біти, оператори й маски</title>', '<title id="title">Bits, operators and masks</title>'),
 ('>Біти: '+M, '>Bits: '+M), ('</tspan> і маски</text>', '</tspan> and masks</text>'),
 ('Байт — це вісім бітів. Бітовий оператор працює з кожним бітом окремо.', 'A byte is eight bits. A bitwise operator works on each bit separately.'),
 ('— розділ Теорії Lab 02', '— section of the Lab 02 theory'),
 ('>біт = 1<', '>bit = 1<'), ('>біт = 0<', '>bit = 0<'), ('нуль, що зайшов', 'a zero shifted in'),
 ('<!-- Заголовок і легенда -->', '<!-- Title and legend -->'),
 ('<!-- 1. Один байт, три записи -->', '<!-- 1. One byte, three notations -->'),
 ('1. Один байт — три записи', '1. One byte, three notations'),
 ('>номер біта<', '>bit number<'), ('>вага<', '>weight<'), ('>старший ліворуч<', '>high bit on the left<'),
 ('4 біти = 1 цифра', '4 bits = 1 digit'),
 ('двійковий: самі біти', 'binary: the bits themselves'),
 ('шістнадцятковий: ', 'hexadecimal: '),
 ('десятковий: ', 'decimal: '), ('</tspan> — ваги одиниць', '</tspan>, the weights of the ones'),
 ('<!-- 2. Доповняльний код -->', "<!-- 2. Two's complement -->"),
 ('2. Доповняльний код: як записати −5', "2. Two's complement: how to write −5"),
 (">п'ять<", '>five<'), ('перевернути кожен біт', 'flip every bit'),
 ('= −5, байт 0xFB', '= −5, byte 0xFB'),
 ('Той самий байт '+M+'0xFB</tspan> — дві розповіді. Різниця лише у вазі біта 7:', 'The same byte '+M+'0xFB</tspan>, two readings. Only the weight of bit 7 differs:'),
 ('Так само '+M+'0xFF</tspan>: як '+M+'uint8_t</tspan> — 255, як '+M+'int8_t</tspan> — −1.', 'Likewise '+M+'0xFF</tspan>: 255 as '+M+'uint8_t</tspan>, −1 as '+M+'int8_t</tspan>.'),
 ('<!-- 3. Шість операторів -->', '<!-- 3. Six operators -->'),
 ('3. Шість операторів: кожен біт окремо', '3. Six operators, each bit on its own'),
 ('1, лише коли обидва 1 → <tspan class="b">маска</tspan>', '1 only if both are 1 → <tspan class="b">mask</tspan>'),
 ('1, якщо хоч один 1 → <tspan class="b">виставити</tspan>', '1 if either is 1 → <tspan class="b">set</tspan>'),
 ('1, якщо різні → <tspan class="b">перемкнути</tspan>', '1 if they differ → <tspan class="b">toggle</tspan>'),
 ('Стовпчик рахується без сусідів. Біт 6: ', 'Each column ignores its neighbours. Bit 6: '),
 ('</tspan> дає 0, '+M+'|</tspan> і '+M+'^</tspan> дають 1.', '</tspan> gives 0, '+M+'|</tspan> and '+M+'^</tspan> give 1.'),
 ('SHL A: біт 7 виїжджає в C', 'SHL A: bit 7 drops into C'),
 ('SHR A: біт 0 виїжджає в C', 'SHR A: bit 0 drops into C'),
 ('>заходить 0<', '>0 shifts in<'),
 ('Для беззнакових: ', 'For unsigned: '),
 ('<tspan class="b">Пріоритет:</tspan>', '<tspan class="b">Precedence:</tspan>'),
 ('</tspan> читається як '+M, '</tspan> parses as '+M),
 ('</tspan> = 0 — завжди хибне. Пишіть ', '</tspan> = 0, always false. Write '),
 ('<tspan class="b">Ширина:</tspan>', '<tspan class="b">Width:</tspan>'),
 ('</tspan> для '+M+'int</tspan> заїжджає в знаковий біт, ', '</tspan> on an '+M+'int</tspan> lands in the sign bit, '),
 ('</tspan> — UB. Для бітів беріть беззнакове: ', '</tspan> is UB. For bits, use unsigned: '),
 ('<!-- 4. Зсув і маска -->', '<!-- 4. Shift and mask -->'),
 ('4. Зсув і маска: розібрати байт на поля', '4. Shift and mask: split a byte into fields'),
 ('1. зсунути поле до біта 0', '1. shift the field down to bit 0'),
 ('2. маска: лишити тільки поле', '2. mask: keep only the field'),
 ('y="814">поле<', 'y="814">field<'),
 ('>без зсуву<', '>no shift<'),
 ('Біт прапорця: виставити, скинути, перевірити', 'A flag bit: set, clear, test'),
 ('>виставити біт 3<', '>set bit 3<'), ('>скинути біт 0<', '>clear bit 0<'), ('≠ 0 → біт 2 є', '≠ 0 → bit 2 is set'),
 ('У '+M+'ember</tspan>: старший півбайт опкода — група', 'In '+M+'ember</tspan>: the high nibble of an opcode is its group'),
 ('</tspan> = 1 → група '+M+'0x1_</tspan>, ALU', '</tspan> = 1 → group '+M+'0x1_</tspan>, the ALU'),
 ('Яка саме інструкція — каже весь байт, за таблицею з ISA.', 'The whole byte says which instruction it is; see the ISA table.'),
]
for a, b in R:
    assert a in s, "MISSING: " + a
    s = s.replace(a, b)
desc = ("Four panels for the Lab 02 theory. 1: the byte 0x2F as eight bits with weights 128…1, two hex digits of four bits each, decimal 47. "
        "2: −5 in two's complement: 5, flip the bits, add 1, giving 0xFB; the same byte is 251 as uint8_t and −5 as int8_t because bit 7 weighs −128. "
        "3: a = 0xCA and b = 0xA6 bit by bit through &amp;, |, ^, ~; the shifts a &lt;&lt; 1 and a &gt;&gt; 1, where the bit that drops out goes into flag C; "
        "the precedence trap x &amp; 1 == 0. 4: the byte 0b1011'10'01 split into opcode, dest and src fields by a shift and a mask; "
        "set, clear and test a flag bit; the high nibble of an ember opcode is its group.")
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], 'w').write(s)
