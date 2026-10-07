#!/usr/bin/env python3
"""Generate img/pointers.uk.svg for Lab 03 (pointers)."""
import sys

W, H = 1080, 1190
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def cells(x0, y, w, h, vals, cls, addrs=None, addr_y=None, two_line=False):
    for i, v in enumerate(vals):
        x = x0 + i * w
        c = cls[i] if isinstance(cls, list) else cls
        o(f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        ty = y + (18 if two_line else h / 2 + 5)
        tcls = "mono" + (" muted" if c.startswith("pad") else "")
        o(f'<text class="{tcls}" x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{v}</text>')
        if addrs:
            ay = y + 36 if two_line else addr_y
            o(f'<text class="xs mono muted" x="{x + w / 2:g}" y="{ay}" text-anchor="middle">{addrs[i]}</text>')

def bracket(x1, x2, y, down=True):
    d = 6 if down else -6
    o(f'<path class="brace" d="M{x1},{y} v{d} H{x2} v{-d}"/>')

STYLE = """  <style>
    svg { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --box:#f6f8fa; --chip:#e7ecf0;
          --code:#ddf4ff; --code-s:#0969da; --data:#dafbe1; --data-s:#1a7f37; --ptr:#fbefff; --ptr-s:#8250df;
          --pad:#f6f8fa; --pad-s:#818b98; --bad:#ffebe9; --bad-s:#cf222e; }
    @media (prefers-color-scheme: dark) {
      svg { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --box:#151b23; --chip:#262c36;
            --code:#0d2c4f; --code-s:#4493f8; --data:#0f2d1a; --data-s:#3fb950; --ptr:#271b45; --ptr-s:#ab7df8;
            --pad:#151b23; --pad-s:#9198a1; --bad:#3d1418; --bad-s:#f85149; }
    }
    text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: var(--fg); font-size: 13px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
    .h1 { font-size: 22px; font-weight: 700; }
    .h2 { font-size: 15px; font-weight: 700; }
    .b { font-weight: 700; }
    .sm { font-size: 11.5px; }
    .xs { font-size: 10.5px; }
    .muted { fill: var(--muted); }
    .ok { fill: var(--data-s); font-weight: 700; }
    .err { fill: var(--bad-s); }
    .reg { font-size: 15px; font-weight: 700; }
    .chip rect { fill: var(--chip); }
    .chip text { font-size: 10.5px; font-weight: 700; fill: var(--muted); text-anchor: middle; }
    .bg { fill: var(--bg); }
    .box { fill: var(--box); stroke: var(--line); stroke-width: 1.5; }
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .data { fill: var(--data); stroke: var(--data-s); stroke-width: 1.2; }
    .data-int { fill: none; stroke: var(--data-s); stroke-width: 2.5; }
    .data-in { fill: var(--data); stroke: var(--data-s); stroke-width: 0.6; stroke-dasharray: 2 2; }
    .ptr { fill: var(--ptr); stroke: var(--ptr-s); stroke-width: 1.2; }
    .ptr-box { fill: var(--ptr); stroke: var(--ptr-s); stroke-width: 2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .code { fill: var(--code); stroke: var(--code-s); stroke-width: 1.2; }
    .r-pc { stroke: var(--code-s); stroke-width: 2; fill: var(--bg); }
    .r-h { stroke: var(--data-s); stroke-width: 2; fill: var(--bg); }
    .null { fill: var(--bad); stroke: var(--bad-s); stroke-width: 2; }
    .brace { fill: none; stroke: var(--muted); stroke-width: 1.2; }
    .arrow { fill: none; stroke-width: 2; }
    .a-ptr { stroke: var(--ptr-s); }  .m-ptr { fill: var(--ptr-s); }
    .a-h { stroke: var(--data-s); }   .m-h { fill: var(--data-s); }
    .a-pc { stroke: var(--code-s); }  .m-pc { fill: var(--code-s); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .x-bad { stroke: var(--bad-s); stroke-width: 2.5; stroke-linecap: round; }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Вказівники: &amp;, * і p + 1</title>')
o('  <desc id="desc">Чотири панелі до теорії Lab 03. 1: int x = 65 займає чотири комірки, вказівник p займає вісім і тримає адресу x; таблиця значень x, &amp;x, p, *p, &amp;p, sizeof до і після *p = 66. 2: той самий масив int a[3] через Byte* крокує по байту, через int* — по чотири байти. 3: nullptr нікуди не вказує, його розіменування — UB; void* тримає адресу без розміру. 4: у ember той самий байт має адресу хоста mem.data + 0x800 і адресу гостя 0x0800 у регістрі H; LOAD A, [H] — це *p, INCH — це ++p.</desc>')
o(STYLE)
o('  <defs>')
for m in ("m-ptr", "m-h", "m-pc", "m-bad"):
    marker(m)
marker("m-io", 6)
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Вказівники: <tspan class="mono">&amp;</tspan>, <tspan class="mono">*</tspan> і <tspan class="mono">p + 1</tspan></text>')
o('<text class="muted" x="24" y="60">Вказівник — це змінна, значення якої є адресою. Усе інше — наслідки.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 03</text>')
o('<rect class="data" x="924" y="26" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="37">значення</text>')
o('<rect class="ptr" x="702" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="736" y="59">вказівник: у ньому адреса</text>')
o('<rect class="pad" x="924" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="59">нічиї байти</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Коробка і стрілка -->')
o('<rect class="box" x="24" y="84" width="1032" height="320" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Коробка і стрілка</text>')
o('<text class="sm muted" x="214" y="110"><tspan class="mono">x</tspan> — ім\'я для компілятора, <tspan class="mono">&amp;x</tspan> — місце в пам\'яті, <tspan class="mono">p</tspan> — змінна, у якій записане це місце</text>')
chip(984, 96, "§1"); chip(1018, 96, "§4")

o('<rect class="cell" x="44" y="150" width="196" height="96" rx="6"/>')
o('<text class="mono" x="60" y="176">int x = 65;</text>')
o('<text class="mono" x="60" y="200">int* p = &amp;x;</text>')
o('<text class="mono" x="60" y="224">*p = 66;</text>')
o('<text class="sm muted" x="44" y="270">Адреси умовні: справжні</text>')
o('<text class="sm muted" x="44" y="286">щоразу інші.</text>')

X0, CW, Y = 280, 46, 196
xbytes = ["41", "00", "00", "00"]
pad = ["??"] * 4
pbytes = ["40", "2a", "3f", "6d", "01", "00", "00", "00"]
vals = xbytes + pad + pbytes
cls = ["data"] * 4 + ["pad"] * 4 + ["ptr"] * 8
addrs = [f"…a{0x40 + i:02x}" for i in range(16)]
o('<text class="mono b" x="372" y="186" text-anchor="middle">int x</text>')
o('<text class="sm muted" x="556" y="186" text-anchor="middle">вирівнювання</text>')
o('<text class="mono b" x="660" y="186">int* p</text>')
o('<path class="arrow a-ptr" d="M960,192 C960,138 303,138 303,192" marker-end="url(#m-ptr)"/>')
o('<text class="sm" x="631" y="140" text-anchor="middle" style="paint-order:stroke" stroke="var(--box)" stroke-width="4">у <tspan class="mono">p</tspan> записана адреса <tspan class="mono">x</tspan> — це і є стрілка</text>')
cells(X0, Y, CW, 36, vals, cls, addrs, addr_y=246)
bracket(282, 462, 252); bracket(466, 646, 252); bracket(650, 1014, 252)
o('<text class="sm mono" x="282" y="274">sizeof(x) = sizeof(*p) = 4</text>')
o('<text class="sm muted" x="282" y="290">65 = 0x41, молодший байт уперед</text>')
o('<text class="sm muted" x="556" y="274" text-anchor="middle">не належать ні x, ні p</text>')
o('<text class="sm" x="832" y="274" text-anchor="middle"><tspan class="mono">sizeof(p) = 8</tspan>: адреса займає 8 байтів</text>')
o('<text class="sm muted" x="832" y="290" text-anchor="middle"><tspan class="mono">0x16d3f2a40</tspan>, молодший байт уперед</text>')

# таблиця виразів
o('<rect class="cell" x="44" y="306" width="992" height="88" rx="6"/>')
o('<line class="rule" x1="44" y1="330" x2="1036" y2="330"/>')
o('<line class="rule" x1="44" y1="372" x2="1036" y2="372"/>')
exprs = ["x", "&amp;x", "p", "*p", "&amp;p", "sizeof(p)", "sizeof(*p)"]
v1 = ["65", "0x16d3f2a40", "0x16d3f2a40", "65", "0x16d3f2a48", "8", "4"]
v2 = ["що в коробці", "де коробка", "те саме число", "піти за адресою", "коробка самого p", "ширина адреси", "розмір int"]
v3 = ["66", "без змін", "без змін", "66", "без змін", "8", "4"]
cx0, cwid = 180, 856 / 7
o('<text class="sm b" x="58" y="323">вираз</text>')
o('<text class="sm b" x="58" y="347">значення</text>')
o('<text class="sm muted" x="58" y="365">що це</text>')
o('<text class="sm b" x="58" y="388">після <tspan class="mono">*p = 66;</tspan></text>')
for i in range(7):
    cx = cx0 + cwid * i + cwid / 2
    o(f'<text class="mono b" x="{cx:.0f}" y="323" text-anchor="middle">{exprs[i]}</text>')
    o(f'<text class="sm mono" x="{cx:.0f}" y="347" text-anchor="middle">{v1[i]}</text>')
    o(f'<text class="sm muted" x="{cx:.0f}" y="365" text-anchor="middle">{v2[i]}</text>')
    c3 = "sm mono ok" if v3[i] == "66" else ("sm muted" if v3[i] == "без змін" else "sm mono")
    o(f'<text class="{c3}" x="{cx:.0f}" y="388" text-anchor="middle">{v3[i]}</text>')
o()

# ---------- Панель 2 ----------
o('<!-- 2. Арифметика вказівників -->')
o('<rect class="box" x="24" y="420" width="640" height="340" rx="10"/>')
o('<text class="h2" x="44" y="446">2. <tspan class="mono">p + 1</tspan> — наступний елемент, а не байт</text>')
chip(624, 432, "§2")
o('<text class="sm mono" x="44" y="472">int a[3] = {10, 20, 30};   Byte* b = (Byte*)a;   int* q = a;</text>')

X0, CW = 44, 42
abytes = ["0a", "00", "00", "00", "14", "00", "00", "00", "1e", "00", "00", "00"]
for i, lab in enumerate(["b", "b+1", "b+2", "b+3"]):
    cx = X0 + CW * i + CW // 2
    o(f'<text class="sm mono b" x="{cx}" y="500" text-anchor="middle">{lab}</text>')
    o(f'<path class="arrow a-ptr" d="M{cx},505 L{cx},522" marker-end="url(#m-ptr)"/>')
cells(X0, 524, CW, 36, abytes, "data")
o('<text class="sm b" x="562" y="546">крок 1 байт</text>')
for i in range(12):
    o(f'<text class="xs mono muted" x="{X0 + CW * i + CW // 2}" y="577" text-anchor="middle">+{i}</text>')
# той самий масив як три int
for i in range(12):
    x = X0 + CW * i
    o(f'<rect class="data-in" x="{x}" y="588" width="{CW}" height="36"/>')
    o(f'<text class="mono" x="{x + CW // 2}" y="611" text-anchor="middle">{abytes[i]}</text>')
for k in range(3):
    o(f'<rect class="data-int" x="{X0 + 4 * CW * k}" y="588" width="{4 * CW}" height="36"/>')
o('<text class="sm b" x="562" y="610">крок 4 байти</text>')
for k, (lab, val) in enumerate([("q", "*q = 10"), ("q+1", "*(q+1) = 20"), ("q+2", "*(q+2) = 30")]):
    cx = X0 + 4 * CW * k + CW // 2
    o(f'<path class="arrow a-ptr" d="M{cx},650 L{cx},627" marker-end="url(#m-ptr)"/>')
    o(f'<text class="sm mono b" x="{cx}" y="666" text-anchor="middle">{lab}</text>')
    o(f'<text class="sm mono" x="{cx}" y="686" text-anchor="middle">{val}</text>')
o('<text class="b" x="44" y="720">адреса(<tspan class="mono">p + n</tspan>) = адреса(<tspan class="mono">p</tspan>) + <tspan class="mono">n · sizeof(*p)</tspan></text>')
o('<text class="sm muted" x="44" y="742"><tspan class="mono">(q + 2) − q = 2</tspan>, а не 8: різниця вказівників теж рахує елементи</text>')
o()

# ---------- Панель 3 ----------
o('<!-- 3. nullptr і void* -->')
o('<rect class="box" x="680" y="420" width="376" height="340" rx="10"/>')
o('<text class="h2" x="700" y="446">3. <tspan class="mono">nullptr</tspan> і <tspan class="mono">void*</tspan></text>')
chip(982, 432, "§1"); chip(1016, 432, "§3")
o('<text class="sm mono" x="700" y="472">int* p = nullptr;</text>')
o('<rect class="ptr-box" x="700" y="484" width="150" height="34" rx="6"/>')
o('<text class="reg mono" x="712" y="506">p</text><text class="mono" x="760" y="506">0x0</text>')
o('<path class="arrow a-bad dashed" d="M852,501 L926,501" marker-end="url(#m-bad)"/>')
o('<circle class="null" cx="944" cy="501" r="13"/>')
o('<path class="x-bad" d="M938,495 L950,507 M950,495 L938,507"/>')
o('<text class="sm" x="966" y="505">нікуди</text>')
o('<text class="sm" x="700" y="542"><tspan class="mono">*p</tspan> — невизначена поведінка (UB). ASan:</text>')
o('<text class="sm mono err" x="700" y="560">SEGV on unknown address 0x000000000000</text>')
o('<text class="sm" x="700" y="580">В <tspan class="mono">ember</tspan> так само: адреса <tspan class="mono">≥ MEM_SIZE</tspan> — відхилити.</text>')
o('<line class="rule" x1="700" y1="598" x2="1036" y2="598"/>')
o('<text class="sm mono" x="700" y="622">void* v = &amp;x;</text>')
o('<rect class="ptr-box" x="700" y="634" width="150" height="34" rx="6"/>')
o('<text class="reg mono" x="712" y="656">v</text><text class="sm mono" x="742" y="656">0x16d3f2a40</text>')
o('<path class="arrow a-ptr dashed" d="M852,651 L912,651" marker-end="url(#m-ptr)"/>')
o('<rect class="pad" x="916" y="634" width="120" height="34" rx="2"/>')
o('<text class="sm muted" x="976" y="655" text-anchor="middle">скільки байтів?</text>')
o('<text class="sm" x="700" y="694">Адреса є, типу немає — отже, немає й розміру:</text>')
o('<text class="sm" x="700" y="712"><tspan class="mono">*v</tspan> і <tspan class="mono">v + 1</tspan> не компілюються.</text>')
o('<text class="sm" x="700" y="736"><tspan class="mono">(int*)v</tspan> повертає тип — і <tspan class="mono">*</tspan> знову працює.</text>')
o()

# ---------- Панель 4 ----------
o('<!-- 4. Хост і гість: H -->')
o('<rect class="box" x="24" y="776" width="1032" height="398" rx="10"/>')
o('<text class="h2" x="44" y="802">4. Те саме в <tspan class="mono">ember</tspan>: <tspan class="mono">H</tspan> — вказівник у залізі</text>')
chip(948, 788, "§2"); chip(982, 788, "§5"); chip(1016, 788, "§6")
o('<text class="sm muted" x="44" y="824">Хост — ваш процес C++: адреса довга, 8 байтів. Гість — програма в <tspan class="mono">ember</tspan>: адреса — номер комірки <tspan class="mono">0x000</tspan>–<tspan class="mono">0xFFF</tspan>, 16 біт.</text>')

o('<text class="b" x="44" y="862">хост</text><text class="sm muted" x="44" y="878">C++</text>')
o('<rect class="ptr-box" x="150" y="846" width="200" height="34" rx="6"/>')
o('<text class="mono b" x="162" y="868">mem.data</text><text class="sm mono" x="250" y="868">0x16d3f0000</text>')
o('<rect class="ptr-box" x="410" y="846" width="200" height="34" rx="6"/>')
o('<text class="mono b" x="422" y="868">Byte* p</text><text class="sm mono" x="508" y="868">0x16d3f0800</text>')
o('<text class="sm muted" x="640" y="860">адреса хоста — справжнє місце в RAM</text>')
o('<text class="sm muted" x="640" y="876">вашого процесу, щоразу інша</text>')

# пам'ять ember
o('<rect class="code" x="150" y="910" width="260" height="44"/>')
o('<text class="b" x="162" y="930">код</text><text class="sm muted" x="196" y="930">і вільне місце</text>')
o('<text class="xs mono muted" x="162" y="946">0x000</text><text class="xs mono muted" x="400" y="946" text-anchor="end">0x7FF</text>')
cells(410, 910, 60, 44, ["0a", "14", "1e", "00", "00", "00"], "data",
      [f"0x{0x800 + i:03X}" for i in range(6)], two_line=True)
o('<rect class="pad" x="770" y="910" width="266" height="44"/>')
o('<text class="sm muted" x="903" y="936" text-anchor="middle">… дані, екран, купа, стек — до <tspan class="mono">0xFFF</tspan></text>')

# стрілки хоста
o('<path class="arrow a-ptr" d="M170,882 L170,906" marker-end="url(#m-ptr)"/>')
o('<path class="arrow a-ptr" d="M440,882 L440,906" marker-end="url(#m-ptr)"/>')
o('<path class="arrow a-ptr dashed" d="M500,882 L500,906" marker-end="url(#m-ptr)"/>')
o('<text class="sm mono muted" x="508" y="898">++p</text>')

o('<text class="b" x="44" y="998">гість</text><text class="sm mono muted" x="44" y="1014">ember</text>')
o('<rect class="r-pc" x="150" y="984" width="140" height="34" rx="6"/>')
o('<text class="reg mono" x="162" y="1006">PC</text><text class="mono" x="200" y="1006">0x0000</text>')
o('<rect class="r-h" x="410" y="984" width="140" height="34" rx="6"/>')
o('<text class="reg mono" x="422" y="1006">H</text><text class="mono" x="460" y="1006">0x0800</text>')
o('<path class="arrow a-pc" d="M170,982 L170,958" marker-end="url(#m-pc)"/>')
o('<path class="arrow a-h" d="M440,982 L440,958" marker-end="url(#m-h)"/>')
o('<path class="arrow a-h dashed" d="M500,982 L500,958" marker-end="url(#m-h)"/>')
o('<text class="sm mono muted" x="508" y="974">INCH</text>')
o('<text class="sm muted" x="640" y="998">адреса гостя — номер комірки:</text>')
o('<text class="sm muted" x="640" y="1014"><tspan class="mono">0x0800</tspan> = 2048 при кожному запуску</text>')

o('<text x="44" y="1048"><tspan class="mono b">p == mem.data + H</tspan><tspan class="sm">  — той самий байт, два різні числа: хост бачить <tspan class="mono">0x16d3f0800</tspan>, гість — <tspan class="mono">0x0800</tspan>.</tspan></text>')

cards = [
    ("LOADH H, 0x0800", "p = &amp;mem.data[0x800];", "покласти адресу у вказівник"),
    ("LOAD A, [H]", "a = *p;", "піти за адресою і взяти байт"),
    ("INCH", "++p;", "зсунути на один елемент — байт"),
]
for k, (asm, cpp, note) in enumerate(cards):
    x = 44 + k * 336
    o(f'<rect class="cell" x="{x}" y="1064" width="320" height="72" rx="6"/>')
    o(f'<text class="mono b" x="{x + 14}" y="1086">{asm}</text><text class="xs muted" x="{x + 306}" y="1086" text-anchor="end">ember</text>')
    o(f'<text class="mono" x="{x + 14}" y="1106">{cpp}</text><text class="xs muted" x="{x + 306}" y="1106" text-anchor="end">C++</text>')
    o(f'<text class="sm muted" x="{x + 14}" y="1126">{note}</text>')

o('<path class="x-bad" d="M46,1150 L56,1160 M56,1150 L46,1160"/>')
o('<text class="sm" x="66" y="1159">Не кладіть <tspan class="mono">p</tspan> у пам\'ять гостя: <tspan class="mono">0x16d3f0800</tspan> не влазить у 16 біт і всередині <tspan class="mono">ember</tspan> нічого не означає. Гостю — індекси, хосту — вказівники.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
