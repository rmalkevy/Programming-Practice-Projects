#!/usr/bin/env python3
"""Generate img/language.uk.svg for Lab 08 (text to tokens, token list, two-pass assembler)."""
import sys

W, H = 1080, 756
out = []
def o(s=""): out.append(s)

def chip(x, y, label):
    o(f'<g class="chip" transform="translate({x},{y})"><rect width="28" height="17" rx="4"/><text x="14" y="12.5">{label}</text></g>')

def cell(x, y, w, h, cls, text="", tcls="mono", rx=0):
    o(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>')
    if text != "":
        o(f'<text class="{tcls}" x="{x + w / 2:g}" y="{y + h / 2 + 5:g}" text-anchor="middle" style="white-space:pre">{text}</text>')

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
    .letter { fill: var(--a); stroke: var(--a-s); stroke-width: 1.2; }
    .digit { fill: var(--val); stroke: var(--val-s); stroke-width: 1.2; }
    .punct { fill: var(--b); stroke: var(--b-s); stroke-width: 1.2; }
    .comment { fill: var(--c); stroke: var(--c-s); stroke-width: 1.2; }
    .space { fill: var(--pad); stroke: var(--pad-s); stroke-width: 1.2; stroke-dasharray: 4 3; }
    .nl { fill: var(--bg); stroke: var(--muted); stroke-width: 1.2; }
    .stage { fill: var(--bg); stroke: var(--muted); stroke-width: 1.5; }
    .node { fill: var(--a); stroke: var(--a-s); stroke-width: 1.5; }
    .nptr { fill: var(--b); stroke: var(--b-s); stroke-width: 1.5; }
    .brace { fill: none; stroke: var(--muted); stroke-width: 1.2; }
    .arrow { fill: none; stroke-width: 2; }
    .a-io { stroke: var(--muted); }   .m-io { fill: var(--muted); }
    .a-b { stroke: var(--b-s); }      .m-b { fill: var(--b-s); }
    .dashed { stroke-dasharray: 5 3; }
  </style>"""

def marker(name, size=7):
    o(f'    <marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path class="{name}" d="M0,0 L10,5 L0,10 z"/></marker>')

def bracket(x1, x2, y):
    o(f'<path class="brace" d="M{x1},{y} v6 H{x2} v-6"/>')

o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">')
o('  <title id="title">Від тексту до байтів</title>')
o('  <desc id="desc">Чотири панелі до теорії Lab 08. 1: конвеєр: файл .asm, лексер, список токенів, асемблер у два проходи, байти в Memory, CPU.run. 2: рядок LOADI A, 0x41 ; x — це байти, і курсор лексера класифікує кожен: літера, цифра, пунктуація, пробіл, коментар; рядок loop: JMP loop стає токенами Ident(loop) Colon Ident(JMP) Ident(loop) Newline Eof. 3: токени у зв\'язному списку з head, tail і next. 4: програма forward: за один прохід операнд JMP done лишається ?? ??, бо мітка нижче; прохід 1 рахує done = 0x0004, прохід 2 видає 30 04 00.</desc>')
o(STYLE)
o('  <defs>')
marker("m-io", 6); marker("m-b")
o('  </defs>')
o()
o(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>')
o()

# ---------- Заголовок ----------
o('<!-- Заголовок і легенда -->')
o('<text class="h1" x="24" y="38">Від тексту до байтів</text>')
o('<text class="muted" x="24" y="60">Текст програми — теж байти. Лексер робить із них токени, асемблер — байти коду.</text>')
chip(700, 24, "§1")
o('<text class="sm muted" x="736" y="37">— розділ Теорії Lab 08</text>')
o()

# ---------- Панель 1 ----------
o('<!-- 1. Конвеєр -->')
o('<rect class="box" x="24" y="84" width="1032" height="130" rx="10"/>')
o('<text class="h2" x="44" y="110">1. Від тексту до <tspan class="mono">run</tspan></text>')
chip(1016, 96, "§4")
stages = [(44, 150, "forward.asm", "текст, байти символів"), (224, 110, "лексер", "lex()"),
          (364, 150, "список токенів", "Token* head"), (544, 170, "асемблер", "прохід 1 · прохід 2"),
          (744, 150, "байти в Memory", "30 04 00 01 00"), (924, 112, "CPU.run", "step, step, …")]
for k, (x, w, t1, t2) in enumerate(stages):
    o(f'<rect class="stage" x="{x}" y="126" width="{w}" height="48" rx="6"/>')
    o(f'<text class="sm b{" mono" if k in (0, 5) else ""}" x="{x + w / 2:g}" y="146" text-anchor="middle">{t1}</text>')
    o(f'<text class="xs{" mono" if k in (1, 2, 4, 5) else ""} muted" x="{x + w / 2:g}" y="164" text-anchor="middle">{t2}</text>')
    if k < 5:
        nx = stages[k + 1][0]
        o(f'<path class="arrow a-io" d="M{x + w + 3},150 L{nx - 3},150" marker-end="url(#m-io)"/>')
o('<text class="sm muted" x="44" y="200"><tspan class="mono">./ember programs/hello.asm</tspan> збирає й виконує; просто <tspan class="mono">./ember</tspan> — REPL, як і раніше.</text>')
o()

# ---------- Панель 2 ----------
P = 230
o('<!-- 2. Символи і токени -->')
o(f'<rect class="box" x="24" y="{P}" width="1032" height="240" rx="10"/>')
o(f'<text class="h2" x="44" y="{P + 26}">2. Символи — це ще не токени</text>')
chip(982, P + 12, "§1"); chip(1016, P + 12, "§2")
o(f'<text class="sm" x="44" y="{P + 52}">Курсор <tspan class="mono">i</tspan> іде байтами рядка <tspan class="mono">LOADI A, 0x41 ; x</tspan> і на кожному вирішує, куди далі:</text>')
line_a = "LOADI A, 0x41 ; x"
def cls_a(i, ch):
    if i >= 14: return "comment"
    if ch == " ": return "space"
    if ch.isdigit(): return "digit"
    if ch.isalpha(): return "letter"
    return "punct"
CW = 30
for i, ch in enumerate(line_a + "\n"):
    x = 44 + CW * i
    if ch == "\n":
        cell(x, P + 62, CW, 30, "nl", "\\n", "xs mono")
    else:
        cell(x, P + 62, CW, 30, cls_a(i, ch), "␣" if ch == " " else ch, "mono muted" if ch == " " else "mono")
    o(f'<text class="xs mono muted" x="{x + CW // 2}" y="{P + 106}" text-anchor="middle">{ord(ch):02X}</text>')
leg = [("letter", "літера → ident()"), ("digit", "цифра → number()"), ("punct", ": , [ ] → свій токен"),
       ("space", "пробіл → пропустити"), ("comment", "; → коментар до кінця рядка"), ("nl", "\\n → Newline")]
for k, (c, t) in enumerate(leg):
    x, y = 620 + 210 * (k % 2), P + 66 + 20 * (k // 2)
    o(f'<rect class="{c}" x="{x}" y="{y}" width="16" height="12" rx="2"/>')
    o(f'<text class="xs" x="{x + 24}" y="{y + 10}">{t}</text>')

o(f'<text class="xs muted" x="44" y="{P + 122}">Окремо вирішується лише байт, з якого починається лексема: <tspan class="mono">0x41</tspan> цілком забере <tspan class="mono">number()</tspan>.</text>')
o(f'<text class="sm" x="44" y="{P + 140}">Лексема за лексемою — токени рядка <tspan class="mono">loop: JMP loop</tspan>:</text>')
line_b = "loop: JMP loop"
for i, ch in enumerate(line_b + "\n"):
    x = 44 + CW * i
    if ch == "\n":
        cell(x, P + 148, CW, 30, "nl", "\\n", "xs mono")
    elif ch == " ":
        cell(x, P + 148, CW, 30, "space", "␣", "mono muted")
    else:
        cell(x, P + 148, CW, 30, "punct" if ch == ":" else "letter", ch, "mono")
cell(44 + CW * 15 + 16, P + 148, 40, 30, "space", "EOF", "xs mono muted")
toks = [(0, 4, "Ident(loop)"), (4, 5, "Colon"), (6, 9, "Ident(JMP)"), (10, 14, "Ident(loop)"), (14, 15, "Newline")]
for a, b, t in toks:
    bracket(44 + CW * a + 2, 44 + CW * b - 2, P + 182)
    o(f'<text class="xs mono b" x="{44 + CW * (a + b) / 2:g}" y="{P + 202}" text-anchor="middle">{t}</text>')
o(f'<text class="xs mono b" x="{44 + CW * 15 + 36}" y="{P + 202}" text-anchor="middle">Eof</text>')
o(f'<line class="rule" x1="604" y1="{P + 132}" x2="604" y2="{P + 226}"/>')
o(f'<text class="sm b" x="620" y="{P + 146}">Граматика рядка</text>')
o(f'<text class="xs mono" x="620" y="{P + 164}">line := [ ident \':\' ] [ instruction ] [ comment ] newline</text>')
o(f'<text class="xs muted" x="620" y="{P + 182}"><tspan class="mono">loop:</tspan> — мітка, <tspan class="mono">JMP</tspan> — мнемоніка, <tspan class="mono">loop</tspan> — операнд-мітка</text>')
o(f'<text class="xs muted" x="620" y="{P + 204}">Вивід лексера, як у CHECKS.md:</text>')
o(f'<text class="xs mono" x="620" y="{P + 220}">Ident(loop) Colon Ident(JMP) Ident(loop) Newline Eof</text>')
o()

# ---------- Панель 3 ----------
Q = 486
o('<!-- 3. Список токенів -->')
o(f'<rect class="box" x="24" y="{Q}" width="508" height="254" rx="10"/>')
o(f'<text class="h2" x="44" y="{Q + 26}">3. Список: довжину не оголошують, а з\'ясовують</text>')
chip(492, Q + 12, "§3")
o(f'<text class="xs mono" x="44" y="{Q + 50}">Token* head = nullptr;  Token* tail = nullptr;</text>')
nodes = [(44, "Ident", "loop"), (154, "Colon", ""), (264, "Ident", "JMP"), (414, "Eof", "")]
NY = Q + 92
for k, (x, kind, txt) in enumerate(nodes):
    o(f'<rect class="node" x="{x}" y="{NY}" width="70" height="44" rx="4"/>')
    o(f'<text class="sm mono b" x="{x + 35}" y="{NY + 18}" text-anchor="middle">{kind}</text>')
    o(f'<text class="xs mono" x="{x + 35}" y="{NY + 34}" text-anchor="middle">{txt if txt else "·"}</text>')
    o(f'<rect class="nptr" x="{x + 70}" y="{NY}" width="20" height="44" rx="4"/>')
    if k < 2:
        o(f'<circle cx="{x + 80}" cy="{NY + 22}" r="3" fill="var(--b-s)"/>')
        o(f'<path class="arrow a-b" d="M{x + 80},{NY + 22} L{nodes[k + 1][0] - 2},{NY + 22}" marker-end="url(#m-b)"/>')
    elif k == 2:
        o(f'<circle cx="{x + 80}" cy="{NY + 22}" r="3" fill="var(--b-s)"/>')
        o(f'<path class="arrow a-b dashed" d="M{x + 80},{NY + 22} L{nodes[3][0] - 2},{NY + 22}" marker-end="url(#m-b)"/>')
        o(f'<text class="sm muted" x="{(x + 90 + nodes[3][0]) / 2:g}" y="{NY + 16}" text-anchor="middle">…</text>')
    else:
        o(f'<text class="xs mono" x="{x + 80}" y="{NY + 26}" text-anchor="middle">∅</text>')
o(f'<text class="xs mono muted" x="{nodes[0][0] + 45}" y="{NY + 58}" text-anchor="middle">рядок 1</text>')
o(f'<text class="xs muted" x="{nodes[3][0] + 90}" y="{NY + 58}" text-anchor="end">next = nullptr</text>')
for lab, x in [("head", nodes[0][0] + 35), ("tail", nodes[3][0] + 35)]:
    o(f'<text class="sm mono b" x="{x}" y="{NY - 18}" text-anchor="middle">{lab}</text>')
    o(f'<path class="arrow a-io" d="M{x},{NY - 14} L{x},{NY - 3}" marker-end="url(#m-io)"/>')
for k, line in enumerate([
    "append:  tail-&gt;next = t; tail = t;    <tspan class=\"muted\">// порожній: head = tail = t</tspan>",
    "обхід:   for (Token* t = head; t; t = t-&gt;next)",
    "кінець:  пройти й delete кожен вузол",
]):
    o(f'<text class="xs mono" x="44" y="{Q + 180 + 18 * k}" style="white-space:pre">{line}</text>')
o(f'<text class="sm muted" x="44" y="{Q + 240}">Файл буває будь-якої довжини — тому список, а не масив. Забули <tspan class="mono">delete</tspan> — витік.</text>')
o()

# ---------- Панель 4 ----------
o('<!-- 4. Два проходи -->')
o(f'<rect class="box" x="548" y="{Q}" width="508" height="254" rx="10"/>')
o(f'<text class="h2" x="568" y="{Q + 26}">4. Два проходи: мітка нижче за стрибок</text>')
chip(1016, Q + 12, "§2")
o(f'<text class="xs muted" x="568" y="{Q + 48}">Програма <tspan class="mono">forward</tspan> з Notes 08 §4; досліди <tspan class="mono">06</tspan> і <tspan class="mono">09</tspan> у практиці Lab 08.</text>')
hx = [568, 616, 742, 892]
for x, h in zip(hx, ["адр.", "текст", "один прохід", "два проходи"]):
    o(f'<text class="xs b" x="{x}" y="{Q + 72}">{h}</text>')
o(f'<line class="rule" x1="568" y1="{Q + 78}" x2="1036" y2="{Q + 78}"/>')
rows = [("0000", "JMP done", '30 <tspan class="err">?? ??</tspan>', "30 04 00"),
        ("0003", "NOP", "01", "01"),
        ("0004", "done: HALT", "00", "00")]
for k, (a, t, one, two) in enumerate(rows):
    y = Q + 98 + 22 * k
    o(f'<text class="sm mono muted" x="{hx[0]}" y="{y}">{a}</text>')
    o(f'<text class="sm mono" x="{hx[1]}" y="{y}">{t}</text>')
    o(f'<text class="sm mono" x="{hx[2]}" y="{y}">{one}</text>')
    o(f'<text class="sm mono{" ok" if k == 0 else ""}" x="{hx[3]}" y="{y}">{two}</text>')
o(f'<text class="sm" x="568" y="{Q + 178}"><tspan class="b">Прохід 1:</tspan> адреса = сума розмірів: <tspan class="mono">0 + 3 + 1</tspan> → <tspan class="mono">done = 0x0004</tspan>.</text>')
o(f'<text class="sm" x="568" y="{Q + 198}"><tspan class="b">Прохід 2:</tspan> видати байти, підставивши <tspan class="mono">0x0004</tspan>: <tspan class="mono ok">30 04 00</tspan>.</text>')
o(f'<text class="sm muted" x="568" y="{Q + 222}">Мітка вище стрибка відома одразу; нижче — лише після проходу 1.</text>')
o(f'<text class="sm muted" x="568" y="{Q + 240}">Вставте <tspan class="mono">NOP</tspan> вище <tspan class="mono">base</tspan> у <tspan class="mono">fact</tspan> — зсунуться обидва <tspan class="mono">JZ base</tspan>.</text>')
o('</svg>')

open(sys.argv[1], "w").write("\n".join(out) + "\n")
