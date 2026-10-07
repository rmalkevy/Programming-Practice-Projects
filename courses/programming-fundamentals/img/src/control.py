#!/usr/bin/env python3
"""Generate img/control.uk.svg for Lab 04 (jumps, control forms, short-circuit, search, switch)."""
import sys

W, H = 1080, 942
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def cell(x, y, w, h, cls, text="", tcls="mono", rx=0):
    o(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>')
    if text != "":
        o(f'<text class="{tcls}" x="{x + w / 2:g}" y="{y + h / 2 + 5:g}" text-anchor="middle">{text}</text>')

STYLE = """  <style>
    svg { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --box:#f6f8fa; --chip:#e7ecf0;
          --a:#ddf4ff; --a-s:#0969da; --b:#fbefff; --b-s:#8250df; --c:#fff1e5; --c-s:#bc4c00;
          --val:#dafbe1; --val-s:#1a7f37; --pad:#f6f8fa; --pad-s:#818b98; --bad:#ffebe9; --bad-s:#cf222e; }
    @media (prefers-color-scheme: dark) {
      svg { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --box:#151b23; --chip:#262c36;
            --a:#0d2c4f; --a-s:#4493f8; --b:#271b45; --b-s:#ab7df8; --c:#3a2111; --c-s:#f0883e;
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
    .tb { fill: var(--b-s); font-weight: 700; }
    .chip rect { fill: var(--chip); }
    .chip text { font-size: 10.5px; font-weight: 700; fill: var(--muted); text-anchor: middle; }
    .bg { fill: var(--bg); }
    .box { fill: var(--box); stroke: var(--line); stroke-width: 1.5; }
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .ga { fill: var(--a); stroke: var(--a-s); stroke-width: 1.2; }
    .gb { fill: var(--b); stroke: var(--b-s); stroke-width: 1.2; }
    .gc { fill: var(--c); stroke: var(--c-s); stroke-width: 1.2; }
    .gv { fill: var(--val); stroke: var(--val-s); stroke-width: 1.2; }
    .zero { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .bad { fill: var(--bad); stroke: var(--bad-s); stroke-width: 1.5; }
    .ghost { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .brace { fill: none; stroke: var(--muted); stroke-width: 1.2; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-b { stroke: var(--b-s); }      .m-b { fill: var(--b-s); }
    .a-val { stroke: var(--val-s); }  .m-val { fill: var(--val-s); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

def bracket(x1, x2, y):
    o(f'<path class="brace" d="M{x1},{y} v6 H{x2} v-6"/>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Керування: перевірки і стрибки</title>')
o('  <desc id="desc">П\'ять панелей до теорії Lab 04. 1: зворотний відлік з ISA §9 — вісім байтів коду, JNZ стрибає назад на 0x0002, поки Z = 0; три ітерації друкують 3, 2, 1. 2: if/else, while і do … while як блоки з умовними стрибками вперед і безумовними назад. 3: &amp;&amp; і || не обчислюють праву частину, коли відповідь уже відома; 1 &amp;&amp; 2 — true, 1 &amp; 2 — 0. 4: лінійний пошук 0x41 у даних 10 20 41 30: H іде по комірках, CMP, на 0x0802 — збіг, вивід 2; що буде без збігу — питання для M4. 5: switch без break: INC провалюється в DEC, і A лишається 5.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-b"); marker("m-val"); marker("m-bad")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Керування: перевірки і стрибки</text>')
o('<text class="muted" x="24" y="60"><tspan class="mono">if</tspan>, <tspan class="mono">while</tspan>, <tspan class="mono">for</tspan> — це порівняння і стрибки. Цикл — це стрибок назад.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 04</text>')
o('<path class="arrow a-b" d="M702,55 L726,55" marker-end="url(#m-b)"/>')
o('<text class="sm muted" x="736" y="59">стрибок назад</text>')
o('<path class="arrow a-io" d="M884,55 L908,55" marker-end="url(#m-io)"/>')
o('<text class="sm muted" x="918" y="59">стрибок уперед</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Відлік у ember -->')
o('<rect class="box" x="24" y="84" width="1032" height="246" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Цикл — це стрибок назад: відлік 3, 2, 1 в <tspan class="mono">ember</tspan></text>')
chip(982, 96, "§2"); chip(1016, 96, "ISA")
o('<text class="sm muted" x="44" y="130">Програма з ISA §9. Трасування — <tspan class="mono">./run.sh 08</tspan> у практиці Lab 04: 11 кроків.</text>')
X0, CW, CY = 64, 50, 196
code = ["20", "03", "03", "19", "32", "02", "00", "00"]
gcls = ["ga", "ga", "gv", "gc", "gb", "gb", "gb", "zero"]
for i in range(8):
    cell(X0 + CW * i, CY, CW, 36, gcls[i], code[i], "mono b")
    o(f'<text class="xs mono muted" x="{X0 + CW * i + CW // 2}" y="{CY + 50}" text-anchor="middle">000{i}</text>')
groups = [(0, 2, "LOADI A, 3"), (2, 3, "OUTN"), (3, 4, "DEC A"), (4, 7, "JNZ loop"), (7, 8, "HALT")]
for a, b, name in groups:
    bracket(X0 + CW * a + 3, X0 + CW * b - 3, CY + 56)
    o(f'<text class="sm mono" x="{X0 + CW * (a + b) / 2:g}" y="{CY + 78}" text-anchor="middle">{name}</text>')
o(f'<path class="arrow a-b" d="M{X0 + CW * 4 + 25},{CY - 2} C{X0 + CW * 4 + 25},{CY - 46} {X0 + CW * 2 + 25},{CY - 46} {X0 + CW * 2 + 25},{CY - 4}" marker-end="url(#m-b)"/>')
o(f'<text class="sm tb" x="{X0 + CW * 3 + 25}" y="{CY - 42}" text-anchor="middle">Z = 0: PC = 0x0002</text>')
o(f'<path class="arrow a-io dashed" d="M{X0 + CW * 6 + 25},{CY - 2} C{X0 + CW * 6 + 25},{CY - 26} {X0 + CW * 7 + 25},{CY - 26} {X0 + CW * 7 + 25},{CY - 4}" marker-end="url(#m-io)"/>')
o(f'<text class="xs muted" x="{X0 + CW * 7 + 30}" y="{CY - 22}">Z = 1</text>')
o(f'<text class="xs mono muted" x="{X0 + CW * 2 + 25}" y="{CY - 8}" text-anchor="middle"> </text>')
o('<text class="sm" x="44" y="300">Операнд <tspan class="mono">JNZ</tspan> — <tspan class="mono">02 00</tspan>: це <tspan class="mono">0x0002</tspan>, молодший байт уперед.</text>')
o('<text class="sm muted" x="44" y="318">Стрибок спрацював — <tspan class="mono">PC</tspan> = операнд, розмір не додається. Ні — <tspan class="mono">PC += 3</tspan>.</text>')

TX = 520
o(f'<line class="rule" x1="{TX - 16}" y1="144" x2="{TX - 16}" y2="318"/>')
cols = [(TX, "ітерація"), (TX + 76, "OUTN друкує"), (TX + 176, "A після DEC"), (TX + 276, "Z"), (TX + 306, "JNZ")]
for x, h in cols:
    o(f'<text class="sm b" x="{x}" y="164">{h}</text>')
o(f'<line class="rule" x1="{TX}" y1="172" x2="1036" y2="172"/>')
rows = [("1", "3", "2", "0", "назад на 0x0002", "sm tb"),
        ("2", "2", "1", "0", "назад на 0x0002", "sm tb"),
        ("3", "1", "0", "1", "далі: 0x0007, HALT", "sm")]
for k, (it, pr, a, z, j, jcls) in enumerate(rows):
    y = 192 + 22 * k
    o(f'<text class="sm mono" x="{TX + 24}" y="{y}">{it}</text>')
    o(f'<text class="sm mono b" x="{TX + 110}" y="{y}">{pr}</text>')
    o(f'<text class="sm mono" x="{TX + 210}" y="{y}">{a}</text>')
    o(f'<text class="sm mono" x="{TX + 278}" y="{y}">{z}</text>')
    o(f'<text class="{jcls}" x="{TX + 306}" y="{y}">{j}</text>')
o(f'<text class="sm" x="{TX}" y="272">Те саме в C++ — перевірка в кінці:</text>')
o(f'<text class="sm mono" x="{TX}" y="292">a = 3; do {{ print(a); --a; }} while (a != 0);</text>')
o(f'<text class="sm muted" x="{TX}" y="312">Вивід <tspan class="mono">3 2 1</tspan>. <tspan class="mono">LOADI</tspan> прапорців не чіпає — <tspan class="mono">Z</tspan> виставляє <tspan class="mono">DEC</tspan>.</text>')
o()

# ---------- Панель 2 ----------
P = 346
o('<!-- 2. Форми керування -->')
o(f'<rect class="box" x="24" y="{P}" width="508" height="320" rx="10"/>')
o(f'<text class="h2" x="44" y="{P + 26}">2. Форми — це перевірки і стрибки</text>')
chip(492, P + 12, "§2")
def form(cx, title, blocks, jumps):
    o(f'<text class="sm mono b" x="{cx + 16}" y="{P + 54}">{title}</text>')
    bx, bw = cx + 16, 112
    ys = []
    for k, (txt, cls) in enumerate(blocks):
        y = P + 66 + 38 * k
        ys.append(y)
        if cls == "label":
            o(f'<text class="sm mono muted" x="{bx + 6}" y="{y + 17}">{txt}</text>')
        else:
            cell(bx, y, bw, 26, cls, txt, "xs mono", rx=4)
    for i, j, side, d in jumps:
        yi, yj = ys[i] + 13, ys[j] + 13
        if side == "r":
            x = bx + bw
            o(f'<path class="arrow a-io" d="M{x},{yi} C{x + d},{yi} {x + d},{yj} {x + 3},{yj}" marker-end="url(#m-io)"/>')
        else:
            x = bx
            o(f'<path class="arrow a-b" d="M{x},{yi} C{x - d},{yi} {x - d},{yj} {x - 3},{yj}" marker-end="url(#m-b)"/>')
form(28, "if / else",
     [("CMP; JZ else", "gb"), ("then-гілка", "zero"), ("JMP end", "gb"), ("else: else-гілка", "zero"), ("end:", "label")],
     [(0, 3, "r", 22), (2, 4, "r", 34)])
form(196, "while",
     [("top: CMP; JZ end", "gb"), ("тіло", "zero"), ("JMP top", "gb"), ("end:", "label")],
     [(0, 3, "r", 22), (2, 0, "l", 26)])
form(364, "do … while",
     [("top: тіло", "zero"), ("CMP; JNZ top", "gb"), ("end:", "label")],
     [(1, 0, "l", 26)])
o(f'<text class="sm muted" x="44" y="{P + 292}"><tspan class="mono">for</tspan> — це <tspan class="mono">while</tspan> з лічильником. <tspan class="mono">for (;;)</tspan> — <tspan class="mono">JMP</tspan> без умови:</text>')
o(f'<text class="sm muted" x="44" y="{P + 308}">тому <tspan class="mono">run</tspan> має ліміт кроків.</text>')
o()

# ---------- Панель 3 ----------
o('<!-- 3. Коротке замикання -->')
o(f'<rect class="box" x="548" y="{P}" width="508" height="320" rx="10"/>')
o(f'<text class="h2" x="568" y="{P + 26}">3. <tspan class="mono">&amp;&amp;</tspan> і <tspan class="mono">||</tspan> можуть не дивитись праворуч</text>')
chip(1016, P + 12, "§1")
def sc(y, left, op, right, tlab, flab, res):
    cell(568, y, 150, 30, "zero", left, "sm mono", rx=4)
    o(f'<text class="mono b" x="738" y="{y + 20}" text-anchor="middle">{op}</text>')
    cell(760, y, 120, 30, "zero", right, "sm mono", rx=4)
    o(f'<text class="xs muted" x="820" y="{y - 6}" text-anchor="middle">{tlab}</text>')
    o(f'<path class="arrow a-val" d="M643,{y + 32} C643,{y + 56} 960,{y + 56} 960,{y + 34}" marker-end="url(#m-val)"/>')
    cell(912, y, 96, 30, "gv", res, "sm mono b", rx=4)
    o(f'<text class="xs ok" x="800" y="{y + 66}" text-anchor="middle">{flab}</text>')
sc(P + 60, "p != nullptr", "&amp;&amp;", "*p == 3", "читається, лише якщо ліва true", "ліва false → одразу false, *p не читаємо", "false")
sc(P + 164, "a", "||", "b", "рахується, лише якщо ліва false", "ліва true → одразу true, b не рахуємо", "true")
o(f'<text class="sm b" x="568" y="{P + 256}">Логічне — не бітове:</text>')
o(f'<text class="sm mono" x="568" y="{P + 276}" style="white-space:pre">1 &amp;&amp; 2 → true      1 &amp; 2 → 0   <tspan class="muted">(01 &amp; 10 = 00)</tspan></text>')
o(f'<text class="sm" x="568" y="{P + 298}"><tspan class="mono err">if (x = 0)</tspan> — присвоєння, а не порівняння;</text>')
o(f'<text class="sm muted" x="568" y="{P + 314}">з <tspan class="mono">-Werror</tspan> не збереться.</text>')
o()

# ---------- Панель 4 ----------
Q = 682
o('<!-- 4. Лінійний пошук -->')
o(f'<rect class="box" x="24" y="{Q}" width="508" height="244" rx="10"/>')
o(f'<text class="h2" x="44" y="{Q + 26}">4. Лінійний пошук: <tspan class="mono">H</tspan> — це <tspan class="mono">i</tspan></text>')
chip(492, Q + 12, "§3")
o(f'<text class="xs mono" x="44" y="{Q + 48}">loop: LOAD A, [H] · CMP A, B · JZ found · INCH · JMP loop</text>')
o(f'<text class="xs muted" x="44" y="{Q + 64}"><tspan class="mono">H</tspan> — це <tspan class="mono">i</tspan>, <tspan class="mono">INCH</tspan> — <tspan class="mono">++i</tspan>, <tspan class="mono">CMP</tspan> — <tspan class="mono">==</tspan>, <tspan class="mono">JZ</tspan> — <tspan class="mono">if</tspan>. Шукаємо <tspan class="mono">B = 0x41</tspan>.</text>')
SX, SW, SY = 64, 56, Q + 110
data = ["10", "20", "41", "30"]
marks = [("≠", "xs muted", "a-io", "m-io"), ("≠", "xs muted", "a-io", "m-io"), ("= 0x41", "xs ok", "a-val", "m-val")]
for i, v in enumerate(data):
    cell(SX + SW * i, SY, SW, 34, "gv" if i == 2 else "zero", v, "mono b" if i == 2 else "mono")
    o(f'<text class="xs mono muted" x="{SX + SW * i + SW // 2}" y="{SY + 48}" text-anchor="middle">080{i}</text>')
for i, (lab, lcls, a, m) in enumerate(marks):
    cx = SX + SW * i + SW // 2
    o(f'<text class="xs mono b" x="{cx}" y="{SY - 28}" text-anchor="middle">H</text>')
    o(f'<path class="arrow {a}" d="M{cx},{SY - 24} L{cx},{SY - 3}" marker-end="url(#{m})"/>')
    o(f'<text class="{lcls}" x="{cx + 8}" y="{SY - 10}">{lab}</text>')
cell(SX + SW * 4, SY, SW, 34, "ghost", "…", "mono muted")
cell(SX + SW * 5, SY, SW, 34, "ghost", "?", "mono err")
o(f'<text class="sm" x="{SX + SW * 6 + 12}" y="{SY + 14}"><tspan class="mono">HLOW</tspan> → <tspan class="mono">A = 2</tspan></text>')
o(f'<text class="sm" x="{SX + SW * 6 + 12}" y="{SY + 32}"><tspan class="mono">OUTN</tspan> друкує <tspan class="mono ok">2</tspan></text>')
o(f'<text class="sm b" x="44" y="{Q + 192}">А якщо <tspan class="mono">0x41</tspan> у даних немає?</text>')
o(f'<text class="sm muted" x="44" y="{Q + 210}"><tspan class="mono">H</tspan> іде далі: <tspan class="mono">0x0804</tspan>, <tspan class="mono">0x0805</tspan>, … Як зупинити цикл на <tspan class="mono">hi</tspan></text>')
o(f'<text class="sm muted" x="44" y="{Q + 226}">і як сказати про промах — вирішуєте ви в M4.</text>')
o()

# ---------- Панель 5 ----------
o('<!-- 5. switch -->')
o(f'<rect class="box" x="548" y="{Q}" width="508" height="244" rx="10"/>')
o(f'<text class="h2" x="568" y="{Q + 26}">5. <tspan class="mono">switch</tspan>: без <tspan class="mono">break</tspan> виконання провалюється</text>')
chip(1016, Q + 12, "§2")
o(f'<text class="xs mono muted" x="568" y="{Q + 48}">op = 0x18 (INC A), A = 5</text>')
for k, (title, l1, l2, ghost2, res, rcls) in enumerate([
        ("без break", "case 0x18: a++;", "case 0x19: a--; break;", False, "A = 5", "err"),
        ("з break", "case 0x18: a++; break;", "case 0x19: a--; break;", True, "A = 6", "ok")]):
    x = 568 + 244 * k
    o(f'<text class="sm b" x="{x}" y="{Q + 74}">{title}</text>')
    cell(x, Q + 84, 220, 30, "gb", l1, "sm mono", rx=4)
    cell(x, Q + 144, 220, 30, "ghost" if ghost2 else "gb", l2, "sm mono muted" if ghost2 else "sm mono", rx=4)
    if not ghost2:
        o(f'<path class="arrow a-bad" d="M{x + 110},{Q + 116} L{x + 110},{Q + 142}" marker-end="url(#m-bad)"/>')
        o(f'<text class="xs err" x="{x + 118}" y="{Q + 134}">break немає — далі</text>')
    else:
        o(f'<path class="arrow a-val" d="M{x + 222},{Q + 99} C{x + 236},{Q + 99} {x + 236},{Q + 196} {x + 60},{Q + 196}" marker-end="url(#m-val)"/>')
        o(f'<text class="xs muted" x="{x + 110}" y="{Q + 134}" text-anchor="middle">не виконується</text>')
    o(f'<text class="sm mono {rcls}" x="{x}" y="{Q + 200}">{res}</text>')
o(f'<text class="sm muted" x="568" y="{Q + 228}"><tspan class="mono">default:</tspan> — невідомий опкод (<tspan class="mono">0x77</tspan>) це помилка, а не тиша.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
