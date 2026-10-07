"""Translate img/pointers.uk.svg into English: python3 pointers_en.py IN.uk.svg OUT.svg"""
import sys
s = open(sys.argv[1]).read()
M = '<tspan class="mono">'
R = [
 ('<title id="title">Вказівники: &amp;, * і p + 1</title>', '<title id="title">Pointers: &amp;, * and p + 1</title>'),
 ('Вказівники: '+M+'&amp;</tspan>, '+M+'*</tspan> і '+M+'p + 1</tspan>', 'Pointers: '+M+'&amp;</tspan>, '+M+'*</tspan> and '+M+'p + 1</tspan>'),
 ('Вказівник — це змінна, значення якої є адресою. Усе інше — наслідки.', 'A pointer is a variable whose value is an address. Everything else follows from that.'),
 ('— розділ Теорії Lab 03', '— section of the Lab 03 theory'),
 ('y="37">значення<', 'y="37">value<'),
 ('вказівник: у ньому адреса', 'pointer: holds an address'),
 ('нічиї байти', 'unowned bytes'),
 ('<!-- Заголовок і легенда -->', '<!-- Title and legend -->'),
 ('<!-- 1. Коробка і стрілка -->', '<!-- 1. Box and arrow -->'),
 ('1. Коробка і стрілка', '1. Box and arrow'),
 ("x</tspan> — ім'я для компілятора, "+M+"&amp;x</tspan> — місце в пам'яті, "+M+"p</tspan> — змінна, у якій записане це місце",
  "x</tspan> is a name for the compiler, "+M+"&amp;x</tspan> is a place in memory, "+M+"p</tspan> is a variable that holds that place"),
 ('Адреси умовні: справжні', 'Addresses are made up: real'),
 ('щоразу інші.', 'ones change every run.'),
 ('>вирівнювання<', '>padding<'),
 ('у '+M+'p</tspan> записана адреса '+M+'x</tspan> — це і є стрілка', M+'p</tspan> holds the address of '+M+'x</tspan>: that is the arrow'),
 ('молодший байт уперед', 'low byte first'),
 ('не належать ні x, ні p', 'belong to neither x nor p'),
 (': адреса займає 8 байтів', ': an address takes 8 bytes'),
 ('>вираз<', '>expression<'),
 ('y="347">значення<', 'y="347">value<'),
 ('>що це<', '>meaning<'),
 ('>після '+M, '>after '+M),
 ('>що в коробці<', ">what's in the box<"),
 ('>де коробка<', '>where the box is<'),
 ('>те саме число<', '>the same number<'),
 ('піти за адресою і взяти байт', 'follow the address, take the byte'),
 ('>піти за адресою<', '>follow the address<'),
 ('>коробка самого p<', ">p's own box<"),
 ('>ширина адреси<', '>address width<'),
 ('>розмір int<', '>size of int<'),
 ('>без змін<', '>unchanged<'),
 ('<!-- 2. Арифметика вказівників -->', '<!-- 2. Pointer arithmetic -->'),
 ('</tspan> — наступний елемент, а не байт', '</tspan> is the next element, not the next byte'),
 ('>крок 1 байт<', '>step: 1 byte<'),
 ('>крок 4 байти<', '>step: 4 bytes<'),
 ('адреса(', 'address('),
 ('</tspan>, а не 8: різниця вказівників теж рахує елементи', '</tspan>, not 8: a pointer difference counts elements too'),
 ('<!-- 3. nullptr і void* -->', '<!-- 3. nullptr and void* -->'),
 ('nullptr</tspan> і '+M+'void*', 'nullptr</tspan> and '+M+'void*'),
 ('>нікуди<', '>nowhere<'),
 ('</tspan> — невизначена поведінка (UB). ASan:', '</tspan> is undefined behavior (UB). ASan:'),
 ('В '+M+'ember</tspan> так само: адреса '+M+'≥ MEM_SIZE</tspan> — відхилити.', 'Same in '+M+'ember</tspan>: reject an address '+M+'≥ MEM_SIZE</tspan>.'),
 ('скільки байтів?', 'how many bytes?'),
 ('Адреса є, типу немає — отже, немає й розміру:', 'An address, but no type, so no size:'),
 ('</tspan> і '+M+'v + 1</tspan> не компілюються.', '</tspan> and '+M+'v + 1</tspan> do not compile.'),
 ('</tspan> повертає тип — і '+M+'*</tspan> знову працює.', '</tspan> brings the type back, and '+M+'*</tspan> works again.'),
 ('<!-- 4. Хост і гість: H -->', '<!-- 4. Host and guest: H -->'),
 ('4. Те саме в '+M+'ember</tspan>: '+M+'H</tspan> — вказівник у залізі', '4. The same in '+M+'ember</tspan>: '+M+'H</tspan> is a pointer in hardware'),
 ('Хост — ваш процес C++: адреса довга, 8 байтів. Гість — програма в '+M+'ember</tspan>: адреса — номер комірки '+M+'0x000</tspan>–'+M+'0xFFF</tspan>, 16 біт.',
  'Host: your C++ process, where an address is long, 8 bytes. Guest: the program inside '+M+'ember</tspan>, where an address is a cell number '+M+'0x000</tspan>–'+M+'0xFFF</tspan>, 16 bits.'),
 ('>хост<', '>host<'),
 ('>гість<', '>guest<'),
 ('адреса хоста — справжнє місце в RAM', 'a host address is a real place in the RAM'),
 ('вашого процесу, щоразу інша', 'of your process, different every run'),
 ('>код<', '>code<'),
 ('x="196" y="930">і вільне місце<', 'x="204" y="930">and free space<'),
 ('… дані, екран, купа, стек — до ', '… data, screen, heap, stack, up to '),
 ('адреса гостя — номер комірки:', 'a guest address is a cell number:'),
 ('</tspan> = 2048 при кожному запуску', '</tspan> = 2048 on every run'),
 ('— той самий байт, два різні числа: хост бачить '+M+'0x16d3f0800</tspan>, гість — '+M+'0x0800</tspan>.',
  '— the same byte, two different numbers: the host sees '+M+'0x16d3f0800</tspan>, the guest sees '+M+'0x0800</tspan>.'),
 ('покласти адресу у вказівник', 'put an address in the pointer'),
 ('зсунути на один елемент — байт', 'move one element, which is one byte'),
 ("Не кладіть "+M+"p</tspan> у пам'ять гостя: "+M+"0x16d3f0800</tspan> не влазить у 16 біт і всередині "+M+"ember</tspan> нічого не означає. Гостю — індекси, хосту — вказівники.",
  "Don't store "+M+"p</tspan> in guest memory: "+M+"0x16d3f0800</tspan> does not fit in 16 bits and means nothing inside "+M+"ember</tspan>. Indices for the guest, pointers for the host."),
]
for a, b in R:
    assert a in s, "MISSING: " + a
    s = s.replace(a, b)
import re
desc = ('Four panels for the Lab 03 theory. 1: int x = 65 takes four cells, the pointer p takes eight and holds the address of x; '
        'a table of x, &amp;x, p, *p, &amp;p and sizeof before and after *p = 66. 2: the same array int a[3] walked with Byte* steps one byte, '
        'with int* four bytes. 3: nullptr points nowhere and dereferencing it is UB; void* holds an address with no size. '
        '4: in ember the same byte has the host address mem.data + 0x800 and the guest address 0x0800 in register H; '
        'LOAD A, [H] is *p and INCH is ++p.')
s = re.sub(r'<desc id="desc">.*?</desc>', '<desc id="desc">' + desc + '</desc>', s)
left = re.findall(r'[А-Яа-яЇїІіЄєҐґ]+', s)
assert not left, left
open(sys.argv[2], 'w').write(s)
