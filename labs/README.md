# labs/ — The 42-Lab Index

> "Forty-two."
> — Deep Thought

This folder contains the full **42-lab program** for first-year computer-science / software-engineering / aviation-engineering students. Each lab is a self-contained Markdown brief — readable, motivational, defensible, and shaped to leave a portfolio-grade artifact behind.

The program is one year long if a student does ~one lab every two weeks. It is one summer long if a student does the practical-portfolio half intensively. It is the rest of someone's life if Lab 42 turns into a real product.

**Useful companion documents (live one folder up):**
- `../INSTRUCTOR_HANDBOOK.md` — pacing, grading philosophy, showcase-night logistics, recommended semester recipes.
- `../TRACK_PICKER.md` — a decision-tree picker that helps a student select 4–6 labs based on what they care about.
- `../templates/MANIFESTO_TEMPLATE.md` — the ceremonial document for Lab 42.

---

## How this index is organized

The 42 labs are grouped four ways:

1. **By number** — the canonical list, with one-line pitches.
2. **By domain** — software, embedded, web, game, mobile, AI/ML, RTOS/Linux, security, space, capstone.
3. **By difficulty + time** — Basic / Standard / Advanced; default 2-week or 3-week budgets; extension-window estimates.
4. **By suggested track** — pre-curated paths, including a *Hitchhiker's Path* through the program.

The same lab will appear in multiple groupings. That's the point.

---

## The full 42 — by number

| # | Title | Domain | Default time |
|---|---|---|---|
| 01 | Mini Messenger | software / fullstack | 2 weeks |
| 02 | Wolfenstein-like Ray Casting Engine | graphics / algorithms | 2 weeks |
| 03 | Simple Ray Tracer | graphics / math | 2 weeks |
| 04 | Embedded Sensor Logger (STM32 / Arduino / ESP32 / Pico) | embedded | 2 weeks |
| 05 | Image Processor | algorithms / graphics | 2 weeks |
| 06 | Digital Tree Visualizer | algorithms / data structures | 2 weeks |
| 07 | Graph Route Finder | algorithms | 2 weeks |
| 08 | Fractal Generator | math / graphics | 2 weeks |
| 09 | Console Paddle Game | game / software | 2 weeks |
| 10 | Maze Generator and Solver | algorithms / game | 2 weeks |
| 11 | Mini File Explorer | software | 2 weeks |
| 12 | Task Tracker | software / fullstack | 2 weeks |
| 13 | Physics Sandbox | math / simulation | 2 weeks |
| 14 | Cellular Automata Simulator | simulation / algorithms | 2 weeks |
| 15 | Mini Search Engine | algorithms / data | 2 weeks |
| 16 | Smart Telemetry Beacon | embedded / IoT | 2–3 weeks |
| 17 | PID Self-Balancing Robot | embedded / control | 2–3 weeks |
| 18 | Smart Plant Monitor | embedded / IoT | 2–3 weeks |
| 19 | Custom Game Controller | embedded / hardware | 2–3 weeks |
| 20 | Personal Portfolio Site | web / portfolio | 2 weeks |
| 21 | REST API With Auth | web / backend | 2–3 weeks |
| 22 | SPA Frontend | web / frontend | 2–3 weeks |
| 23 | Real-Time Multiplayer Service | web / realtime | 2–3 weeks |
| 24 | Browser Extension | web / product | 2 weeks |
| 25 | Platformer Game | game | 2–3 weeks |
| 26 | Procedural Roguelike | game / algorithms | 2–3 weeks |
| 27 | Multiplayer Browser Game | game / realtime | 3 weeks |
| 28 | Game Jam | game / product | 2 weeks |
| 29 | Android Native App | mobile | 2–3 weeks |
| 30 | Cross-Platform App (React Native) | mobile | 2–3 weeks |
| 31 | LLM RAG App | AI / fullstack | 2–3 weeks |
| 32 | Neural Net From Scratch (Karpathy-style) | AI / math | 2–3 weeks |
| 33 | Object Detection And Tracking | AI / vision | 2–3 weeks |
| 34 | AI Capstone | AI / product | 3 weeks |
| 35 | RTOS Mini-Autopilot | embedded / RTOS | 3 weeks |
| 36 | Embedded Linux From The Inside | embedded / Linux | 3 weeks |
| 37 | PX4 + MAVLink + ROS 2 Drone Stack | embedded / drones | 3 weeks |
| 38 | Smash The Stack: Binary Exploitation | security | 2–3 weeks |
| 39 | Web Security By Breaking The OWASP Top 10 | security / web | 2–3 weeks |
| 40 | Network, Wireless & Drone-Link Security | security / RF | 2–3 weeks |
| 41 | Mostly Harmless: Orbital Mechanics & Mission Planner | space / math | 2–3 weeks |
| 42 | Life, The Universe, And Everything (capstone) | meta / portfolio | 3+ weeks |

Each filename is `lab-NN-slug.md` under this folder.

---

## By domain

### Software fundamentals (great first labs)
- 01 Messenger · 09 Paddle · 10 Maze · 11 File Explorer · 12 Task Tracker · 15 Search Engine

### Graphics, math, and simulation
- 02 Ray Casting · 03 Ray Tracer · 05 Image Processor · 06 Tree Viz · 08 Fractals · 13 Physics Sandbox · 14 Cellular Automata · 41 Orbital Mechanics

### Algorithms and data structures
- 06 Tree Viz · 07 Graph Route · 10 Maze · 14 CA · 15 Search Engine

### Embedded and hardware
- 04 Sensor Logger · 16 Telemetry Beacon · 17 PID Robot · 18 Plant Monitor · 19 Game Controller · 35 RTOS Autopilot · 36 Embedded Linux · 37 PX4 Drone Stack

### Web and full-stack
- 12 Task Tracker · 20 Portfolio · 21 REST API · 22 SPA · 23 Realtime · 24 Extension

### Game development
- 09 Paddle · 10 Maze · 13 Physics · 14 CA · 25 Platformer · 26 Roguelike · 27 Multiplayer Game · 28 Game Jam

### Mobile
- 29 Android Native · 30 Cross-Platform (React Native)

### AI / ML
- 31 LLM RAG · 32 NN From Scratch · 33 Object Detection & Tracking · 34 AI Capstone

### Security (offensive + defensive)
- 38 Binary Exploitation · 39 Web/OWASP · 40 Network/Wireless/Drone-Link

### Space / aerospace / aviation
- 04 Sensor Logger · 16 Telemetry Beacon · 17 PID Robot · 35 RTOS Autopilot · 37 PX4 Drone Stack · 40 Drone-Link Security · 41 Orbital Mechanics

### Meta / capstone
- 28 Game Jam · 34 AI Capstone · 42 Life, The Universe, And Everything

---

## By difficulty (Basic → Standard → Advanced)

These are *starting* difficulties. Every lab has Extension Challenges that take it from a 2-week sprint to a 3–5-week portfolio piece (Lab 42 stretches to a summer).

### Basic — gentle on-ramps
- 01 Messenger · 09 Paddle · 10 Maze · 11 File Explorer · 12 Task Tracker · 20 Portfolio · 24 Extension · 28 Game Jam

### Standard — meaty mid-program
- 05 Image Processor · 06 Tree Viz · 07 Graph Route · 08 Fractals · 14 CA · 15 Search Engine · 16 Telemetry · 18 Plant Monitor · 19 Controller · 21 REST API · 22 SPA · 25 Platformer · 26 Roguelike · 29 Android · 30 Cross-Platform · 31 LLM RAG · 33 Object Detection · 39 OWASP

### Advanced — big stretches
- 02 Ray Casting · 03 Ray Tracer · 04 Sensor Logger · 13 Physics · 17 PID Robot · 23 Realtime · 27 Multiplayer Game · 32 NN From Scratch · 34 AI Capstone · 35 RTOS Autopilot · 36 Embedded Linux · 37 PX4 Stack · 38 Binary Exploit · 40 Drone-Link · 41 Orbital Mechanics

### The boss
- 42 Life, The Universe, And Everything

---

## Suggested tracks

A *track* is 4–6 labs that hang together. Use them as one-semester syllabuses, intensive summer paths, or self-study itineraries. Lab 42 is the recommended closer for any track — you can synthesize 2–3 of the prior labs into your final answer.

### Track A — *Defense / Aerospace / Drones (Ukrainian-context flagship)*
**04 Sensor Logger → 17 PID Robot → 35 RTOS Autopilot → 37 PX4 Stack → 40 Drone-Link Security → 42**
Ukrainian defense-tech employability path. Real Yuzhmash / Firefly / Promin / Skyrora alignment. Add 41 Orbital Mechanics for satellite-flavor extension.

### Track B — *AI / ML*
**31 LLM RAG → 32 NN From Scratch → 33 Object Detection → 34 AI Capstone → 42**
End-to-end modern AI: from-scratch math, vision, language, shipped product. Add 22 SPA for the deployable UI layer.

### Track C — *Full-Stack Engineer*
**12 Task Tracker → 20 Portfolio → 21 REST API → 22 SPA → 23 Realtime → 42**
The classic web-engineer pipeline. Lab 42 typically becomes a small SaaS / civic-tech / community-tool project.

### Track D — *Game Developer*
**09 Paddle → 10 Maze → 25 Platformer → 26 Roguelike → 27 Multiplayer Game → 28 Jam → 42**
Six labs with a built-in jam. Lab 42 is usually the polished final game.

### Track E — *Embedded / Systems Programmer*
**04 Sensor Logger → 16 Telemetry → 19 Game Controller → 35 RTOS Autopilot → 36 Embedded Linux → 42**
The "I want to write firmware" path. Combines beautifully with a Lab 38 (binary exploitation) extension.

### Track F — *Security Engineer*
**21 REST API → 38 Binary Exploit → 39 OWASP → 40 Drone-Link → 42**
Build first (Lab 21) so you have something of your own to break. Then attacker-then-defender across three layers.

### Track G — *Mobile Developer*
**20 Portfolio → 22 SPA → 29 Android → 30 Cross-Platform → 42**
A mobile-shipping pipeline; Lab 42 typically ships to a real app store or as a sideloadable APK.

### Track H — *Math / Graphics / Simulation*
**02 Ray Casting → 03 Ray Tracer → 08 Fractals → 13 Physics → 14 CA → 41 Orbital Mechanics → 42**
The "I want to feel math as a superpower" path. Visually iconic portfolio.

### Track Z — *The Hitchhiker's Path* (built-in homage)
**01 Messenger → 03 Ray Tracer → 13 Physics Sandbox → 31 LLM RAG → 41 Orbital Mechanics → 42**
A guided tour from "first shipped thing" to "Mostly Harmless" to "Life, the Universe, and Everything." Recommended if a student has no domain preference and just wants the program's *spirit*. Don't Panic.

---

## Quick-reference: pairings & cross-lab synergies

These pairs / triples are explicitly endorsed by the labs themselves; their *Extension Challenges* sections cite them directly. Pick a pair when you want a 4–5-week project instead of a 2-week one.

- **21 + 22** → full-stack web product
- **21 + 22 + 23** → real-time full-stack
- **21 + 38 + 39** → service + attacker-then-defender
- **22 + 24** → SPA + browser-extension companion
- **25 + 27** → single-player engine grown into multiplayer
- **26 + 14** → roguelike with cellular-automata caves
- **31 + 32** → use your from-scratch NN inside your RAG app
- **32 + 33** → train your own detector from your own NN
- **31 + 33 + 34** → multimodal AI capstone
- **35 + 37** → write your autopilot, fly it in PX4 SITL
- **35 + 36** → RTOS firmware *plus* Linux companion
- **36 + 38** → exploit your own kernel module
- **37 + 40** → drone stack *with* secured MAVLink link
- **41 + 32** → RL controller for low-thrust trajectories
- **41 + 37** → orbital guidance running on PX4
- **40 + 16** → secure your own IoT telemetry
- **39 + 21** → pen-test your own service end-to-end

---

## Conventions inside each lab

Every lab uses the same template (with two structural variants for product-flavored vs algorithmic-flavored labs):

1. **Hook** — the story, including the cultural reference / appetizer (a YouTube video, a famous book, a free tutorial).
2. **Why this is worth your time** — the employability / curiosity / portfolio argument.
3. **The target** — Basic / Standard / Advanced acceptance criteria.
4. **The big idea / diagram** — Mermaid sketch of the architecture.
5. **Two-week plan with milestones** — daily breakdown.
6. **Levels** — Basic, Standard, Advanced (with Side Quests inside Advanced).
7. **Extension challenges (3–5 weeks)** — explicit pairings with other labs.
8. **Make it yours (required)** — student picks a personal twist.
9. **Working solo or in a team** — solo or up to 3, with Git-from-day-one and who-did-what required for teams.
10. **Tooling and platform tips.**
11. **Suggested project structure.**
12. **When you get stuck.**
13. **Submission / Deployment checklist** (algorithmic labs use *Submission*; product labs use *Deployment*).
14. **What evaluators / recruiters look at** (algorithmic labs use *evaluators*; product labs use *recruiters*).
15. **What to put in your README.**
16. **Reflection** — the defense questions.
17. **Showcase** — gallery night.
18. **Going further** — books, talks, communities.
19. **A final word** — the closing emotional beat.

Lab 42 is the deliberate exception: it has no instructor-set acceptance criteria, only the **shipped / not shipped** binary and the requirement of a `MANIFESTO.md`.

---

## Ethical labs (read first)

The three security labs (38, 39, 40) open with a **`⚠ Read this first — Ethics, Legality, Sandbox`** block whose rules are non-negotiable. Every project derived from those labs must include an `ETHICS.md`. Anyone teaching from this folder should read those three blocks before assigning.

The drone-stack lab (37) and the drone-link security lab (40) **never use real aircraft**. All experiments live inside PX4 SITL or a Wi-Fi access point the student owns.

---

## Where to start (quick recipe)

1. Read `lab-01-messenger.md` end to end — it's the canonical example of the template.
2. Read `lab-42-life-the-universe-and-everything.md` end to end — it's the philosophical anchor of the program.
3. Pick a track from the list above (or run the `TRACK_PICKER`).
4. Open the first lab in your chosen track. Open an empty repo. Begin.

Don't Panic.

42.
