#!/usr/bin/env python3
"""Generate img/arrays.uk.svg for Lab 05 (arrays, 2D, the screen, strings, bubble sort)."""
import sys

W, H = 1080, 852
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def cell(x, y, w, h, cls, text="", tcls="mono", ty=None):
    o(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    if text != "":
        o(f'<text class="{tcls}" x="{x + w / 2:g}" y="{ty if ty is not None else y + h / 2 + 5:g}" text-anchor="middle">{text}</text>')

STYLE = """  <style>
    svg { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --box:#f6f8fa; --chip:#e7ecf0;
          --r0:#ddf4ff; --r0-s:#0969da; --r1:#fbefff; --r1-s:#8250df; --r2:#fff1e5; --r2-s:#bc4c00;
          --val:#dafbe1; --val-s:#1a7f37; --pad:#f6f8fa; --pad-s:#818b98; --bad:#ffebe9; --bad-s:#cf222e; --row:#ddf4ff; }
    @media (prefers-color-scheme: dark) {
      svg { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --box:#151b23; --chip:#262c36;
            --r0:#0d2c4f; --r0-s:#4493f8; --r1:#271b45; --r1-s:#ab7df8; --r2:#3a2111; --r2-s:#f0883e;
            --val:#0f2d1a; --val-s:#3fb950; --pad:#151b23; --pad-s:#9198a1; --bad:#3d1418; --bad-s:#f85149; --row:#0d2c4f; }
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
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .faint { stroke: var(--line); stroke-width: 0.6; }
    .zero { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .val { fill: var(--val); stroke: var(--val-s); stroke-width: 1.2; }
    .r0 { fill: var(--r0); stroke: var(--r0-s); stroke-width: 1.2; }
    .r1 { fill: var(--r1); stroke: var(--r1-s); stroke-width: 1.2; }
    .r2 { fill: var(--r2); stroke: var(--r2-s); stroke-width: 1.2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .bad { fill: var(--bad); stroke: var(--bad-s); stroke-width: 1.5; stroke-dasharray: 4 3; }
    .hit { stroke: var(--fg); stroke-width: 2.5; }
    .screen { fill: var(--bg); stroke: var(--muted); stroke-width: 1.5; }
    .rowband { fill: var(--row); }
    .bytebox { fill: none; stroke: var(--fg); stroke-width: 2; }
    .pixel { fill: var(--fg); }
    .zoom { stroke: var(--muted); stroke-width: 1; stroke-dasharray: 3 3; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-ptr { stroke: var(--r1-s); }   .m-ptr { fill: var(--r1-s); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Масиви, екран і рядки</title>')
o('  <desc id="desc">П\'ять панелей до теорії Lab 05. 1: Byte buf[8] = {1, 2, 3} — вісім комірок, решта нулі; buf[i] — це *(buf + i); buf[8] за краєм. 2: int m[3][4] як таблиця і як пам\'ять, k = r * 4 + c, m[1][2] — це k = 6. 3: екран 64 × 32 у 256 байтах з 0xA00: піксель (13, 2) — байт 0xA11, біт 2, маска 0x04; без «7 −» засвічується x = 10. 4: char s[4] = "HI" і strlen до першого нуля; "ABCD" без місця для нуля. 5: бульбашка на 4 1 3 2: шість порівнянь, чотири обміни.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-ptr"); marker("m-bad")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Масиви, екран і рядки</text>')
o('<text class="muted" x="24" y="60">Масив — це пам\'ять підряд плюс правило, де лежить i-й елемент. Решта — наслідки цього правила.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 05</text>')
o('<rect class="val" x="924" y="26" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="37">значення</text>')
o('<rect class="bad" x="702" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="736" y="59">за краєм масиву</text>')
o('<rect class="zero" x="924" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="59">нуль</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Масив -->')
o('<rect class="box" x="24" y="84" width="508" height="228" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Масив — пам\'ять плюс правило</text>')
chip(492, 96, "§1")
o('<text class="sm mono" x="44" y="134">Byte buf[8] = {1, 2, 3};   <tspan class="muted">// решта — нулі</tspan></text>')
X0, CW = 44, 48
vals = ["1", "2", "3", "0", "0", "0", "0", "0"]
for i, v in enumerate(vals):
    cell(X0 + CW * i, 172, CW, 34, "val" if i < 3 else "zero", v, "mono b" if i < 3 else "mono muted")
    o(f'<text class="xs mono muted" x="{X0 + CW * i + CW // 2}" y="222" text-anchor="middle">[{i}]</text>')
cell(X0 + CW * 8, 172, CW, 34, "bad", "?", "mono err")
o(f'<text class="xs mono err" x="{X0 + CW * 8 + CW // 2}" y="222" text-anchor="middle">[8]</text>')
for i, lab in [(0, "buf"), (5, "buf + 5")]:
    cx = X0 + CW * i + CW // 2
    o(f'<text class="sm mono b" x="{cx}" y="152" text-anchor="middle">{lab}</text>')
    o(f'<path class="arrow a-ptr" d="M{cx},156 L{cx},170" marker-end="url(#m-ptr)"/>')
o('<text class="sm" x="44" y="248"><tspan class="mono">buf[i]</tspan> — це <tspan class="mono">*(buf + i)</tspan>: адреса першого елемента плюс <tspan class="mono">i</tspan> кроків (Lab 3).</text>')
o('<text class="sm" x="44" y="268"><tspan class="mono err">buf[8]</tspan> — уже не масив: ASan зупинить програму.</text>')
o('<text class="sm muted" x="44" y="288">У функцію <tspan class="mono">buf</tspan> приходить як вказівник, тому розмір передають окремо:</text>')
o('<text class="sm mono muted" x="44" y="304">f(buf, 8)</text>')
o()

# ---------- Панель 2 ----------
o('<!-- 2. Два виміри -->')
o('<rect class="box" x="548" y="84" width="508" height="228" rx="10"/>')
o('<text class="h2" x="568" y="110">2. Два виміри — це один вимір і крок</text>')
chip(1016, 96, "§2")
TX, TY, TW, TH = 600, 140, 34, 22
for c in range(4):
    o(f'<text class="xs mono muted" x="{TX + TW * c + TW // 2}" y="{TY - 6}" text-anchor="middle">{c}</text>')
for r in range(3):
    o(f'<text class="xs mono muted" x="{TX - 8}" y="{TY + TH * r + 15}" text-anchor="end">{r}</text>')
    for c in range(4):
        cls = f"r{r}" + (" hit" if (r, c) == (1, 2) else "")
        cell(TX + TW * c, TY + TH * r, TW, TH, cls, f"{r * 10 + c}", "sm mono" + (" b" if (r, c) == (1, 2) else ""))
o(f'<text class="xs muted" x="{TX + 68}" y="{TY + 3 * TH + 14}" text-anchor="middle">int m[3][4]</text>')
o('<text class="mono b" x="770" y="158">k = r * 4 + c</text>')
o('<text class="sm" x="770" y="180"><tspan class="mono">m[1][2]</tspan> → <tspan class="mono">k = 1·4 + 2 = 6</tspan></text>')
o('<text class="sm muted" x="770" y="200">рядок лежить у пам\'яті поруч</text>')
o('<text class="sm muted" x="568" y="240">у пам\'яті:</text>')
SX, SW = 632, 34
for k in range(12):
    r, c = divmod(k, 4)
    cls = f"r{r}" + (" hit" if k == 6 else "")
    cell(SX + SW * k, 228, SW, 22, cls, f"{r * 10 + c}", "sm mono" + (" b" if k == 6 else ""))
    o(f'<text class="xs mono muted" x="{SX + SW * k + SW // 2}" y="264" text-anchor="middle">{k}</text>')
o('<text class="xs muted" x="620" y="264" text-anchor="end">k</text>')
o('<text class="sm muted" x="568" y="286">Обхід рядками йде підряд; колонками — стрибками по 4 елементи</text>')
o('<text class="sm muted" x="568" y="302">(16 байтів для <tspan class="mono">int</tspan>). Переплутана формула <tspan class="mono">c * 3 + r</tspan> дає інший елемент.</text>')
o()

# ---------- Панель 3 ----------
P = 328
o('<!-- 3. Екран -->')
o(f'<rect class="box" x="24" y="{P}" width="1032" height="268" rx="10"/>')
o(f'<text class="h2" x="44" y="{P + 26}">3. Піксель — це біт: екран 64 × 32 у 256 байтах</text>')
chip(1016, P + 12, "§2")
o(f'<text class="sm muted" x="44" y="{P + 46}">Піксель <tspan class="mono">(13, 2)</tspan>. Формули — з ISA §7; ті самі числа друкує <tspan class="mono">./run.sh 03 13 2</tspan> у практиці Lab 05.</text>')
SX0, SY0, PX = 64, P + 72, 5
o(f'<text class="xs mono muted" x="{SX0}" y="{SY0 - 6}">x = 0</text>')
o(f'<text class="xs mono muted" x="{SX0 + 64 * PX}" y="{SY0 - 6}" text-anchor="end">63</text>')
o(f'<text class="xs mono muted" x="{SX0 - 6}" y="{SY0 + 8}" text-anchor="end">0</text>')
o(f'<text class="xs mono muted" x="{SX0 - 6}" y="{SY0 + 32 * PX}" text-anchor="end">31</text>')
o(f'<rect class="screen" x="{SX0}" y="{SY0}" width="{64 * PX}" height="{32 * PX}"/>')
o(f'<rect class="rowband" x="{SX0}" y="{SY0 + 2 * PX}" width="{64 * PX}" height="{PX}"/>')
for r in range(1, 32):
    o(f'<line class="faint" x1="{SX0}" y1="{SY0 + r * PX}" x2="{SX0 + 64 * PX}" y2="{SY0 + r * PX}"/>')
for b in range(1, 8):
    o(f'<line class="rule" x1="{SX0 + 40 * b}" y1="{SY0}" x2="{SX0 + 40 * b}" y2="{SY0 + 32 * PX}"/>')
o(f'<rect class="pixel" x="{SX0 + 13 * PX}" y="{SY0 + 2 * PX}" width="{PX}" height="{PX}"/>')
o(f'<rect class="bytebox" x="{SX0 + 8 * PX}" y="{SY0 + 2 * PX}" width="{8 * PX}" height="{PX}"/>')
o(f'<path class="arrow a-io" d="M{SX0 + 13 * PX + 2.5:g},{SY0 + 44} L{SX0 + 13 * PX + 2.5:g},{SY0 + 3 * PX + 3}" marker-end="url(#m-io)"/>')
o(f'<text class="sm" x="{SX0 + 13 * PX - 8:g}" y="{SY0 + 58}" style="paint-order:stroke" stroke="var(--bg)" stroke-width="5">піксель <tspan class="mono">(13, 2)</tspan>: рядок 2, байт 1 цього рядка</text>')
o(f'<text class="sm muted" x="{SX0}" y="{SY0 + 32 * PX + 20}">8 байтів на рядок × 32 рядки, з <tspan class="mono">0xA00</tspan></text>')

ZX, ZY, ZW = 440, P + 86, 40
o(f'<text x="{ZX}" y="{ZY - 24}"><tspan class="mono b">mem[0xA11]</tspan><tspan class="sm muted"> — пікселі x = 8…15 рядка 2</tspan></text>')
o(f'<line class="zoom" x1="{SX0 + 16 * PX}" y1="{SY0 + 2 * PX}" x2="{ZX}" y2="{ZY}"/>')
o(f'<line class="zoom" x1="{SX0 + 16 * PX}" y1="{SY0 + 3 * PX}" x2="{ZX}" y2="{ZY + 36}"/>')
for i in range(8):
    x = ZX + ZW * i
    lit = (i == 5)
    cell(x, ZY, ZW, 36, "val" if lit else "zero", "1" if lit else "0", "mono b" if lit else "mono muted")
    o(f'<text class="xs mono muted" x="{x + ZW // 2}" y="{ZY - 6}" text-anchor="middle">{7 - i}</text>')
    o(f'<text class="xs mono" x="{x + ZW // 2}" y="{ZY + 50}" text-anchor="middle">{8 + i}</text>')
o(f'<text class="xs muted" x="{ZX - 6}" y="{ZY - 6}" text-anchor="end">біт</text>')
o(f'<text class="xs muted" x="{ZX - 6}" y="{ZY + 50}" text-anchor="end">x</text>')
fy = ZY + 70
for k, line in enumerate([
    "адреса = 0xA00 + y·8 + x/8",
    "       = 0xA00 + 16 + 1 = 0xA11",
    "біт    = 7 − x%8 = 7 − 5 = 2",
    "маска  = 1 &lt;&lt; 2 = 0x04",
    "горить = (mem[0xA11] &gt;&gt; 2) &amp; 1",
]):
    o(f'<text class="sm mono" x="{ZX}" y="{fy + 17 * k}" style="white-space:pre">{line}</text>')
o(f'<text class="sm muted" x="{ZX}" y="{SY0 + 32 * PX + 20}">Засвітити <tspan class="mono">|= 0x04</tspan>, погасити <tspan class="mono">&amp;= ~0x04</tspan>: трійка з Lab 2.</text>')

RX = 800
o(f'<line class="rule" x1="{RX - 20}" y1="{P + 60}" x2="{RX - 20}" y2="{P + 252}"/>')
o(f'<text class="sm b" x="{RX}" y="{P + 70}">Забули «7 −»: біт 5 замість 2</text>')
for row, (lit, cls, cap, ccls) in enumerate([(5, "val", "з «7 −»: світиться x = 13", "sm ok"),
                                             (2, "bad", "без: x = 10 — дзеркально у вісімці", "sm err")]):
    y = P + 80 + 58 * row
    for i in range(8):
        cell(RX + 28 * i, y, 28, 22, cls if i == lit else "zero", "#" if i == lit else "·", "sm mono b" if i == lit else "sm mono muted")
    o(f'<text class="{ccls}" x="{RX}" y="{y + 38}">{cap}</text>')
o(f'<text class="sm" x="{RX}" y="{P + 214}">Рядок 2 у дампі, з <tspan class="mono">0xA10</tspan>:</text>')
o(f'<text class="sm mono" x="{RX}" y="{P + 234}">00 <tspan class="ok">04</tspan> 00 00 00 00 00 00</text>')
o()

# ---------- Панель 4 ----------
Q = 612
o('<!-- 4. Рядки -->')
o(f'<rect class="box" x="24" y="{Q}" width="508" height="224" rx="10"/>')
o(f'<text class="h2" x="44" y="{Q + 26}">4. Рядок: довжина за домовленістю</text>')
chip(492, Q + 12, "§3")
def cstr(y, code, chars, codes, beyond, label, lcls, stop):
    o(f'<text class="sm mono" x="44" y="{y}">{code}</text>')
    cy = y + 10
    for i, (ch, cd) in enumerate(zip(chars, codes)):
        cls = "zero" if cd == "0" else "val"
        x = 64 + 48 * i
        o(f'<rect class="{cls}" x="{x}" y="{cy}" width="48" height="40"/>')
        o(f'<text class="mono b" x="{x + 24}" y="{cy + 18}" text-anchor="middle">{ch}</text>')
        o(f'<text class="xs mono muted" x="{x + 24}" y="{cy + 33}" text-anchor="middle">{cd}</text>')
    if beyond:
        x = 64 + 48 * 4
        o(f'<rect class="bad" x="{x}" y="{cy}" width="48" height="40"/>')
        o(f'<text class="mono err" x="{x + 24}" y="{cy + 25}" text-anchor="middle">?</text>')
    ex = 64 + 48 * stop + 24
    o(f'<path class="arrow {"a-bad" if beyond else "a-io"}" d="M70,{cy + 50} L{ex},{cy + 50}" marker-end="url(#{"m-bad" if beyond else "m-io"})"/>')
    if not beyond:
        o(f'<text class="xs muted" x="{ex + 10}" y="{cy + 54}">strlen іде до першого 0</text>')
    o(f'<text class="{lcls}" x="{64 + 48 * 5 + 12}" y="{cy + 18}">{label[0]}</text>')
    o(f'<text class="sm" x="{64 + 48 * 5 + 12}" y="{cy + 36}">{label[1]}</text>')
cstr(Q + 52, 'char s[4] = "HI";', ["H", "I", "\\0", "\\0"], ["72", "73", "0", "0"], False,
     ("strlen(s) = 2", "sizeof(s) = 4 — буфер"), "sm mono ok", 2)
cstr(Q + 136, '"ABCD" у char s[4]', ["A", "B", "C", "D"], ["65", "66", "67", "68"], True,
     ("нуля немає", "strlen іде за край — ASan"), "sm err", 4.6)
o()

# ---------- Панель 5 ----------
o('<!-- 5. Бульбашка -->')
o(f'<rect class="box" x="548" y="{Q}" width="508" height="224" rx="10"/>')
o(f'<text class="h2" x="568" y="{Q + 26}">5. Бульбашка: міняємо сусідів</text>')
chip(1016, Q + 12, "§4")
steps = [
    ("прохід 1", [4, 1, 3, 2], 0, [1, 4, 3, 2], 0),
    ("", [1, 4, 3, 2], 1, [1, 3, 4, 2], 0),
    ("", [1, 3, 4, 2], 2, [1, 3, 2, 4], 1),
    ("прохід 2", [1, 3, 2, 4], 0, None, 1),
    ("", [1, 3, 2, 4], 1, [1, 2, 3, 4], 2),
    ("прохід 3", [1, 2, 3, 4], 0, None, 4),
]
done_before = 0
for k, (lab, st, i, after, done_after) in enumerate(steps):
    y = Q + 42 + 25 * k
    if lab:
        o(f'<text class="sm b" x="568" y="{y + 15}">{lab}</text>')
    for j, v in enumerate(st):
        cls = "val" if j >= 4 - done_before else "zero"
        if j in (i, i + 1):
            cls += " hit"
        cell(650 + 30 * j, y, 30, 21, cls, str(v), "sm mono b" if j in (i, i + 1) else "sm mono")
    if after:
        o(f'<text class="sm b" x="784" y="{y + 15}">обмін →</text>')
        for j, v in enumerate(after):
            cls = "val" if j >= 4 - done_after else "zero"
            cell(850 + 30 * j, y, 30, 21, cls, str(v), "sm mono")
    else:
        o(f'<text class="sm muted" x="784" y="{y + 15}">без обміну</text>')
    done_before = done_after
o(f'<text class="sm" x="568" y="{Q + 210}">6 порівнянь, 4 обміни. Після проходу найбільше з решти — на місці.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
