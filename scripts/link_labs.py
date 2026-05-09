#!/usr/bin/env python3
"""Add cross-lab markdown links inside every lab-NN-*.md file.

For each lab file, wraps every "Lab NN" / "Labs NN, NN, NN" / "Labs NN-NN"
reference (where NN != the file's own number) with a markdown link
to the corresponding lab file. Skips:

- the file's own H1 title line (line 0),
- fenced code blocks,
- already-linked references like [Lab 35](url),
- self-references (lab-35 referring to "Lab 35").
"""

import os
import re
import sys

LAB_FILES = {
    1: "lab-01-messenger.md",
    2: "lab-02-ray-casting-engine.md",
    3: "lab-03-ray-tracer.md",
    4: "lab-04-stm32-sensor-logger.md",
    5: "lab-05-image-processor.md",
    6: "lab-06-digital-tree-visualizer.md",
    7: "lab-07-graph-route-finder.md",
    8: "lab-08-fractal-generator.md",
    9: "lab-09-console-paddle-game.md",
    10: "lab-10-maze-generator-solver.md",
    11: "lab-11-mini-file-explorer.md",
    12: "lab-12-task-tracker.md",
    13: "lab-13-physics-sandbox.md",
    14: "lab-14-cellular-automata.md",
    15: "lab-15-mini-search-engine.md",
    16: "lab-16-smart-telemetry-beacon.md",
    17: "lab-17-pid-self-balancer.md",
    18: "lab-18-smart-plant-monitor.md",
    19: "lab-19-custom-game-controller.md",
    20: "lab-20-personal-portfolio.md",
    21: "lab-21-rest-api-auth.md",
    22: "lab-22-spa-frontend.md",
    23: "lab-23-realtime-multiplayer.md",
    24: "lab-24-browser-extension.md",
    25: "lab-25-platformer-game.md",
    26: "lab-26-procedural-roguelike.md",
    27: "lab-27-multiplayer-browser-game.md",
    28: "lab-28-game-jam.md",
    29: "lab-29-android-native-app.md",
    30: "lab-30-cross-platform-app.md",
    31: "lab-31-llm-rag-app.md",
    32: "lab-32-neural-net-from-scratch.md",
    33: "lab-33-object-detection-tracking.md",
    34: "lab-34-ai-capstone.md",
    35: "lab-35-rtos-mini-autopilot.md",
    36: "lab-36-embedded-linux-from-inside.md",
    37: "lab-37-px4-mavlink-drone-stack.md",
    38: "lab-38-binary-exploitation.md",
    39: "lab-39-web-security-owasp.md",
    40: "lab-40-network-wireless-drone-security.md",
    41: "lab-41-mostly-harmless-orbital-mechanics.md",
    42: "lab-42-life-the-universe-and-everything.md",
}

# Singleton: "Lab 35" not already inside a link.
SINGLE_RE = re.compile(r'(?<!\[)\bLab (\d{1,2})\b(?!\])')

# Range: "Labs 38–40" or "Labs 38-40" (en-dash or hyphen).
RANGE_RE = re.compile(r'(?<!\[)\bLabs (\d{1,2})\s*[\-\u2013]\s*(\d{1,2})\b(?!\])')

# List: "Labs 38, 39, 40" or "Labs 38, 39, and 40" — at least two numbers.
LIST_RE = re.compile(
    r'(?<!\[)\bLabs (\d{1,2}(?:\s*,\s*(?:and\s+)?\d{1,2})+)\b(?!\])'
)


def process_file(path: str, self_n: int) -> int:
    """Return number of replacements made."""
    with open(path, encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')
    in_code = False
    h1_seen = False
    changes = 0

    out_lines = []
    for line in lines:
        # Skip fenced code blocks.
        if line.strip().startswith('```'):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue

        # Skip the file's own first H1 line.
        if not h1_seen and line.startswith('# '):
            h1_seen = True
            out_lines.append(line)
            continue

        # ---- Pass 1: "Labs NN-NN" range -> linkify both endpoints.
        def range_repl(m: re.Match) -> str:
            nonlocal changes
            a = int(m.group(1))
            b = int(m.group(2))
            if not (1 <= a <= 42 and 1 <= b <= 42):
                return m.group(0)
            link_a = (
                f'[{a:02d}]({LAB_FILES[a]})' if a != self_n
                else f'{a:02d}'
            )
            link_b = (
                f'[{b:02d}]({LAB_FILES[b]})' if b != self_n
                else f'{b:02d}'
            )
            # Use the original separator if possible.
            sep = '\u2013' if '\u2013' in m.group(0) else '-'
            changes += 1
            return f'Labs {link_a}{sep}{link_b}'

        line = RANGE_RE.sub(range_repl, line)

        # ---- Pass 2: "Labs NN, NN, NN" list -> linkify each number.
        def list_repl(m: re.Match) -> str:
            nonlocal changes
            inner = m.group(1)
            def num_replace(nm: re.Match) -> str:
                n = int(nm.group(0))
                if not (1 <= n <= 42) or n == self_n:
                    return nm.group(0)
                return f'[{n:02d}]({LAB_FILES[n]})'
            new_inner = re.sub(r'\d{1,2}', num_replace, inner)
            if new_inner == inner:
                return m.group(0)
            changes += 1
            return f'Labs {new_inner}'

        line = LIST_RE.sub(list_repl, line)

        # ---- Pass 3: "Lab NN" singletons.
        def single_repl(m: re.Match) -> str:
            nonlocal changes
            n = int(m.group(1))
            if not (1 <= n <= 42) or n == self_n:
                return m.group(0)
            changes += 1
            return f'[Lab {n}]({LAB_FILES[n]})'

        line = SINGLE_RE.sub(single_repl, line)

        out_lines.append(line)

    new_text = '\n'.join(out_lines)
    if new_text != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
    return changes


def main():
    labs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'labs')
    if not os.path.isdir(labs_dir):
        labs_dir = 'labs'

    total = 0
    for n in range(1, 43):
        fname = LAB_FILES[n]
        path = os.path.join(labs_dir, fname)
        if not os.path.exists(path):
            print(f'  MISSING: {path}', file=sys.stderr)
            continue
        c = process_file(path, n)
        total += c
        if c:
            print(f'  {fname}: {c} replacement(s)')
    print(f'\nTotal replacements: {total}')


if __name__ == '__main__':
    main()
