# 42 — A Programming Practice Program

> "The Answer to the Great Question … Of Life, the Universe and Everything … Is … **Forty-two**."
> — Douglas Adams, *The Hitchhiker's Guide to the Galaxy*

A self-contained, year-long programming program for first-year computer-science / software-engineering / aerospace-engineering students. **Forty-two practical labs**, written to be motivational, honest, employable, and fun. Designed in Ukraine, for the next generation of Ukrainian engineers — but transplantable to any first- or second-year cohort, anywhere.

---

## What this program is

- **42 labs**, each a self-contained Markdown brief — `labs/lab-NN-slug.md`.
- Each lab is **2–3 weeks** of default work; each has explicit **Extension Challenges** that stretch it to 3–5 weeks.
- Every lab leaves a **portfolio-grade artifact** behind — public repo, public deploy, public demo video.
- Every lab includes a **Reflection** for defense, a **showcase**-ready writeup, and a *Make-it-yours* personal-twist requirement.
- The final lab — **Lab 42 — Life, The Universe, And Everything** — is the student's own École-42-spirited capstone.

The program covers: software fundamentals · graphics & math · algorithms · embedded systems · web & full-stack · games · mobile · AI/ML · RTOS & Linux internals · drone autopilots · security (offensive + defensive) · orbital mechanics · and a meta-capstone.

---

## How to use this repo

| If you are a… | Read this first |
|---|---|
| **Student picking labs** | [`TRACK_PICKER.md`](./TRACK_PICKER.md) |
| **Student starting a specific lab** | [`labs/README.md`](./labs/README.md) → pick lab → open the lab file |
| **Student doing the capstone (Lab 42)** | [`templates/MANIFESTO_TEMPLATE.md`](./templates/MANIFESTO_TEMPLATE.md) |
| **Instructor / TA / mentor** | [`INSTRUCTOR_HANDBOOK.md`](./INSTRUCTOR_HANDBOOK.md) |
| **Curious recruiter / parent / friend** | [`labs/README.md`](./labs/README.md) — the full index with one-line pitches |

---

## The 42 in one screen

| # | Title | Domain |
|---|---|---|
| 01 | Mini Messenger | software / fullstack |
| 02 | Wolfenstein-like Ray Casting Engine | graphics |
| 03 | Simple Ray Tracer | graphics / math |
| 04 | Embedded Sensor Logger | embedded |
| 05 | Image Processor | algorithms / graphics |
| 06 | Digital Tree Visualizer | algorithms |
| 07 | Graph Route Finder | algorithms |
| 08 | Fractal Generator | math / graphics |
| 09 | Console Paddle Game | game |
| 10 | Maze Generator and Solver | algorithms / game |
| 11 | Mini File Explorer | software |
| 12 | Task Tracker | software / fullstack |
| 13 | Physics Sandbox | math / simulation |
| 14 | Cellular Automata Simulator | simulation |
| 15 | Mini Search Engine | algorithms / data |
| 16 | Smart Telemetry Beacon | embedded / IoT |
| 17 | PID Self-Balancing Robot | embedded / control |
| 18 | Smart Plant Monitor | embedded / IoT |
| 19 | Custom Game Controller | embedded / hardware |
| 20 | Personal Portfolio Site | web |
| 21 | REST API With Auth | web / backend |
| 22 | SPA Frontend | web / frontend |
| 23 | Real-Time Multiplayer Service | web / realtime |
| 24 | Browser Extension | web / product |
| 25 | Platformer Game | game |
| 26 | Procedural Roguelike | game |
| 27 | Multiplayer Browser Game | game / realtime |
| 28 | Game Jam | game / product |
| 29 | Android Native App | mobile |
| 30 | Cross-Platform App (React Native) | mobile |
| 31 | LLM RAG App | AI |
| 32 | Neural Net From Scratch | AI / math |
| 33 | Object Detection And Tracking | AI / vision |
| 34 | AI Capstone | AI / product |
| 35 | RTOS Mini-Autopilot | embedded / RTOS |
| 36 | Embedded Linux From The Inside | embedded / Linux |
| 37 | PX4 + MAVLink + ROS 2 Drone Stack | embedded / drones |
| 38 | Smash The Stack: Binary Exploitation | security |
| 39 | OWASP Top 10 (Web Security) | security / web |
| 40 | Network / Wireless / Drone-Link Security | security / RF |
| 41 | Mostly Harmless: Orbital Mechanics | space / math |
| 42 | Life, The Universe, And Everything | meta / capstone |

For full pitches, difficulty groupings, suggested tracks, and cross-lab pairings, see **[`labs/README.md`](./labs/README.md)**.

---

## Tracks

Eight curated paths through the program; pick one with the help of [`TRACK_PICKER.md`](./TRACK_PICKER.md).

- **Track A** — Defense / Aerospace / Drones (Ukrainian flagship)
- **Track B** — AI / ML
- **Track C** — Full-Stack Engineer
- **Track D** — Game Developer
- **Track E** — Embedded / Systems
- **Track F** — Security Engineer
- **Track G** — Mobile Developer
- **Track H** — Math / Graphics / Simulation
- **Track Z** — *The Hitchhiker's Path* (the official "I don't know" answer)

---

## Repository layout

```txt
.
├── README.md                       # this file
├── INSTRUCTOR_HANDBOOK.md          # for instructors / TAs / mentors
├── TRACK_PICKER.md                 # decision tree for picking 4–6 labs
├── templates/
│   └── MANIFESTO_TEMPLATE.md       # the Lab 42 ceremonial document
└── labs/
    ├── README.md                   # comprehensive lab index
    ├── lab-01-messenger.md
    ├── lab-02-ray-casting-engine.md
    ├── ...
    └── lab-42-life-the-universe-and-everything.md
```

---

## Design principles

The program is opinionated. The five most important opinions:

1. **Shipping > grading.** Every lab leaves a runnable artifact in the world. *Lateness with a working artifact beats on-time without one.*
2. **The student writes the question (eventually).** Forty-one labs are instructor-prompted. The forty-second is the student's own.
3. **Make it yours is required, not optional.** Every lab includes a personal-twist section the student must defend.
4. **Honest stakes.** Security labs ship with `ETHICS.md`. Drone labs run in simulation. Real users matter; vanity metrics don't.
5. **Don't Panic.** The tone of the labs is deliberately warm. They were written to be re-read at 2 AM the night before a defense — and to leave the student feeling capable, not crushed.

---

## License & contribution

The labs are licensed permissively (see `LICENSE` once added — recommendation: CC-BY-4.0 for the prose, MIT for any included code samples). Contributions from students who finish labs and notice outdated tooling, broken links, or unclear sentences are welcomed and credited — *that PR is part of your portfolio.*

For larger structural changes (adding labs, restructuring tracks), open an issue first.

---

## Acknowledgments

Built for the next generation of Ukrainian engineers in 2026. Inspired in spirit by **École 42** (peer review, ship-or-die, open-ended ambition) and **Douglas Adams** (the answer is 42 — but only if you've found the right question). Carries deep debts to the open-source teaching tradition: Karpathy's neural-net lectures, the Ray Tracing in One Weekend series, OWASP's documentation, PX4's simulator, the Cornell BMW astrodynamics text, the *Phrack* archive, and a thousand YouTube creators whose hours kept the labs grounded in reality.

---

> **Don't Panic.**
> — *The Hitchhiker's Guide to the Galaxy*

42.
