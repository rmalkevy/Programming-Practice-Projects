#!/usr/bin/env python3
"""Generate img/bits.uk.svg for Lab 02 (bitwise operators, masks)."""
import sys

W, H = 1080, 1120
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def bitrow(x0, y, cw, ch, bits, cls=None, hit=None):
    """bits: string of 0/1. cls: None (by value) or list of classes per bit."""
    for i, b in enumerate(bits):
        x = x0 + cw * i
        c = cls[i] if cls else ("one" if b == "1" else "zero")
        if hit is not None and i == hit:
            c += " hit"
        o(f'<rect class="{c}" x="{x}" y="{y}" width="{cw}" height="{ch}"/>')
        t = "mono b" if b == "1" else "mono muted"
        o(f'<text class="{t}" x="{x + cw / 2:g}" y="{y + ch / 2 + 5:g}" text-anchor="middle">{b}</text>')

def bracket(x1, x2, y):
    o(f'<path class="brace" d="M{x1},{y} v6 H{x2} v-6"/>')

STYLE = """  <style>
    svg { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --box:#f6f8fa; --chip:#e7ecf0;
          --one:#dafbe1; --one-s:#1a7f37; --code:#ddf4ff; --code-s:#0969da; --ptr:#fbefff; --ptr-s:#8250df;
          --heap:#fff1e5; --heap-s:#bc4c00; --pad:#f6f8fa; --pad-s:#818b98; --bad:#ffebe9; --bad-s:#cf222e; }
    @media (prefers-color-scheme: dark) {
      svg { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#3d444d; --box:#151b23; --chip:#262c36;
            --one:#0f2d1a; --one-s:#3fb950; --code:#0d2c4f; --code-s:#4493f8; --ptr:#271b45; --ptr-s:#ab7df8;
            --heap:#3a2111; --heap-s:#f0883e; --pad:#151b23; --pad-s:#9198a1; --bad:#3d1418; --bad-s:#f85149; }
    }
    text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; fill: var(--fg); font-size: 13px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
    .h1 { font-size: 22px; font-weight: 700; }
    .h2 { font-size: 15px; font-weight: 700; }
    .big { font-size: 20px; font-weight: 700; }
    .b { font-weight: 700; }
    .sm { font-size: 11.5px; }
    .xs { font-size: 10.5px; }
    .muted { fill: var(--muted); }
    .ok { fill: var(--one-s); font-weight: 700; }
    .err { fill: var(--bad-s); font-weight: 700; }
    .chip rect { fill: var(--chip); }
    .chip text { font-size: 10.5px; font-weight: 700; fill: var(--muted); text-anchor: middle; }
    .bg { fill: var(--bg); }
    .box { fill: var(--box); stroke: var(--line); stroke-width: 1.5; }
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .one { fill: var(--one); stroke: var(--one-s); stroke-width: 1.2; }
    .zero { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .f-op { fill: var(--code); stroke: var(--code-s); stroke-width: 1.2; }
    .f-dst { fill: var(--ptr); stroke: var(--ptr-s); stroke-width: 1.2; }
    .f-src { fill: var(--heap); stroke: var(--heap-s); stroke-width: 1.2; }
    .hit { stroke: var(--fg); stroke-width: 2.5; }
    .flag { fill: var(--bad); stroke: var(--bad-s); stroke-width: 2; }
    .trap { fill: var(--bad); stroke: var(--bad-s); stroke-width: 1.2; }
    .band { fill: none; stroke: var(--muted); stroke-width: 1.5; stroke-dasharray: 4 3; }
    .brace { fill: none; stroke: var(--muted); stroke-width: 1.2; }
    .arrow { fill: none; stroke-width: 2; }
    .thin { fill: none; stroke: var(--muted); stroke-width: 1.3; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
    .dashed { stroke-dasharray: 4 3; }
  </style>"""

def marker(name, size):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Біти, оператори й маски</title>')
o('  <desc id="desc">Чотири панелі до теорії Lab 02. 1: байт 0x2F як вісім бітів із вагами 128…1, дві шістнадцяткові цифри по чотири біти, десяткове 47. 2: −5 у доповняльному коді: 5, інвертувати, додати 1 — 0xFB; той самий байт як uint8_t — 251, як int8_t — −5, бо біт 7 важить −128. 3: a = 0xCA і b = 0xA6 біт за бітом через &amp;, |, ^, ~; зсуви a &lt;&lt; 1 і a &gt;&gt; 1, біт, що виїхав, потрапляє в прапорець C; пастка пріоритету x &amp; 1 == 0. 4: байт 0b1011\'10\'01 розбирається на поля opcode, dest, src зсувом і маскою; виставити, скинути й перевірити біт прапорця; старший півбайт опкода ember — група.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 5)
marker("m-bad", 6)
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Біти: <tspan class="mono">&amp; | ^ ~ &lt;&lt; &gt;&gt;</tspan> і маски</text>')
o('<text class="muted" x="24" y="60">Байт — це вісім бітів. Бітовий оператор працює з кожним бітом окремо.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 02</text>')
o('<rect class="one" x="924" y="26" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="37">біт = 1</text>')
o('<rect class="zero" x="702" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="736" y="59">біт = 0</text>')
o('<rect class="pad" x="924" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="59">нуль, що зайшов</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Один байт, три записи -->')
o('<rect class="box" x="24" y="84" width="508" height="246" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Один байт — три записи</text>')
chip(492, 96, "§1")
X0, CW = 64, 36
for i in range(8):
    cx = X0 + CW * i + CW // 2
    o(f'<text class="xs mono muted" x="{cx}" y="138" text-anchor="middle">{7 - i}</text>')
    o(f'<text class="xs mono" x="{cx}" y="156" text-anchor="middle">{2 ** (7 - i)}</text>')
o('<text class="sm muted" x="362" y="138">номер біта</text>')
o('<text class="sm muted" x="362" y="156">вага</text>')
bitrow(X0, 164, CW, 34, "00101111")
o('<text class="sm muted" x="362" y="186">старший ліворуч</text>')
bracket(66, 206, 204); bracket(210, 350, 204)
o('<text class="big mono" x="136" y="232" text-anchor="middle">2</text>')
o('<text class="big mono" x="280" y="232" text-anchor="middle">F</text>')
o('<text class="sm muted" x="362" y="226">4 біти = 1 цифра</text>')
o('<text class="mono b" x="44" y="268">0b0010\'1111</text><text class="sm muted" x="160" y="268">двійковий: самі біти</text>')
o('<text class="mono b" x="44" y="290">0x2F</text><text class="sm muted" x="160" y="290">шістнадцятковий: <tspan class="mono">2·16 + 15</tspan></text>')
o('<text class="mono b" x="44" y="312">47</text><text class="sm muted" x="160" y="312">десятковий: <tspan class="mono">32 + 8 + 4 + 2 + 1</tspan> — ваги одиниць</text>')
o()

# ---------- Панель 2 ----------
o('<!-- 2. Доповняльний код -->')
o('<rect class="box" x="548" y="84" width="508" height="246" rx="10"/>')
o('<text class="h2" x="568" y="110">2. Доповняльний код: як записати −5</text>')
chip(1016, 96, "§2")
X0, CW = 660, 28
rows = [("5", "00000101", "п'ять", "sm muted"), ("~5", "11111010", "перевернути кожен біт", "sm muted"),
        ("~5 + 1", "11111011", "= −5, байт 0xFB", "sm ok")]
for k, (lab, bits, note, ncls) in enumerate(rows):
    y = 124 + 32 * k
    o(f'<text class="mono b" x="568" y="{y + 18}">{lab}</text>')
    bitrow(X0, y, CW, 26, bits)
    o(f'<text class="{ncls}" x="896" y="{y + 18}">{note}</text>')
o('<text class="sm" x="568" y="242">Той самий байт <tspan class="mono">0xFB</tspan> — дві розповіді. Різниця лише у вазі біта 7:</text>')
fb = "11111011"
for k, (lab, w7, total, tcls) in enumerate([("uint8_t", "128", "= 251", "sm mono b"), ("int8_t", "−128", "= −5", "sm mono ok")]):
    y = 266 + 22 * k
    o(f'<text class="sm mono b" x="568" y="{y}">{lab}</text>')
    for i, b in enumerate(fb):
        cx = X0 + CW * i + CW // 2
        w = (w7 if i == 0 else str(2 ** (7 - i))) if b == "1" else "·"
        c = "xs mono err" if (i == 0 and k == 1) else "xs mono"
        o(f'<text class="{c}" x="{cx}" y="{y}" text-anchor="middle">{w}</text>')
    o(f'<text class="{tcls}" x="896" y="{y}">{total}</text>')
o('<text class="sm muted" x="568" y="314">Так само <tspan class="mono">0xFF</tspan>: як <tspan class="mono">uint8_t</tspan> — 255, як <tspan class="mono">int8_t</tspan> — −1.</text>')
o()

# ---------- Панель 3 ----------
o('<!-- 3. Шість операторів -->')
o('<rect class="box" x="24" y="346" width="1032" height="378" rx="10"/>')
o('<text class="h2" x="44" y="372">3. Шість операторів: кожен біт окремо</text>')
chip(1016, 358, "§3")
X0, CW = 150, 30
a, b = "11001010", "10100110"
ops = [
    ("a", a, "0xCA", ""),
    ("b", b, "0xA6", ""),
    None,
    ("a &amp; b", "10000010", "0x82", "1, лише коли обидва 1 → <tspan class=\"b\">маска</tspan>"),
    ("a | b", "11101110", "0xEE", "1, якщо хоч один 1 → <tspan class=\"b\">виставити</tspan>"),
    ("a ^ b", "01101100", "0x6C", "1, якщо різні → <tspan class=\"b\">перемкнути</tspan>"),
    ("~a", "00110101", "0x35", "перевернути кожен біт"),
]
o(f'<rect class="band" x="{X0 + CW - 4}" y="380" width="{CW + 8}" height="222" rx="4"/>')
y = 386
for row in ops:
    if row is None:
        o(f'<line class="rule" x1="44" y1="{y + 4}" x2="690" y2="{y + 4}"/>')
        y += 12
        continue
    lab, bits, hx, rule = row
    o(f'<text class="mono b" x="44" y="{y + 19}">{lab}</text>')
    bitrow(X0, y, CW, 28, bits)
    o(f'<text class="mono" x="404" y="{y + 19}">{hx}</text>')
    if rule:
        o(f'<text class="sm" x="456" y="{y + 19}">{rule}</text>')
    y += 34
o(f'<text class="sm muted" x="44" y="622">Стовпчик рахується без сусідів. Біт 6: <tspan class="mono">a = 1</tspan>, <tspan class="mono">b = 0</tspan> → <tspan class="mono">&amp;</tspan> дає 0, <tspan class="mono">|</tspan> і <tspan class="mono">^</tspan> дають 1.</text>')

# зсуви
o('<line class="rule" x1="706" y1="384" x2="706" y2="630"/>')
SX, SW = 772, 28
def shift(title, note, y_src, y_res, src, res, left):
    o(f'<text x="720" y="{y_src - 10}"><tspan class="mono b">{title}</tspan><tspan class="sm muted">  {note}</tspan></text>')
    bitrow(SX, y_src, SW, 28, src)
    cls = ["one" if c == "1" else "zero" for c in res]
    enter = 7 if left else 0
    cls[enter] = "pad"
    bitrow(SX, y_res, SW, 28, res, cls)
    cbit = src[0] if left else src[7]
    cx = 720 if left else SX + SW * 8 + 10
    o(f'<rect class="flag" x="{cx}" y="{y_res}" width="{SW + 8}" height="28" rx="4"/>')
    o(f'<text class="mono b" x="{cx + (SW + 8) / 2:g}" y="{y_res + 19}" text-anchor="middle">{cbit}</text>')
    o(f'<text class="sm b" x="{cx + (SW + 8) / 2:g}" y="{y_res + 44}" text-anchor="middle">C</text>')
    for i in range(8):
        sx = SX + SW * i + SW / 2
        j = i - 1 if left else i + 1
        if 0 <= j < 8:
            dx = SX + SW * j + SW / 2
        else:
            dx = cx + (SW + 8) / 2
        o(f'<path class="thin" d="M{sx:g},{y_src + 30} L{dx:g},{y_res - 2}" marker-end="url(#m-io)"/>')
    ex = SX + SW * enter + SW / 2
    if left:
        o(f'<text class="xs muted" x="{ex + 18:g}" y="{y_res + 44}" text-anchor="end">заходить 0</text>')
    else:
        o(f'<text class="xs muted" x="{ex - 14:g}" y="{y_res + 44}">заходить 0</text>')

shift("a &lt;&lt; 1", "SHL A: біт 7 виїжджає в C", 398, 458, a, "10010100", True)
shift("a &gt;&gt; 1", "SHR A: біт 0 виїжджає в C", 530, 590, a, "01100101", False)
o('<text class="sm muted" x="720" y="652">Для беззнакових: <tspan class="mono">x &lt;&lt; n</tspan> = <tspan class="mono">x · 2ⁿ</tspan>, <tspan class="mono">x &gt;&gt; n</tspan> = <tspan class="mono">x / 2ⁿ</tspan></text>')

# пастка
o('<rect class="trap" x="44" y="664" width="992" height="48" rx="6"/>')
o('<text class="sm" x="58" y="684"><tspan class="b">Пріоритет:</tspan> <tspan class="mono">x &amp; 1 == 0</tspan> читається як <tspan class="mono">x &amp; (1 == 0)</tspan> = <tspan class="mono">x &amp; 0</tspan> = 0 — завжди хибне. Пишіть <tspan class="mono b">(x &amp; 1) == 0</tspan>.</text>')
o('<text class="sm" x="58" y="702"><tspan class="b">Ширина:</tspan> <tspan class="mono">1 &lt;&lt; 31</tspan> для <tspan class="mono">int</tspan> заїжджає в знаковий біт, <tspan class="mono">1 &lt;&lt; 32</tspan> — UB. Для бітів беріть беззнакове: <tspan class="mono b">1u &lt;&lt; n</tspan>.</text>')
o()

# ---------- Панель 4 ----------
o('<!-- 4. Зсув і маска -->')
o('<rect class="box" x="24" y="740" width="1032" height="364" rx="10"/>')
o('<text class="h2" x="44" y="766">4. Зсув і маска: розібрати байт на поля</text>')
chip(982, 752, "§4"); chip(1016, 752, "§5")
o('<text class="sm mono" x="44" y="790">std::uint8_t ins = 0b1011\'10\'01;   // 0xB9 = opcode:4 | dest:2 | src:2</text>')

C1, C2, C3, CW = 190, 470, 750, 22
o(f'<text class="sm muted" x="{C1}" y="814">ins</text>')
o(f'<text class="sm muted" x="{C2}" y="814">1. зсунути поле до біта 0</text>')
o(f'<text class="sm muted" x="{C3}" y="814">2. маска: лишити тільки поле</text>')
o('<text class="sm muted" x="942" y="814">поле</text>')
ins = "10111001"
icls = ["f-op"] * 4 + ["f-dst"] * 2 + ["f-src"] * 2
fields = [
    ("opcode", "f-op", 4, "0x0F", 4, "0b1011 = 11"),
    ("dest", "f-dst", 2, "0x03", 2, "0b10 = 2"),
    ("src", "f-src", 0, "0x03", 2, "0b01 = 1"),
]
for k, (name, fcls, sh, mask, width, res) in enumerate(fields):
    y = 824 + 40 * k
    o(f'<rect class="{fcls}" x="44" y="{y + 6}" width="14" height="14" rx="2"/>')
    o(f'<text class="mono b" x="66" y="{y + 18}">{name}</text>')
    bitrow(C1, y, CW, 26, ins, icls)
    shifted = "0" * sh + ins[:8 - sh]
    scls = ["pad"] * sh + icls[:8 - sh]
    bitrow(C2, y, CW, 26, shifted, scls)
    masked = "0" * (8 - width) + shifted[8 - width:]
    mcls = ["pad"] * (8 - width) + [fcls] * width
    bitrow(C3, y, CW, 26, masked, mcls)
    op1 = f"&gt;&gt; {sh}" if sh else "без зсуву"
    o(f'<path class="arrow a-io" d="M{C1 + 8 * CW + 8},{y + 13} L{C2 - 8},{y + 13}" marker-end="url(#m-io)"/>')
    o(f'<text class="sm mono b" x="{(C1 + 8 * CW + C2) / 2:g}" y="{y + 8}" text-anchor="middle">{op1}</text>')
    o(f'<path class="arrow a-io" d="M{C2 + 8 * CW + 8},{y + 13} L{C3 - 8},{y + 13}" marker-end="url(#m-io)"/>')
    o(f'<text class="sm mono b" x="{(C2 + 8 * CW + C3) / 2:g}" y="{y + 8}" text-anchor="middle">&amp; {mask}</text>')
    o(f'<text class="mono b" x="942" y="{y + 18}">{res}</text>')
o('<text class="sm mono" x="44" y="962">opcode = (ins &gt;&gt; 4) &amp; 0x0F;   dest = (ins &gt;&gt; 2) &amp; 0x03;   src = ins &amp; 0x03;</text>')
o('<line class="rule" x1="44" y1="976" x2="1036" y2="976"/>')

# прапорці
o('<text class="sm b" x="44" y="998">Біт прапорця: виставити, скинути, перевірити</text>')
FX = 190
flag_rows = [
    ("flags", "00000101", None, "", "sm muted"),
    ("flags | (1u &lt;&lt; 3)", "00001101", 4, "виставити біт 3", "sm"),
    ("flags &amp; ~(1u &lt;&lt; 0)", "00000100", 7, "скинути біт 0", "sm"),
    ("flags &amp; (1u &lt;&lt; 2)", "00000100", 5, "≠ 0 → біт 2 є", "sm ok"),
]
for k, (lab, bits, hit, note, ncls) in enumerate(flag_rows):
    y = 1008 + 22 * k
    o(f'<text class="sm mono" x="44" y="{y + 15}">{lab}</text>')
    bitrow(FX, y, 22, 20, bits, hit=hit)
    o(f'<text class="{ncls}" x="{FX + 8 * 22 + 12}" y="{y + 15}">{note}</text>')

# ember
o('<line class="rule" x1="580" y1="988" x2="580" y2="1092"/>')
o('<text class="sm b" x="600" y="998">У <tspan class="mono">ember</tspan>: старший півбайт опкода — група</text>')
o('<text class="sm mono b" x="600" y="1026">0x16</text>')
bitrow(648, 1010, 26, 24, "00010110", ["f-op"] * 4 + ["zero"] * 4)
o('<text class="sm mono" x="866" y="1026">SHL A</text>')
o('<text class="sm" x="600" y="1056"><tspan class="mono">(op &gt;&gt; 4) &amp; 0x0F</tspan> = 1 → група <tspan class="mono">0x1_</tspan>, ALU</text>')
o('<text class="sm muted" x="600" y="1076"><tspan class="mono">0x10 ADD</tspan> · <tspan class="mono">0x11 SUB</tspan> · … · <tspan class="mono">0x16 SHL A</tspan> · <tspan class="mono">0x17 SHR A</tspan></text>')
o('<text class="sm muted" x="600" y="1094">Яка саме інструкція — каже весь байт, за таблицею з ISA.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
