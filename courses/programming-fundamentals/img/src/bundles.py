#!/usr/bin/env python3
"""Generate img/bundles.uk.svg for Lab 06 (struct layout, enum class, lifetimes, heap bugs, ember heap)."""
import sys

W, H = 1080, 910
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def cell(x, y, w, h, cls, text="", tcls="mono"):
    o(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
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
    .cell { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .rule { stroke: var(--line); stroke-width: 1.2; }
    .guide { stroke: var(--line); stroke-width: 1; stroke-dasharray: 3 3; }
    .fa { fill: var(--a); stroke: var(--a-s); stroke-width: 1.2; }
    .fb { fill: var(--b); stroke: var(--b-s); stroke-width: 1.2; }
    .fc { fill: var(--c); stroke: var(--c-s); stroke-width: 1.2; }
    .ra { fill: var(--a); stroke: var(--a-s); stroke-width: 1.5; }
    .rb { fill: var(--b); stroke: var(--b-s); stroke-width: 1.5; }
    .rc { fill: var(--c); stroke: var(--c-s); stroke-width: 1.5; }
    .zero { fill: var(--bg); stroke: var(--line); stroke-width: 1.2; }
    .pad { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .bad { fill: var(--bad); stroke: var(--bad-s); stroke-width: 1.5; stroke-dasharray: 4 3; }
    .ptr { fill: var(--b); stroke: var(--b-s); stroke-width: 2; }
    .brace { fill: none; stroke: var(--muted); stroke-width: 1.2; }
    .x-bad { stroke: var(--bad-s); stroke-width: 2.5; stroke-linecap: round; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-b { stroke: var(--b-s); }      .m-b { fill: var(--b-s); }
    .a-bad { stroke: var(--bad-s); }  .m-bad { fill: var(--bad-s); }
    .a-val { stroke: var(--val-s); }  .m-val { fill: var(--val-s); }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

def bracket(x1, x2, y):
    o(f'<path class="brace" d="M{x1},{y} v6 H{x2} v-6"/>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Структури, час життя і купа</title>')
o('  <desc id="desc">П\'ять панелей до теорії Lab 06. 1: struct P { char c; int n; } займає 8 байтів, хоча полів 5: між c і n три вирівнювальні байти; ті самі поля op, addr, imm у трьох порядках займають 6, 4 і 4 байти. 2: enum class Op: байт 0x18 стає Op::Inc лише через приведення. 3: три часи життя — статична пам\'ять, стек і купа, з адресами з практики і шкалою часу. 4: завислий вказівник — вказівник без об\'єкта, витік — об\'єкт без вказівника. 5: купа ember: ALLOC видає блоки 0x0C00 на 4 байти і 0x0C04 на 2, вершина купи 0x0C06, FREE немає.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-b"); marker("m-bad"); marker("m-val")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок і легенда ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Структури, час життя і купа</text>')
o('<text class="muted" x="24" y="60">Поля лежать поруч — з дірками для вирівнювання. Де лежить сама змінна, вирішує її час життя.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 06</text>')
o('<rect class="pad" x="924" y="26" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="954" y="37">нічиї байти</text>')
o('<rect class="bad" x="702" y="48" width="22" height="14" rx="2"/>')
o('<text class="sm muted" x="736" y="59">звільнена пам\'ять</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. struct -->')
o('<rect class="box" x="24" y="84" width="640" height="290" rx="10"/>')
o('<text class="h2" x="44" y="110">1. <tspan class="mono">struct</tspan> — поля поруч, у яких є імена</text>')
chip(624, 96, "§1")
o('<text class="sm mono" x="44" y="134">struct P { char c; int n; };   P p{\'A\', 300};</text>')
X0, CW = 44, 52
bytes_ = ["41", "EE", "EE", "EE", "2C", "01", "00", "00"]
cls = ["fa"] + ["pad"] * 3 + ["fb"] * 4
own = ["c", "··", "··", "··", "n", "n", "n", "n"]
for i in range(8):
    cx = X0 + CW * i + CW // 2
    o(f'<text class="xs mono muted" x="{cx}" y="158" text-anchor="middle">{i}</text>')
    cell(X0 + CW * i, 164, CW, 36, cls[i], bytes_[i], "mono muted" if cls[i] == "pad" else "mono b")
    o(f'<text class="xs mono{" muted" if own[i] == "··" else " b"}" x="{cx}" y="216" text-anchor="middle">{own[i]}</text>')
o('<text class="xs muted" x="468" y="158">зміщення</text>')
o('<text class="mono b" x="476" y="178">sizeof(P) = 8</text>')
o('<text class="sm" x="476" y="196">а полів — 1 + 4 = 5</text>')
o('<text class="sm muted" x="476" y="216"><tspan class="mono">int</tspan> стає на зміщення,</text>')
o('<text class="sm muted" x="476" y="232">кратне 4: <tspan class="mono">alignof(int)</tspan></text>')
o('<text class="sm muted" x="44" y="240">Вирівнювальні байти нічиї: у дампі там досі те, що лежало (<tspan class="mono">EE</tspan>).</text>')
o('<text class="sm b" x="44" y="264">Порядок полів змінює розмір:</text>')
layouts = [
    ("{ Byte op; uint16_t addr; Byte imm; }", ["op", "··", "addr", "addr", "imm", "··"], "= 6"),
    ("{ uint16_t addr; Byte op; Byte imm; }", ["addr", "addr", "op", "imm"], "= 4"),
    ("{ Byte op; Byte imm; uint16_t addr; }", ["op", "imm", "addr", "addr"], "= 4"),
]
fcls = {"op": "fa", "addr": "fb", "imm": "fc", "··": "pad"}
for k, (code, cells_, size) in enumerate(layouts):
    y = 274 + 26 * k
    o(f'<text class="xs mono" x="44" y="{y + 15}">{code}</text>')
    for i, f in enumerate(cells_):
        cell(296 + 40 * i, y, 40, 22, fcls[f], f, "xs mono muted" if f == "··" else "xs mono")
    o(f'<text class="mono b" x="{296 + 40 * 6 + 12}" y="{y + 16}">{size}</text>')
o('<text class="sm muted" x="44" y="366">Масив із 8 таких записів: 48 проти 32 байтів.</text>')
o()

# ---------- Панель 2 ----------
o('<!-- 2. enum class -->')
o('<rect class="box" x="680" y="84" width="376" height="290" rx="10"/>')
o('<text class="h2" x="700" y="110">2. <tspan class="mono">enum class</tspan> — цілі з типом</text>')
chip(1016, 96, "§2")
o('<text class="xs mono" x="700" y="134">enum class Op : std::uint8_t {</text>')
o('<text class="xs mono" x="700" y="150" style="white-space:pre">    Add = 0x10, Inc = 0x18, …</text>')
o('<text class="xs mono" x="700" y="166">};</text>')
o('<rect class="zero" x="700" y="186" width="104" height="32" rx="4"/>')
o('<text class="mono" x="752" y="207" text-anchor="middle">Byte 0x18</text>')
o('<path class="arrow a-io" d="M806,202 L880,202" marker-end="url(#m-io)"/>')
o('<text class="xs mono b" x="843" y="196" text-anchor="middle">(Op)b</text>')
o('<rect class="ra" x="884" y="186" width="150" height="32" rx="4"/>')
o('<text class="mono b" x="959" y="207" text-anchor="middle">Op::Inc</text>')
o('<text class="xs muted" x="700" y="234">сирий байт</text><text class="xs muted" x="884" y="234">розібраний опкод</text>')
o('<text class="sm" x="700" y="262"><tspan class="ok">✓</tspan> <tspan class="mono xs">switch (op) { case Op::Inc: … }</tspan></text>')
o('<text class="sm" x="700" y="282"><tspan class="err">✗</tspan> <tspan class="mono xs">Op op = 0x18;</tspan> <tspan class="xs muted">— не збирається</tspan></text>')
o('<text class="sm" x="700" y="302"><tspan class="err">✗</tspan> <tspan class="mono xs">Op::Add + 1</tspan> <tspan class="xs muted">— не збирається</tspan></text>')
o('<text class="sm" x="700" y="330"><tspan class="mono">(Op)0x77</tspan> нічого не перевіряє:</text>')
o('<text class="sm" x="700" y="348">невідомий байт ловить <tspan class="mono">default:</tspan> —</text>')
o('<text class="sm" x="700" y="366">це помилка, а не тихий <tspan class="mono">Nop</tspan>.</text>')
o()

# ---------- Панель 3 ----------
P = 390
o('<!-- 3. Три часи життя -->')
o(f'<rect class="box" x="24" y="{P}" width="1032" height="260" rx="10"/>')
o(f'<text class="h2" x="44" y="{P + 26}">3. Три часи життя: де живе змінна і як довго</text>')
chip(1016, P + 12, "§3")
o(f'<text class="sm muted" x="44" y="{P + 46}">Адреси — з <tspan class="mono">./run.sh 05 3</tspan> у практиці Lab 06. У вас будуть інші, але три ділянки так само далеко одна від одної.</text>')
kinds = [
    ("ra", "Статична / глобальна", "global_counter  0x102737f40", "ember: Memory, якщо глобальний (не робіть)"),
    ("rb", "Автоматична (стек)", "in_main 0x16d6ea380 · dive(1) …9fe0 · dive(2) …9d80 · dive(3) …9b20", "ember: CPU cpu у main"),
    ("rc", "Динамічна (купа)", "new int 0x6020000000b0 · …0f0 · …130", "ember: купа гостя 0xC00–0xEFF"),
]
TX = {"старт": 566, "{": 700, "new": 760, "}": 860, "delete": 940, "кінець": 1018}
for name, x in TX.items():
    o(f'<line class="guide" x1="{x}" y1="{P + 58}" x2="{x}" y2="{P + 232}"/>')
    o(f'<text class="xs mono muted" x="{x}" y="{P + 248}" text-anchor="middle">{name}</text>')
bars = [(566, 1018, "увесь час роботи"), (700, 860, "до виходу з блока"), (760, 940, "до delete — блок уже скінчився")]
for k, (cls_, title, addrs, ember) in enumerate(kinds):
    y = P + 60 + 58 * k
    o(f'<rect class="{cls_}" x="44" y="{y}" width="480" height="50" rx="6"/>')
    o(f'<text class="sm b" x="56" y="{y + 19}">{title}</text>')
    o(f'<text class="xs muted" x="512" y="{y + 19}" text-anchor="end">{ember}</text>')
    o(f'<text class="xs mono" x="56" y="{y + 38}">{addrs}</text>')
    x1, x2, lab = bars[k]
    o(f'<rect class="{cls_}" x="{x1}" y="{y + 16}" width="{x2 - x1}" height="18" rx="4"/>')
    lx = x1 + 6
    o(f'<text class="xs" x="{lx}" y="{y + 29}">{lab}</text>')
o()

# ---------- Панель 4 ----------
Q = 666
o('<!-- 4. Завислий вказівник і витік -->')
o(f'<rect class="box" x="24" y="{Q}" width="576" height="228" rx="10"/>')
o(f'<text class="h2" x="44" y="{Q + 26}">4. Завислий вказівник і витік — протилежні</text>')
chip(560, Q + 12, "§3")
o(f'<line class="rule" x1="310" y1="{Q + 40}" x2="310" y2="{Q + 216}"/>')
# A: вказівник без об'єкта
o(f'<text class="sm b" x="44" y="{Q + 50}">Вказівник без об\'єкта</text>')
o(f'<text class="xs mono" x="44" y="{Q + 66}">int* p = new int{{42}};</text>')
o(f'<text class="xs mono" x="44" y="{Q + 80}">delete p;</text>')
o(f'<rect class="ptr" x="44" y="{Q + 92}" width="160" height="30" rx="6"/>')
o(f'<text class="mono b" x="56" y="{Q + 112}">p</text><text class="sm mono" x="80" y="{Q + 112}">0x6020000000b0</text>')
o(f'<path class="arrow a-b" d="M124,{Q + 124} L124,{Q + 148}" marker-end="url(#m-b)"/>')
o(f'<rect class="bad" x="64" y="{Q + 150}" width="120" height="30" rx="4"/>')
o(f'<text class="mono err" x="124" y="{Q + 170}" text-anchor="middle">42?</text>')
o(f'<text class="xs muted" x="192" y="{Q + 170}">звільнено</text>')
o(f'<text class="xs mono err" x="44" y="{Q + 198}">*p → heap-use-after-free</text>')
o(f'<text class="xs mono err" x="44" y="{Q + 214}">delete p; знову → double-free</text>')
# B: об'єкт без вказівника
o(f'<text class="sm b" x="326" y="{Q + 50}">Об\'єкт без вказівника</text>')
o(f'<text class="xs mono" x="326" y="{Q + 66}">int* p = new int{{1}};</text>')
o(f'<text class="xs mono" x="326" y="{Q + 80}">p = new int{{2}};</text>')
o(f'<rect class="ptr" x="400" y="{Q + 92}" width="70" height="30" rx="6"/>')
o(f'<text class="mono b" x="435" y="{Q + 112}" text-anchor="middle">p</text>')
o(f'<rect class="rc" x="330" y="{Q + 150}" width="90" height="30" rx="4"/>')
o(f'<text class="mono b" x="375" y="{Q + 170}" text-anchor="middle">1</text>')
o(f'<rect class="rc" x="480" y="{Q + 150}" width="90" height="30" rx="4"/>')
o(f'<text class="mono b" x="525" y="{Q + 170}" text-anchor="middle">2</text>')
o(f'<path class="arrow a-io dashed" d="M420,{Q + 124} L385,{Q + 148}"/>')
o(f'<path class="x-bad" d="M396,{Q + 130} L408,{Q + 142} M408,{Q + 130} L396,{Q + 142}"/>')
o(f'<path class="arrow a-b" d="M455,{Q + 124} L510,{Q + 148}" marker-end="url(#m-b)"/>')
o(f'<text class="xs err" x="326" y="{Q + 198}">витік: на 1 уже ніхто не вказує</text>')
o(f'<text class="xs muted" x="326" y="{Q + 214}">LeakSanitizer — на Linux; macOS мовчить</text>')
o()

# ---------- Панель 5 ----------
o('<!-- 5. Купа ember -->')
o(f'<rect class="box" x="616" y="{Q}" width="440" height="228" rx="10"/>')
o(f'<text class="h2" x="636" y="{Q + 26}">5. Купа <tspan class="mono">ember</tspan>: <tspan class="mono">ALLOC</tspan> іде лише вперед</text>')
chip(1016, Q + 12, "ISA")
o(f'<text class="xs mono" x="636" y="{Q + 50}">LOADI A, 4 · ALLOC → H = 0x0C00, heap = 0x0C04</text>')
o(f'<text class="xs mono" x="636" y="{Q + 66}">LOADI A, 2 · ALLOC → H = 0x0C04, heap = 0x0C06</text>')
HX, HW, HY = 636, 50, Q + 96
hv = ["11", "00", "00", "00", "22", "00", "", ""]
hc = ["fa"] * 4 + ["fb"] * 2 + ["pad"] * 2
for i in range(8):
    cell(HX + HW * i, HY, HW, 32, hc[i], hv[i], "sm mono b")
    o(f'<text class="xs mono muted" x="{HX + HW * i + HW // 2}" y="{HY + 46}" text-anchor="middle">0C0{i}</text>')
for lab, i in [("H", 4), ("heap", 6)]:
    cx = HX + HW * i + HW // 2
    o(f'<text class="xs mono b" x="{cx}" y="{HY - 12}" text-anchor="middle">{lab}</text>')
    o(f'<path class="arrow a-io" d="M{cx},{HY - 9} L{cx},{HY - 2}" marker-end="url(#m-io)"/>')
bracket(HX + 2, HX + 4 * HW - 2, HY + 54); bracket(HX + 4 * HW + 2, HX + 6 * HW - 2, HY + 54); bracket(HX + 6 * HW + 2, HX + 8 * HW - 2, HY + 54)
o(f'<text class="xs" x="{HX + 2 * HW}" y="{HY + 74}" text-anchor="middle">перший блок, 4 байти</text>')
o(f'<text class="xs" x="{HX + 5 * HW}" y="{HY + 74}" text-anchor="middle">другий, 2</text>')
o(f'<text class="xs muted" x="{HX + 7 * HW}" y="{HY + 74}" text-anchor="middle">вільно до 0xEFF</text>')
o(f'<text class="sm" x="636" y="{Q + 198}"><tspan class="mono">FREE</tspan> немає: вершина купи тільки росте.</text>')
o(f'<text class="sm muted" x="636" y="{Q + 214}">Не влізло — <tspan class="mono">C = 1</tspan>, а <tspan class="mono">H</tspan> не змінюється.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
