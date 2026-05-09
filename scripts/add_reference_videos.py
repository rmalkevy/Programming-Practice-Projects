#!/usr/bin/env python3
"""Replace 'Instructor TODO' placeholder lines with curated YouTube reference videos.

Each lab gets a single 'Reference video' block-quote line pointing at a hand-picked
YouTube video that demonstrates a polished example of the lab's project type.
External 'Compare against ...' references already present in the lab are preserved.
"""

import os
import sys

# (lab_number, replacement_line) — replacement_line is the FULL replacement,
# including the leading `> ` and any preserved external references.
REPLACEMENTS = {
    1: (
        "> **Reference build:** [Build and Deploy a Full Stack Realtime Chat Messaging App — JavaScript Mastery](https://www.youtube.com/watch?v=MJzbJQLGehs) — shows the polish bar a personal-chat product can hit end-to-end."
    ),
    2: (
        "> **Reference build:** [Coding Challenge #146 — Rendering Raycasting — The Coding Train](https://www.youtube.com/watch?v=vYgIKn7iDH8) — Daniel Shiffman walks through exactly the 2D-rays-to-3D-walls journey this lab asks of you. Pair with [Coding Challenge #145: 2D Raycasting](https://www.youtube.com/watch?v=TOEi6T2mtHo) as a primer."
    ),
    3: (
        "> **Reference build:** [Coding Adventure: Ray Tracing — Sebastian Lague](https://www.youtube.com/watch?v=Qz0KTGYJtUk) — gold-standard look-and-feel target for the Standard / Advanced acceptance criteria of this lab."
    ),
    4: (
        "> **Reference builds:** [Real-Time Data Logging with Arduino: Mastering millis() and SD Cards](https://www.youtube.com/watch?v=RAJH2B3PVXM) for the SD-card-logging spine, and [Andreas Spiess — How to work with FreeRTOS on ESP32](https://www.youtube.com/watch?v=684KSAvYbw4) for embedded multitasking culture."
    ),
    5: (
        "> **Reference video:** [But what is a convolution? — 3Blue1Brown](https://www.youtube.com/watch?v=KuXjwB4LzSA) — the cleanest visual explanation of the core operation behind every kernel filter in this lab."
    ),
    6: (
        "> **Reference video:** [Data Structures Easy to Advanced Course — William Fiset / freeCodeCamp](https://www.youtube.com/watch?v=RBSGKlAvoiM) — animated BST walkthroughs that match this lab's visualization spirit. (Compare against [VisuAlgo](https://visualgo.net/en/bst) for the look-and-feel target.)"
    ),
    7: (
        "> **Reference video:** [A* Pathfinding (E01: algorithm explanation) — Sebastian Lague](https://www.youtube.com/watch?v=-L-WgKMFuhE) — the cleanest A* explanation on YouTube. Pair with Computerphile's [A* (A Star) Search Algorithm](https://www.youtube.com/watch?v=ySN5Wnu88nE) for a tighter intuition primer."
    ),
    8: (
        "> **Reference video:** [The Mandelbrot Set — Numberphile (with Dr. Holly Krieger)](https://www.youtube.com/watch?v=NGMRB4O922I) — the gentlest, most cited intro to *what* you're rendering. Pair with [The Coding Train — Coding Challenge #21: Mandelbrot Set with p5.js](https://www.youtube.com/watch?v=6z7GQewK-Ks) for a build-along."
    ),
    9: (
        "> **Reference video:** [Pong with Python & Pygame — Tech With Tim / freeCodeCamp](https://www.youtube.com/watch?v=tS8F7_X2qB0) — comprehensive 1-hour build of the canonical paddle game; matches this lab's Standard target."
    ),
    10: (
        "> **Reference video:** [The Coding Train — Maze Generator series (Coding Challenge #10)](https://www.youtube.com/playlist?list=PL3Esa3e6Kj9qcBFxrsP5DK8E_1dO5t_m1) — Daniel Shiffman builds a recursive-backtracker maze generator step by step; matches this lab's Basic and Standard milestones."
    ),
    11: (
        "> **Reference build:** [Developing a Terminal App in Go with Bubble Tea — package main](https://www.youtube.com/watch?v=_gzypL-Qv-g) — fundamentals of building polished TUI apps in Go (the techniques transfer cleanly to a file explorer)."
    ),
    12: (
        "> **Reference build:** [How To Build Your First TypeScript Project — TODO List Application — Web Dev Simplified](https://www.youtube.com/watch?v=jBmrduvKl5w) — clean baseline for the Standard target. For the full-stack flavor, pair with any classic [Theo / WebDevSimplified] follow-up tutorials."
    ),
    13: (
        "> **Reference build:** [Writing a Physics Engine from scratch — collision detection optimization — Pezzza's Work](https://www.youtube.com/watch?v=9IULfQH7E90) — Verlet-physics in C++, with the legendary spatial-grid optimization. The visual bar to aim for at the Advanced level."
    ),
    14: (
        "> **Reference video:** [7.3: The Game of Life — The Coding Train (Nature of Code)](https://www.youtube.com/watch?v=tENSCEO-LEc) — Conway in 16 minutes, with code. Pair with [Coding Challenge #179: Elementary Cellular Automata](https://www.youtube.com/watch?v=Ggxt06qSAe4) for the 1D companion."
    ),
    15: (
        "> **Reference build:** [Search Engine in Rust (Ep.01) — Tsoding Daily](https://www.youtube.com/watch?v=hm5xOJiVEeg) — live-coded TF-IDF inverted-index search engine built from scratch; the spirit of the Advanced target."
    ),
    16: (
        "> **Reference build:** [ESP32 Based IoT Weather Station — Complete Guide](https://www.youtube.com/watch?v=GE5an3kYOKQ) — multi-sensor → cloud-dashboard pipeline, end-to-end. Pair with [Andreas Spiess channel](https://www.youtube.com/c/AndreasSpiess) for the full Swiss-accent ESP32 / LoRa / IoT canon."
    ),
    17: (
        "> **Reference build:** [Joop Brokking — *Your Arduino Balancing Robot* (YABR)](http://www.brokking.net/yabr_main.html) — the legendary self-balancing-robot build with code, schematics, and a multi-part [video walkthrough on YouTube](https://www.youtube.com/playlist?list=PL0K4VDicBzshc4hIwPZ1B-faaaY9DPbLf) (start with Part 1 — *PID controller explained*)."
    ),
    18: (
        "> **Reference build:** [ESP32 Project 35 — Plant Monitor: soil, temperature & light — SunFounder](https://www.youtube.com/watch?v=SdgvQlIllPA) — clean ESP32 plant-monitor build matching the Basic level. Pair with [Why most Arduino soil-moisture sensors suck — Andreas Spiess](https://www.youtube.com/watch?v=m0mcCtcViTY) before you buy hardware."
    ),
    19: (
        "> **Reference build:** [Adafruit Arcade Fightstick guide](https://learn.adafruit.com/arcade-fightstick) — a full custom-controller build (RP2040 + arcade buttons + USB-HID firmware), with [demo video](https://www.youtube.com/watch?v=eA55A6IIOZw). The same pattern scales to any custom HID device this lab might become."
    ),
    20: (
        "> **Reference videos:** browse [Lee Robinson's YouTube channel](https://www.youtube.com/c/LeeRobinsonDev) for modern Next.js / personal-site deep-dives. (Compare against [brittanychiang.com](https://brittanychiang.com/) and [paco.me](https://paco.me/) for the look-and-feel target.)"
    ),
    21: (
        "> **Reference build:** [JWT Authentication Tutorial — Node.js — Web Dev Simplified](https://www.youtube.com/watch?v=mbsmsi7l3r4) for the auth spine, then [JWT Authentication with Access Tokens & Refresh Tokens](https://www.youtube.com/watch?v=XYjOteYbCMo) for the production-grade refresh-token pattern."
    ),
    22: (
        "> **Reference videos:** [Fireship — Frontend Frameworks playlist](https://www.youtube.com/playlist?list=PLXU6UYQih-Bp1b8lUwZn36LLMwTs7tZB2) for the 100-second tour of every modern SPA framework — pick yours, then build."
    ),
    23: (
        "> **Reference build:** [How to Create the Simplest .io Game in 30 Minutes — JavaScript + Node.js + Socket.IO](https://www.youtube.com/watch?v=hj4ZF1FlkDE) — full real-time multiplayer baseline in 30 minutes; matches the Basic target end-to-end."
    ),
    24: (
        "> **Reference build:** [Build a Chrome Extension — Course for Beginners — freeCodeCamp](https://www.youtube.com/watch?v=0n809nd4Zu4) — Manifest V3 from scratch with a real published-extension target."
    ),
    25: (
        "> **Reference build:** [Pygame Platformer Tutorial — Full Course — DaFluffyPotato](https://www.youtube.com/watch?v=2gABYM5M0ww) — 6-hour platformer build covering tiles, physics, particles, parallax, AI, level editing, and packaging. The Advanced bar for this lab."
    ),
    26: (
        "> **Reference video:** [I Tried to make a Roguelike in One Month — Devlog](https://www.youtube.com/watch?v=tl21e4y0iyQ) — solo procgen-roguelike devlog covering scope, polish, and the Steam-release path."
    ),
    27: (
        "> **Reference build:** [Coding Challenge #32.1: Agar.io — Part 1 (Basic Game Mechanics) — The Coding Train](https://www.youtube.com/watch?v=JXuxYMGe4KI) — multi-part .io-game build with WebSockets and a real multiplayer server. The Standard target lives here."
    ),
    28: (
        "> **Reference video:** [I Spent a Week Making a Game about Vacuuming — Sebastian Lague](https://www.youtube.com/watch?v=PGk0rnyTa1U) — the spirit of a small-scope themed jam: tight loop, surprising polish, shipped. Pair with any [Game Maker's Toolkit Game Jam recap](https://www.youtube.com/c/MarkBrownGMT) for jam-culture inspiration."
    ),
    29: (
        "> **Reference build:** [The Jetpack Compose Beginner Crash Course — Philipp Lackner](https://www.youtube.com/watch?v=6_wK_Ud8--0) — the canonical 2026 Android-native starting point. Pair with [Material 3 Apps with Jetpack Compose](https://www.youtube.com/watch?v=h7K4n9C2jkI) once your app needs polish."
    ),
    30: (
        "> **Reference videos:** [William Candillon — *Can it be done in React Native?* channel](https://www.youtube.com/@wcandillon) — recreations of polished native interactions (Spotify, Airbnb, YouTube, Duolingo) in React Native. The look-and-feel bar for this lab's Advanced target."
    ),
    31: (
        "> **Reference build:** [Chatbots with RAG: LangChain Full Walkthrough — James Briggs](https://www.youtube.com/watch?v=LhnCsygAvzY) — embeddings + Pinecone + LangChain end-to-end; matches the Standard target. Pair with [LangChain Multi-Query Retriever for RAG](https://www.youtube.com/watch?v=VFf8XJUIHnU) for the Advanced retrieval techniques."
    ),
    32: (
        "> **Reference video:** [The spelled-out intro to neural networks and backpropagation: building micrograd — Andrej Karpathy](https://www.youtube.com/watch?v=VMj-3S1tku0) — *the* video. The Standard target of this lab is essentially \"finish this video.\" The full [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) playlist is the Advanced map."
    ),
    33: (
        "> **Reference build:** [Track & Count Objects using YOLOv8, ByteTrack & Supervision — Roboflow](https://www.youtube.com/watch?v=OS5qI9YBkfk) — full detection-plus-tracking-plus-counting pipeline matching this lab's Standard and Advanced targets."
    ),
    34: (
        "> **Reference video:** [Cursor Team — Future of Programming with AI — Lex Fridman Podcast #447](https://www.youtube.com/watch?v=oFfVt3S51T4) — a 2.5-hour conversation with the founders of one of the most polished AI products in existence. The bar for what \"narrow, polished, AI-native\" means in 2026."
    ),
    35: (
        "> **Reference build:** [Carbon Aeronautics — Quadcopter Drone series](https://github.com/CarbonAeronautics) — multi-part YouTube series (search the channel) covering quadcopter dynamics, PID, Kalman filtering, and rate-mode flight. Pair with [Andreas Spiess — How to work with FreeRTOS on ESP32](https://www.youtube.com/watch?v=684KSAvYbw4) for the RTOS task-and-queue culture."
    ),
    36: (
        "> **Reference build:** [Buildroot Tutorial — Linux Kernel on QEMU Virtual board](https://www.youtube.com/watch?v=oy5PtFhVk5E) — boot a custom Linux from scratch, in a VM, with running user-space; the Basic target of this lab made concrete. For the deeper systems-engineering culture, browse [Bootlin's training pages](https://bootlin.com/training/)."
    ),
    37: (
        "> **Reference videos:** [Ardupilot & PX4 SITL — From 0 to 100 in One Hour](https://www.youtube.com/watch?v=mKt4ZTaE2bk) for the toolchain-and-first-mission spine, and [Swarm of 16 PX4 Drones Creates 3D Heart Shape — MAVSDK Drone Show SITL Demo](https://www.youtube.com/watch?v=7j3QzX3dlfk) for the visual bar of what's possible at the Advanced level."
    ),
    38: (
        "> **Reference videos:** the entire [Binary Exploitation / Memory Corruption playlist by LiveOverflow](https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN) is the canonical reference for this lab. Start with [Writing a Simple Buffer Overflow Exploit](https://www.youtube.com/watch?v=oS2O75H57qU)."
    ),
}


def main() -> None:
    labs_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, 'labs'
    )
    labs_dir = os.path.normpath(labs_dir)

    # Map lab number → file name (only those that have an Instructor TODO line).
    lab_files = {n: f for n, f in [
        (1, 'lab-01-messenger.md'),
        (2, 'lab-02-ray-casting-engine.md'),
        (3, 'lab-03-ray-tracer.md'),
        (4, 'lab-04-stm32-sensor-logger.md'),
        (5, 'lab-05-image-processor.md'),
        (6, 'lab-06-digital-tree-visualizer.md'),
        (7, 'lab-07-graph-route-finder.md'),
        (8, 'lab-08-fractal-generator.md'),
        (9, 'lab-09-console-paddle-game.md'),
        (10, 'lab-10-maze-generator-solver.md'),
        (11, 'lab-11-mini-file-explorer.md'),
        (12, 'lab-12-task-tracker.md'),
        (13, 'lab-13-physics-sandbox.md'),
        (14, 'lab-14-cellular-automata.md'),
        (15, 'lab-15-mini-search-engine.md'),
        (16, 'lab-16-smart-telemetry-beacon.md'),
        (17, 'lab-17-pid-self-balancer.md'),
        (18, 'lab-18-smart-plant-monitor.md'),
        (19, 'lab-19-custom-game-controller.md'),
        (20, 'lab-20-personal-portfolio.md'),
        (21, 'lab-21-rest-api-auth.md'),
        (22, 'lab-22-spa-frontend.md'),
        (23, 'lab-23-realtime-multiplayer.md'),
        (24, 'lab-24-browser-extension.md'),
        (25, 'lab-25-platformer-game.md'),
        (26, 'lab-26-procedural-roguelike.md'),
        (27, 'lab-27-multiplayer-browser-game.md'),
        (28, 'lab-28-game-jam.md'),
        (29, 'lab-29-android-native-app.md'),
        (30, 'lab-30-cross-platform-app.md'),
        (31, 'lab-31-llm-rag-app.md'),
        (32, 'lab-32-neural-net-from-scratch.md'),
        (33, 'lab-33-object-detection-tracking.md'),
        (34, 'lab-34-ai-capstone.md'),
        (35, 'lab-35-rtos-mini-autopilot.md'),
        (36, 'lab-36-embedded-linux-from-inside.md'),
        (37, 'lab-37-px4-mavlink-drone-stack.md'),
        (38, 'lab-38-binary-exploitation.md'),
    ]}

    updated = 0
    skipped = 0
    for lab_num, fname in lab_files.items():
        path = os.path.join(labs_dir, fname)
        if not os.path.exists(path):
            print(f'  MISSING: {path}', file=sys.stderr)
            skipped += 1
            continue

        with open(path, encoding='utf-8') as f:
            text = f.read()

        # Find the line that starts with '> **Instructor TODO:' and replace it.
        lines = text.split('\n')
        replaced = False
        new_line = REPLACEMENTS.get(lab_num)
        if not new_line:
            print(f'  no replacement defined for lab {lab_num}')
            skipped += 1
            continue

        for i, line in enumerate(lines):
            if line.lstrip().startswith('> **Instructor TODO:'):
                lines[i] = new_line
                replaced = True
                break

        if not replaced:
            print(f'  {fname}: no Instructor TODO line found — skipped')
            skipped += 1
            continue

        new_text = '\n'.join(lines)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f'  {fname}: replaced')
        updated += 1

    print(f'\nUpdated: {updated} files. Skipped: {skipped}.')


if __name__ == '__main__':
    main()
