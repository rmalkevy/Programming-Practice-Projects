#!/usr/bin/env python3
"""Generate img/types.uk.svg for Lab 01 (kinds of errors, types as sizes, overflow and floating point)."""
import sys

W, H = 1080, 600
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
    .chip rect { fill: var(--chip); }
    .chip text { font-size: 10.5px; font-weight: 700; fill: var(--muted); text-anchor: middle; }
    .bg { fill: var(--bg); }
    .box { fill: var(--box); stroke: var(--line); stroke-width: 1.5; }
    .stage { fill: var(--bg); stroke: var(--muted); stroke-width: 1.5; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .t1 { fill: var(--a); stroke: var(--a-s); stroke-width: 1.2; }
    .t2 { fill: var(--b); stroke: var(--b-s); stroke-width: 1.2; }
    .t4 { fill: var(--val); stroke: var(--val-s); stroke-width: 1.2; }
    .t8 { fill: var(--c); stroke: var(--c-s); stroke-width: 1.2; }
    .one { fill: var(--val); stroke: var(--val-s); stroke-width: 1.2; }
    .zero { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .hit { stroke: var(--fg); stroke-width: 2.5; }
    .bad { fill: var(--bad); stroke: var(--bad-s); stroke-width: 1.5; }
    .x-bad { stroke: var(--bad-s); stroke-width: 2.5; stroke-linecap: round; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-val { stroke: var(--val-s); }  .m-val { fill: var(--val-s); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

def cross(x, y):
    o(f'<path class="x-bad" d="M{x - 5},{y - 5} L{x + 5},{y + 5} M{x + 5},{y - 5} L{x - 5},{y + 5}"/>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Коробка байтів: помилки й типи</title>')
o('  <desc id="desc">Три панелі до теорії Lab 01. 1: шлях від тексту до запуску і де зупиняються три види помилок: синтаксична і попередження з -Werror — у компіляторі, програми немає; помилка виконання — під час запуску, як 10 / 0 під UBSan. 2: тип — це розмір: uint8_t, uint16_t, int, double і void* як 1, 2, 4, 8 і 8 байтів із діапазонами; один байт 01000001 — це 65, 0x41 і \'A\', а \'A\' ^ 32 — це \'a\'. 3: uint8_t загортається 255 → 0, int на INT_MAX + 1 — невизначена поведінка; 0.1 + 0.2 не дорівнює 0.3.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-val"); marker("m-bad")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Коробка байтів: помилки й типи</text>')
o('<text class="muted" x="24" y="60">Ви пишете текст, машина виконує байти. Тип каже, скільки байтів і що з ними можна робити.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 01</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Три види помилок -->')
o('<rect class="box" x="24" y="84" width="1032" height="176" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Виконується не той текст, який ви написали</text>')
chip(1016, 96, "§1")
stages = [(44, 150, "source.cpp", "текст"), (234, 200, "компілятор", "-Wall -Wextra -Werror"),
          (474, 170, "програма", "машинний код"), (684, 190, "запуск", "ASan, UBSan стежать"), (914, 122, "вивід", "")]
for k, (x, w, t1, t2) in enumerate(stages):
    o(f'<rect class="stage" x="{x}" y="124" width="{w}" height="44" rx="6"/>')
    o(f'<text class="sm b{" mono" if k == 0 else ""}" x="{x + w / 2:g}" y="{142 if t2 else 151}" text-anchor="middle">{t1}</text>')
    if t2:
        o(f'<text class="xs{" mono" if k == 1 else ""} muted" x="{x + w / 2:g}" y="{159}" text-anchor="middle">{t2}</text>')
    if k < 4:
        o(f'<path class="arrow a-io" d="M{x + w + 3},146 L{stages[k + 1][0] - 3},146" marker-end="url(#m-io)"/>')
errs = [("синтаксична помилка", 334, "компілятор відмовився перекладати — програми немає"),
        ("попередження", 334, "з -Werror підозра стає помилкою — програми теж немає"),
        ("помилка виконання", 779, "")]
for k, (lab, cx, note) in enumerate(errs):
    y = 194 + 22 * k
    o(f'<text class="sm b" x="44" y="{y + 4}">{lab}</text>')
    cross(cx, y)
    if note:
        o(f'<text class="xs muted" x="{cx + 14}" y="{y + 4}">{note}</text>')
o('<text class="xs muted" x="474" y="242">програма є і вже біжить — ловить санітайзер</text>')
o('<text class="xs mono err" x="793" y="242">10 / 0 → division by zero</text>')
o()

# ---------- Панель 2 ----------
P = 276
o('<!-- 2. Тип — це розмір -->')
o(f'<rect class="box" x="24" y="{P}" width="508" height="308" rx="10"/>')
o(f'<text class="h2" x="44" y="{P + 26}">2. Тип — це розмір і набір операцій</text>')
chip(492, P + 12, "§2")
o(f'<text class="xs muted" x="44" y="{P + 46}">Числа — з <tspan class="mono">./run.sh 02</tspan> на 64-бітному Mac. Своє число друкуйте, а не завчайте.</text>')
types = [("std::uint8_t", 1, "t1", "0 … 255 — комірка ember"),
         ("std::uint16_t", 2, "t2", "0 … 65535 — адреса ember"),
         ("int", 4, "t4", "−2147483648 … 2147483647"),
         ("double", 8, "t8", "~15 десяткових цифр"),
         ("void*", 8, "t8", "ширина адреси (Lab 3)")]
for k, (name, n, cls, rng) in enumerate(types):
    y = P + 58 + 28 * k
    o(f'<text class="sm mono b" x="44" y="{y + 15}">{name}</text>')
    for i in range(n):
        cell(150 + 22 * i, y, 22, 20, cls)
    o(f'<text class="xs mono muted" x="{150 + 22 * n + 6}" y="{y + 14}">{n}</text>')
    o(f'<text class="xs" x="{150 + 22 * 8 + 26}" y="{y + 14}">{rng}</text>')
o(f'<line class="rule" x1="44" y1="{P + 204}" x2="512" y2="{P + 204}"/>')
o(f'<text class="sm b" x="44" y="{P + 226}">Один байт — чотири записи:</text>')
bits = "01000001"
for i, b in enumerate(bits):
    cls = ("one" if b == "1" else "zero") + (" hit" if i == 2 else "")
    cell(44 + 26 * i, P + 236, 26, 26, cls, b, "sm mono b" if b == "1" else "sm mono muted")
    o(f'<text class="xs mono muted" x="{44 + 26 * i + 13}" y="{P + 274}" text-anchor="middle">{7 - i}</text>')
o(f'<text class="sm mono" x="270" y="{P + 254}">65 · 0x41 · \'A\'</text>')
o(f'<text class="xs muted" x="270" y="{P + 274}">ті самі біти; розповідь веде тип</text>')
o(f'<text class="sm" x="44" y="{P + 296}"><tspan class="mono">\'A\' ^ 32</tspan> = <tspan class="mono">\'a\'</tspan>: велика й мала літера різняться одним бітом 5.</text>')
o()

# ---------- Панель 3 ----------
o('<!-- 3. Переповнення й рухома кома -->')
o(f'<rect class="box" x="548" y="{P}" width="508" height="308" rx="10"/>')
o(f'<text class="h2" x="568" y="{P + 26}">3. Переповнення, рухома кома й інша брехня</text>')
chip(1016, P + 12, "§3")
o(f'<text class="sm b" x="568" y="{P + 52}"><tspan class="mono">std::uint8_t</tspan>, +1: загортається, і це визначено</text>')
wrap = ["253", "254", "255", "0", "1", "2"]
for i, v in enumerate(wrap):
    cell(568 + 52 * i, P + 62, 52, 26, "t1", v, "sm mono")
o(f'<path class="arrow a-val" d="M{568 + 52 * 2 + 26},{P + 90} C{568 + 52 * 2 + 26},{P + 110} {568 + 52 * 3 + 26},{P + 110} {568 + 52 * 3 + 26},{P + 92}" marker-end="url(#m-val)"/>')
o(f'<text class="xs ok" x="{568 + 52 * 6 + 10}" y="{P + 80}">255 + 1 = 0</text>')
o(f'<text class="sm b" x="568" y="{P + 132}"><tspan class="mono">int</tspan>, +1 після <tspan class="mono">INT_MAX</tspan>: невизначена поведінка</text>')
cell(568, P + 142, 110, 26, "t4", "2147483646", "sm mono")
cell(678, P + 142, 110, 26, "t4", "2147483647", "sm mono")
cell(788, P + 142, 110, 26, "bad", "?", "sm mono err")
o(f'<text class="xs mono err" x="568" y="{P + 186}">runtime error: signed integer overflow: 2147483647 + 1</text>')
o(f'<text class="xs muted" x="568" y="{P + 202}">Компілятор може вважати, що цього не буває: <tspan class="mono">x + 1 &gt; x</tspan> — «завжди true».</text>')
o(f'<line class="rule" x1="568" y1="{P + 214}" x2="1036" y2="{P + 214}"/>')
o(f'<text class="sm b" x="568" y="{P + 236}"><tspan class="mono">double</tspan>: більшість десяткових дробів не вміщаються</text>')
o(f'<text class="sm mono" x="568" y="{P + 256}">0.1 + 0.2 = 0.30000000000000004</text>')
o(f'<text class="sm mono" x="568" y="{P + 274}" style="white-space:pre">0.3       = 0.29999999999999999</text>')
o(f'<text class="sm" x="568" y="{P + 296}"><tspan class="mono">a + b == c</tspan> → <tspan class="err">false</tspan>; з допуском <tspan class="mono">|a + b − c| &lt; 1e-9</tspan> → <tspan class="ok">true</tspan></text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
