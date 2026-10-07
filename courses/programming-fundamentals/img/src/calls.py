#!/usr/bin/env python3
"""Generate img/calls.uk.svg for Lab 07 (call stack, parameters, stack ADT)."""
import sys

W, H = 1080, 1120
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

STYLE = """  <style>
    svg { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --box:#f6f8fa; --chip:#e7ecf0;
          --f3:#ddf4ff; --f3-s:#0969da; --f2:#fbefff; --f2-s:#8250df; --f1:#fff1e5; --f1-s:#bc4c00;
          --val:#dafbe1; --val-s:#1a7f37; --pad:#f6f8fa; --pad-s:#818b98; --bad:#ffebe9; --bad-s:#cf222e; }
    @media (prefers-color-scheme: dark) {
      svg { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --box:#151b23; --chip:#262c36;
            --f3:#0d2c4f; --f3-s:#4493f8; --f2:#271b45; --f2-s:#ab7df8; --f1:#3a2111; --f1-s:#f0883e;
            --val:#0f2d1a; --val-s:#3fb950; --pad:#151b23; --pad-s:#9198a1; --bad:#3d1418; --bad-s:#f85149; }
    }
    text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: var(--fg); font-size: 13px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
    .h1 { font-size: 22px; font-weight: 700; }
    .h2 { font-size: 15px; font-weight: 700; }
    .b { font-weight: 700; }
    .sm { font-size: 11.5px; }
    .xs { font-size: 10.5px; }
    .muted { fill: var(--muted); }
    .ok { fill: var(--val-s); font-weight: 700; }
    .err { fill: var(--bad-s); font-weight: 700; }
    .t3 { fill: var(--f3-s); } .t2 { fill: var(--f2-s); } .t1 { fill: var(--f1-s); }
    .chip rect { fill: var(--chip); }
    .chip text { font-size: 10.5px; font-weight: 700; fill: var(--muted); text-anchor: middle; }
    .bg { fill: var(--bg); }
    .box { fill: var(--box); stroke: var(--line); stroke-width: 1.5; }
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .empty { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .f3 { fill: var(--f3); stroke: var(--f3-s); stroke-width: 1.2; }
    .f2 { fill: var(--f2); stroke: var(--f2-s); stroke-width: 1.2; }
    .f1 { fill: var(--f1); stroke: var(--f1-s); stroke-width: 1.2; }
    .fr3 { fill: var(--f3); stroke: var(--f3-s); stroke-width: 2; }
    .fr2 { fill: var(--f2); stroke: var(--f2-s); stroke-width: 2; }
    .fr1 { fill: var(--f1); stroke: var(--f1-s); stroke-width: 2; }
    .frm { fill: var(--bg); stroke: var(--muted); stroke-width: 2; }
    .val { fill: var(--val); stroke: var(--val-s); stroke-width: 2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .hit { stroke: var(--fg); stroke-width: 2.5; }
    .bar3 { stroke: var(--f3-s); stroke-width: 4; } .bar2 { stroke: var(--f2-s); stroke-width: 4; } .bar1 { stroke: var(--f1-s); stroke-width: 4; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-val { stroke: var(--val-s); }  .m-val { fill: var(--val-s); }
    .a-f2 { stroke: var(--f2-s); }    .m-f2 { fill: var(--f2-s); }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Виклик, повернення і стек</title>')
o('  <desc id="desc">Чотири панелі до теорії Lab 07. 1: fact(3) в ember за лістингом з ISA §6: п\'ять знімків стека 0xFFF…0xFF7 на кроках 2, 11, 27, 30 і 34 трасування; CALL кладе адресу повернення, PUSH A зберігає n, кадри fact(3), fact(2), fact(1); POP і RET лише піднімають SP, старі байти лишаються. 2: у C++ кожен виклик fact має свій n, значення повертаються 1, 2, 6. 3: передача за значенням, за вказівником і за посиланням. 4: стек як тип: top — останній зайнятий, SP — наступний вільний.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-val"); marker("m-f2")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Виклик і повернення: стек</text>')
o('<text class="muted" x="24" y="60"><tspan class="mono">CALL</tspan> — це стрибок, який пам\'ятає, куди повернутись. Пам\'ятає він на стеку.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 07</text>')
o('<rect class="pad" x="924" y="26" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="37">старий байт</text>')
o('<rect class="f3" x="702" y="48" width="22" height="14" rx="2"/>')
o('<rect class="f2" x="728" y="48" width="22" height="14" rx="2"/>')
o('<rect class="f1" x="754" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="786" y="59">кадри <tspan class="mono">fact(3)</tspan>, <tspan class="mono">fact(2)</tspan>, <tspan class="mono">fact(1)</tspan></text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. fact(3) в ember -->')
o('<rect class="box" x="24" y="84" width="1032" height="482" rx="10"/>')
o('<text class="h2" x="44" y="110">1. <tspan class="mono">fact(3)</tspan> в <tspan class="mono">ember</tspan>: стек крок за кроком</text>')
chip(982, 96, "§1"); chip(1016, 96, "§3")
o('<text class="sm muted" x="44" y="130">Лістинг з ISA §6, тільки <tspan class="mono">LOADI A, 3</tspan>. Номери кроків — з трасування <tspan class="mono">./run.sh 09 a=3</tspan> у практиці Lab 07.</text>')

# лістинг
listing = [
    ("0000", "20 03", "", "LOADI A, 3", "", ""),
    ("0002", "54 07 00", "", "CALL  fact", "b", ""),
    ("0005", "03", "", "OUTN", "", "← сюди RET"),
    ("0006", "00", "", "HALT", "", ""),
    None,
    ("0007", "21 00", "fact:", "LOADI B, 0", "", ""),
    ("0009", "1A", "", "CMP   A, B", "", "n == 0 ?"),
    ("000A", "31 1B 00", "", "JZ    base", "", ""),
    ("000D", "21 01", "", "LOADI B, 1", "", ""),
    ("000F", "1A", "", "CMP   A, B", "", "n == 1 ?"),
    ("0010", "31 1B 00", "", "JZ    base", "", ""),
    ("0013", "50", "", "PUSH  A", "b", "зберегти n"),
    ("0014", "19", "", "DEC   A", "", "n − 1"),
    ("0015", "54 07 00", "", "CALL  fact", "b", ""),
    ("0018", "53", "", "POP   B", "b", "← сюди RET"),
    ("0019", "1B", "", "MUL   A, B", "", ""),
    ("001A", "55", "", "RET", "b", ""),
    ("001B", "20 01", "base:", "LOADI A, 1", "", ""),
    ("001D", "55", "", "RET", "b", ""),
]
o('<rect class="cell" x="44" y="142" width="320" height="346" rx="6"/>')
y = 162
for row in listing:
    if row is None:
        y += 8
        continue
    addr, bts, lab, ins, bold, note = row
    o(f'<text class="sm mono muted" x="56" y="{y}">{addr}</text>')
    o(f'<text class="sm mono muted" x="92" y="{y}">{bts}</text>')
    if lab:
        o(f'<text class="sm mono" x="154" y="{y}">{lab}</text>')
    o(f'<text class="sm mono{" b" if bold else ""}" x="194" y="{y}">{ins}</text>')
    if note:
        ncls = "sm ok" if note.startswith("←") else "xs muted"
        o(f'<text class="{ncls}" x="280" y="{y}">{note}</text>')
    y += 18

# знімки стека
ADDRS = ["0xFFF", "0xFFE", "0xFFD", "0xFFC", "0xFFB", "0xFFA", "0xFF9", "0xFF8", "0xFF7"]
VALS = ["05", "00", "03", "18", "00", "02", "18", "00", ""]
FRAME = [3, 3, 3, 2, 2, 2, 1, 1, None]
snaps = [
    ("крок 2", "виклик fact(3)", 2, 2, "A = 3", "B = 0"),
    ("крок 11", "виклик fact(2)", 5, 5, "A = 2", "B = 1"),
    ("крок 27", "fact(1): база", 8, 8, "A = 1", "B = 1"),
    ("крок 30", "fact(2): MUL", 5, 8, "A = 2", "B = 2"),
    ("крок 34", "назад у main", 0, 8, "A = 6", "B = 3"),
]
RY, RH, CW = 184, 28, 58
for r, a in enumerate(ADDRS):
    o(f'<text class="xs mono muted" x="420" y="{RY + RH * r + 18}" text-anchor="end">{a}</text>')
for k, (h1, h2, live, written, ra, rb) in enumerate(snaps):
    x = 430 + 104 * k
    o(f'<text class="sm b" x="{x}" y="160">{h1}</text>')
    o(f'<text class="xs muted" x="{x}" y="175">{h2}</text>')
    for r in range(9):
        yy = RY + RH * r
        if r < live:
            c, t = f"f{FRAME[r]}", "sm mono b"
        elif r < written:
            c, t = "pad", "sm mono muted"
        else:
            c, t = "empty", ""
        o(f'<rect class="{c}" x="{x}" y="{yy}" width="{CW}" height="{RH}"/>')
        if t and VALS[r]:
            o(f'<text class="{t}" x="{x + CW / 2:g}" y="{yy + 19}" text-anchor="middle">{VALS[r]}</text>')
    sy = RY + RH * live + 18
    o(f'<text class="sm mono b" x="{x + CW + 4}" y="{sy}">◀ SP</text>')
    o(f'<text class="sm mono" x="{x}" y="456">{ra}</text>')
    o(f'<text class="sm mono muted" x="{x}" y="474">{rb}</text>')

# ролі комірок
roles = [(0, 3, 3, "кадр fact(3)", "ret = 0x0005", "n = 3"),
         (3, 6, 2, "кадр fact(2)", "ret = 0x0018", "n = 2"),
         (6, 8, 1, "кадр fact(1)", "ret = 0x0018", "")]
for r0, r1, f, name, ret, n in roles:
    o(f'<line class="bar{f}" x1="958" y1="{RY + RH * r0 + 3}" x2="958" y2="{RY + RH * r1 - 3}"/>')
    o(f'<text class="sm b t{f}" x="966" y="{RY + RH * r0 + 18}">{name.split()[0]}<tspan class="mono"> {name.split()[1]}</tspan></text>')
    o(f'<text class="xs mono" x="966" y="{RY + RH * (r0 + 1) + 18}">{ret}</text>')
    if n:
        o(f'<text class="xs mono" x="966" y="{RY + RH * (r0 + 2) + 18}">{n}</text>')

o('<text class="sm" x="44" y="510"><tspan class="mono b">CALL</tspan> кладе адресу <tspan class="b">після себе</tspan>: молодший байт, потім старший (<tspan class="mono">05</tspan>, <tspan class="mono">00</tspan>). <tspan class="mono b">RET</tspan> знімає їх у зворотному порядку. <tspan class="mono b">PUSH A</tspan> зберігає <tspan class="mono">n</tspan>: наступний виклик зітре <tspan class="mono">A</tspan>.</text>')
o('<text class="sm" x="44" y="530"><tspan class="mono b">POP</tspan> і <tspan class="mono b">RET</tspan> не стирають байтів, лише піднімають <tspan class="mono">SP</tspan>. Сірі комірки — старі значення: їх перезапише наступний <tspan class="mono">PUSH</tspan>.</text>')
o('<text class="sm" x="44" y="550">Після <tspan class="mono">fact(3)</tspan> <tspan class="mono">SP</tspan> знову <tspan class="mono ok">0xFFF</tspan>: кожен <tspan class="mono">PUSH</tspan> має свій <tspan class="mono">POP</tspan>, кожен <tspan class="mono">CALL</tspan> — свій <tspan class="mono">RET</tspan>. Конвенція: аргумент і результат в <tspan class="mono">A</tspan>.</text>')
o()

# ---------- Панель 2 ----------
o('<!-- 2. Кожен виклик — свій n -->')
o('<rect class="box" x="24" y="582" width="508" height="326" rx="10"/>')
o('<text class="h2" x="44" y="608">2. Кожен виклик — свій <tspan class="mono">n</tspan></text>')
chip(492, 594, "§3")
o('<text class="sm mono" x="44" y="632">int fact(int n) {</text>')
o('<text class="sm mono" x="60" y="648">if (n &lt;= 1) return 1;       <tspan class="muted">// база</tspan></text>')
o('<text class="sm mono" x="60" y="664">return n * fact(n - 1);   <tspan class="muted">// менший випадок</tspan></text>')
o('<text class="sm mono" x="44" y="680">}</text>')
frames = [
    ("frm", "main", "", "fact(3)", ""),
    ("fr3", "fact(3)", "n = 3", "3 * fact(2)", "6"),
    ("fr2", "fact(2)", "n = 2", "2 * fact(1)", "2"),
    ("fr1", "fact(1)", "n = 1", "база: 1", "1"),
]
for k, (cls, name, n, expr, ret) in enumerate(frames):
    x, y = 64 + 22 * k, 696 + 42 * k
    o(f'<rect class="{cls}" x="{x}" y="{y}" width="250" height="34" rx="6"/>')
    o(f'<text class="mono b" x="{x + 12}" y="{y + 22}">{name}</text>')
    if n:
        o(f'<text class="mono" x="{x + 82}" y="{y + 22}">{n}</text>')
    o(f'<text class="sm mono" x="{x + (150 if n else 82)}" y="{y + 22}">{expr}</text>')
    if k < 3:
        nx, ny = 64 + 22 * (k + 1), 696 + 42 * (k + 1)
        o(f'<path class="arrow a-io" d="M{x + 18},{y + 36} L{x + 18},{ny + 17} L{nx - 2},{ny + 17}" marker-end="url(#m-io)"/>')
    if ret:
        o(f'<path class="arrow a-val" d="M{x + 252},{y + 17} C{x + 300},{y + 17} {x + 300},{y - 25} {x + 230},{y - 25}" marker-end="url(#m-val)"/>')
        o(f'<text class="sm ok" x="{x + 292}" y="{y - 4}">повертає {ret}</text>')
o('<text class="sm" x="44" y="882">Три різні <tspan class="mono">n</tspan> у трьох різних кадрах; кожен живе, доки його виклик не поверне.</text>')
o('<text class="sm muted" x="44" y="900">Глобальна <tspan class="mono">g_n</tspan> замість параметра — одна коробка на всіх, і <tspan class="mono">fact(4) = 1</tspan>.</text>')
o()

# ---------- Панель 3 ----------
o('<!-- 3. Параметри -->')
o('<rect class="box" x="548" y="582" width="508" height="326" rx="10"/>')
o('<text class="h2" x="568" y="608">3. Як значення потрапляють усередину</text>')
chip(1016, 594, "§2")
o('<text class="sm muted" x="640" y="632" text-anchor="middle">кадр <tspan class="mono">main</tspan></text>')
o('<text class="sm muted" x="835" y="632" text-anchor="middle">кадр <tspan class="mono">inc</tspan></text>')
params = [
    ("void inc(int x)", "inc(a);", "копія", "a = 5", "err"),
    ("void inc(int* p)", "inc(&amp;a);", "адреса", "a = 6", "ok"),
    ("void inc(int&amp; r)", "inc(a);", "інше ім'я", "a = 6", "ok"),
]
for k, (sig, call, how, res, rcls) in enumerate(params):
    top = 642 + 84 * k
    o(f'<text class="sm mono b" x="568" y="{top + 12}">{sig}</text><text class="sm mono muted" x="700" y="{top + 12}">{call}</text>')
    by = top + 22
    o(f'<text class="sm mono b" x="592" y="{by + 21}">a</text>')
    if k == 0:
        o(f'<rect class="val" x="604" y="{by}" width="72" height="32" rx="4"/>')
        o(f'<text class="mono" x="640" y="{by + 21}" text-anchor="middle">5</text>')
        o(f'<path class="arrow a-io dashed" d="M678,{by + 16} L788,{by + 16}" marker-end="url(#m-io)"/>')
        o(f'<text class="xs muted" x="733" y="{by + 11}" text-anchor="middle">{how}</text>')
        o(f'<rect class="f2" x="800" y="{by}" width="72" height="32" rx="4"/>')
        o(f'<text class="mono" x="836" y="{by + 21}" text-anchor="middle">5 → 6</text>')
        o(f'<text class="sm mono b t2" x="878" y="{by + 21}">x</text>')
    elif k == 1:
        o(f'<rect class="val" x="604" y="{by}" width="72" height="32" rx="4"/>')
        o(f'<text class="mono" x="640" y="{by + 21}" text-anchor="middle">5 → 6</text>')
        o(f'<rect class="f2" x="800" y="{by}" width="72" height="32" rx="4"/>')
        o(f'<text class="mono" x="836" y="{by + 21}" text-anchor="middle">&amp;a</text>')
        o(f'<text class="sm mono b t2" x="878" y="{by + 21}">p</text>')
        o(f'<path class="arrow a-f2" d="M798,{by + 16} L680,{by + 16}" marker-end="url(#m-f2)"/>')
        o(f'<text class="xs muted" x="739" y="{by + 11}" text-anchor="middle">{how}: <tspan class="mono">*p += 1</tspan></text>')
    else:
        o(f'<rect class="val" x="604" y="{by}" width="72" height="32" rx="4"/>')
        o(f'<text class="mono" x="640" y="{by + 21}" text-anchor="middle">5 → 6</text>')
        o(f'<text class="sm mono b t2" x="682" y="{by + 21}">r</text>')
        o(f'<text class="xs muted" x="800" y="{by + 13}">своєї коробки немає:</text>')
        o(f'<text class="xs muted" x="800" y="{by + 27}"><tspan class="mono">r</tspan> — ще одне ім\'я для <tspan class="mono">a</tspan></text>')
    o(f'<text class="sm mono {rcls}" x="1036" y="{by + 21}" text-anchor="end">{res}</text>')
o('<text class="sm muted" x="568" y="896"><tspan class="mono">const T&amp;</tspan> — як <tspan class="mono">T&amp;</tspan>, тільки для читання: запис через нього не збереться.</text>')
o()

# ---------- Панель 4 ----------
o('<!-- 4. Стек як тип -->')
o('<rect class="box" x="24" y="924" width="1032" height="182" rx="10"/>')
o('<text class="h2" x="44" y="950">4. Стек як тип: той самий LIFO, інша лічба</text>')
chip(1016, 936, "§5")
srows = [
    ("Stack s;", ["", "", "", ""], [0, 0, 0, 0], None, "top = −1", "порожній"),
    ("push(s, 5);", ["5", "", "", ""], [1, 0, 0, 0], 0, "top = 0", ""),
    ("push(s, 7);", ["5", "7", "", ""], [1, 1, 0, 0], 1, "top = 1", ""),
    ("pop(s, out);", ["5", "7", "", ""], [1, 2, 0, 0], 0, "top = 0", "out = 7"),
]
for k, (lab, vals, st, top, ttxt, note) in enumerate(srows):
    y = 964 + 32 * k
    o(f'<text class="sm mono b" x="44" y="{y + 17}">{lab}</text>')
    for i in range(4):
        x = 150 + 44 * i
        c = {0: "empty", 1: "val", 2: "pad"}[st[i]]
        if c == "val":
            c = "f3"
        if top == i:
            c += " hit"
        o(f'<rect class="{c}" x="{x}" y="{y}" width="44" height="24"/>')
        if vals[i]:
            t = "sm mono muted" if st[i] == 2 else "sm mono b"
            o(f'<text class="{t}" x="{x + 22}" y="{y + 17}" text-anchor="middle">{vals[i]}</text>')
    o(f'<text class="sm mono" x="340" y="{y + 17}">{ttxt}</text>')
    if note:
        o(f'<text class="sm {"ok" if note.startswith("out") else "muted"}" x="420" y="{y + 17}">{note}</text>')
for i in range(4):
    o(f'<text class="xs mono muted" x="{172 + 44 * i}" y="1102" text-anchor="middle">[{i}]</text>')
o('<text class="xs mono muted" x="144" y="1102" text-anchor="end">s.data</text>')

o('<line class="rule" x1="500" y1="940" x2="500" y2="1094"/>')
o('<text class="sm b" x="660" y="972">Stack (хост)</text><text class="sm b" x="850" y="972"><tspan class="mono">SP</tspan> (ember)</text>')
cmp_rows = [
    ("порожній", "top = −1", "SP = 0xFFF"),
    ("вказує на", "останній зайнятий", "наступний вільний"),
    ("росте", "вгору: data[0], data[1]…", "вниз: 0xFFF, 0xFFE…"),
    ("переповнення", "push при top == CAP − 1", "SP нижче 0xF00"),
    ("спустошення", "pop при top == −1", "зняття при SP ≥ 0xFFF"),
]
for k, (lab, host, guest) in enumerate(cmp_rows):
    y = 994 + 22 * k
    o(f'<text class="sm muted" x="520" y="{y}">{lab}</text>')
    o(f'<text class="sm" x="660" y="{y}">{host}</text>')
    o(f'<text class="sm" x="850" y="{y}">{guest}</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
