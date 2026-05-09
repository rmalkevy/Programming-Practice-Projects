# Track Picker — Find Your 4–6 Labs

> "If you don't know where you're going, any road will get you there."
> — paraphrased from Lewis Carroll
>
> "If you *do* know where you're going, the road is much shorter."
> — paraphrased from every senior engineer ever

This is a decision tree. Read top-down. Answer each question. The leaves are **suggested 4–6-lab tracks** drawn from the 42-lab program, ending (almost always) with **Lab 42** as your capstone.

Doing more than one track is welcome. Mixing two adjacent tracks is welcome. Blowing past 6 labs into the whole program is *more* than welcome.

If you have *no idea* what to pick, jump straight to **Track Z — The Hitchhiker's Path** at the bottom. It is the official "I don't know" answer.

---

## Question 1 — Why are you here?

- **(A)** *I want a job in 12 months.* → go to **Question 2**.
- **(B)** *I want to be the kind of programmer who can build anything.* → go to **Question 3**.
- **(C)** *I want to do this for fun and curiosity.* → go to **Question 4**.
- **(D)** *I'm not sure.* → go to **Track Z** at the bottom. Don't Panic.

---

## Question 2 — *Job in 12 months* — what does that job look like?

- **(2a)** *Defense / aerospace / drone / aviation in Ukraine* → **Track A — Defense / Aerospace / Drones.**
- **(2b)** *Web full-stack at a startup or product company* → **Track C — Full-Stack Engineer.**
- **(2c)** *Mobile (Android / iOS / cross-platform)* → **Track G — Mobile Developer.**
- **(2d)** *AI / ML engineer / applied research* → **Track B — AI / ML.**
- **(2e)** *Game studio (small indie or AAA)* → **Track D — Game Developer.**
- **(2f)** *Cybersecurity / red team / blue team / AppSec* → **Track F — Security Engineer.**
- **(2g)** *Embedded / firmware / robotics* → **Track E — Embedded / Systems.**
- **(2h)** *Anything that pays, I just want out of "junior"* → **Track C** (full-stack employs the most juniors), with two extension labs from **Track F**.

---

## Question 3 — *Build anything* — which kind of "anything" excites you most?

- **(3a)** *Things that move in the physical world* → **Track E — Embedded / Systems.**
- **(3b)** *Things that look beautiful on a screen* → **Track H — Math / Graphics / Simulation.**
- **(3c)** *Things millions of people might use* → **Track C — Full-Stack Engineer**, then add **Lab 24 (browser extension)** as a side project for product flavor.
- **(3d)** *Things that think* → **Track B — AI / ML.**
- **(3e)** *Things that fly* → **Track A — Defense / Aerospace / Drones.**
- **(3f)** *All of the above and I refuse to choose* → **Track Z — The Hitchhiker's Path.**

---

## Question 4 — *Fun and curiosity* — what's the texture of "fun" for you?

- **(4a)** *I love mathematics; I want to feel it as a superpower* → **Track H — Math / Graphics / Simulation.**
- **(4b)** *I love games and want to make my own* → **Track D — Game Developer.**
- **(4c)** *I love taking things apart to see how they work* → **Track F — Security Engineer.**
- **(4d)** *I love making physical things blink, move, beep, and behave* → **Track E — Embedded / Systems.**
- **(4e)** *I love teaching, explaining, and writing* → **Track Z — The Hitchhiker's Path** + Lab 42 in the *Path B (The Question)* mode.

---

## The tracks

Each track is a 4–6-lab path. They all end in Lab 42 unless explicitly noted. *Don't skip Lab 42 — it is the program.*

### Track A — Defense / Aerospace / Drones (Ukrainian-flagship)

**04 → 17 → 35 → 37 → 40 → 42**

- 04 Embedded Sensor Logger — *first firmware*.
- 17 PID Self-Balancing Robot — *first control loop*.
- 35 RTOS Mini-Autopilot — *first real-time system*.
- 37 PX4 + MAVLink + ROS 2 Drone Stack — *first autonomous mission*.
- 40 Network / Wireless / Drone-Link Security — *first secured link*.
- 42 Capstone — fuse 35 + 37 + 40 into one secure autonomous-drone reference (popular Lab 42 outcome).

*Add 41 Orbital Mechanics for satellite-flavored extension.*
*Add 33 Object Detection for vision-guidance extension.*

**Why this track in Ukraine:** Firefly Aerospace, Promin Aerospace, Skyrora, Yuzhmash heritage, dual-use defense industry — the most direct hire path that exists right now.

---

### Track B — AI / ML

**31 → 32 → 33 → 34 → 42**

- 31 LLM RAG App — *first deployed AI product*.
- 32 Neural Net From Scratch (Karpathy-style) — *first time you understand what's inside the framework*.
- 33 Object Detection And Tracking — *first vision system*.
- 34 AI Capstone — *first portfolio-grade AI artifact*.
- 42 Capstone — usually a multimodal or production-flavored synthesis of 31 + 33 + 34.

*Add 22 SPA for the deployable UI layer.*
*Add 23 Realtime if streaming inference matters.*
*Add 41 Orbital Mechanics + RL controller for a uniquely-yours capstone.*

**Why this track:** AI hiring is currently the highest-paid junior pipeline in software, full stop. *And* the local market is hungry for engineers who can ship inference, not just talk about prompts.

---

### Track C — Full-Stack Engineer

**12 → 21 → 22 → 23 → 20 → 42**

- 12 Task Tracker — *the friendliest first product*.
- 21 REST API With Auth — *first real backend*.
- 22 SPA Frontend — *first real frontend*.
- 23 Real-Time Multiplayer Service — *first websocket/SSE service*.
- 20 Personal Portfolio — *deploy your own brand*.
- 42 Capstone — usually a small SaaS / civic-tech / community-tool.

*Add 24 Browser Extension for product breadth.*
*Add 39 OWASP for "I can both build and break web apps" credibility.*

**Why this track:** the single most-hired junior pipeline in software globally. Web companies will always be hiring.

---

### Track D — Game Developer

**09 → 10 → 25 → 26 → 27 → 28 → 42**

- 09 Console Paddle Game — *first game loop*.
- 10 Maze Generator and Solver — *first procedural content*.
- 25 Platformer Game — *first real engine work*.
- 26 Procedural Roguelike — *first deep procgen*.
- 27 Multiplayer Browser Game — *first multiplayer*.
- 28 Game Jam — *first shipped polished game with constraints*.
- 42 Capstone — usually the polished final game.

*Add 13 Physics Sandbox for game-physics depth.*
*Add 14 Cellular Automata for organic procgen.*

**Why this track:** game studios hire on portfolio, full stop. A polished demo on itch.io is more valuable than any degree.

---

### Track E — Embedded / Systems Programmer

**04 → 16 → 19 → 35 → 36 → 42**

- 04 Embedded Sensor Logger — *first firmware*.
- 16 Smart Telemetry Beacon — *first network-connected device*.
- 19 Custom Game Controller — *first USB-HID protocol implementation*.
- 35 RTOS Mini-Autopilot — *first real-time system*.
- 36 Embedded Linux From The Inside — *first kernel module + custom distro*.
- 42 Capstone — typically a hardware product with companion app, or a hardened firmware platform.

*Add 38 Binary Exploitation for the systems-security angle.*
*Add 17 PID Self-Balancing Robot for the controls angle.*

**Why this track:** the Ukrainian and global defense / IoT / automotive industries are perpetually short of firmware engineers. This is one of the highest-leverage tracks in the program.

---

### Track F — Security Engineer

**21 → 38 → 39 → 40 → 42**

- 21 REST API With Auth — *build your own thing first; the rest is pen-testing your own work*.
- 38 Smash The Stack — *first memory-corruption exploit*.
- 39 OWASP Top 10 — *first web pen-test*.
- 40 Network / Wireless / Drone-Link Security — *first network-level security*.
- 42 Capstone — typically a small open-source security tool, a CVE-style writeup, or a hardened reference platform.

*Add 36 Embedded Linux for kernel-module exploitation extension.*
*Add 35 RTOS for embedded vulnerability-research extension.*

**Why this track:** AppSec / DevSecOps / red team / blue team are all currently understaffed; CTF / bug-bounty profiles are *uniquely portable* to any country.

**⚠ Read the security labs' opening ethics blocks before starting.**

---

### Track G — Mobile Developer

**20 → 22 → 29 → 30 → 42**

- 20 Personal Portfolio — *first deployed thing*.
- 22 SPA Frontend — *first reactive UI*.
- 29 Android Native App — *first Android app*.
- 30 Cross-Platform App (React Native) — *first cross-platform app*.
- 42 Capstone — typically shipped as a sideloadable APK or a published cross-platform app.

*Add 31 LLM RAG for AI-flavored mobile features.*
*Add 16 Telemetry Beacon for IoT-companion-app extension.*

**Why this track:** mobile shippers are perennially hireable and the App Store / Play Store are public credibility tokens.

---

### Track H — Math / Graphics / Simulation

**02 → 03 → 08 → 13 → 14 → 41 → 42**

- 02 Wolfenstein-like Ray Casting Engine — *first 3D-style render*.
- 03 Simple Ray Tracer — *first real lighting math*.
- 08 Fractal Generator — *first iterative-math beauty*.
- 13 Physics Sandbox — *first physics engine*.
- 14 Cellular Automata — *first emergent-behavior sim*.
- 41 Mostly Harmless Orbital Mechanics — *first interplanetary mission planner*.
- 42 Capstone — typically a "math made beautiful" interactive visualizer or simulator.

*Add 32 NN From Scratch for the gradient-math angle.*
*Add 25 / 26 Game Dev for game-engine-style synthesis.*

**Why this track:** the "math-into-pixels" path produces the most visually-striking portfolios in the program. Recruiters in graphics, ML, simulation, and aerospace open these portfolios twice.

---

### Track Z — The Hitchhiker's Path

> "If you've nothing else to do, you might as well try and find one of those things, the Earth, you know, while there's still — well, isn't a — well, while there's still a — well, while there's still — well, well, well —" said Slartibartfast.
> — *Hitchhiker's Guide*

**01 → 03 → 13 → 31 → 41 → 42**

For the student who has no domain preference, no clear job-target, and just wants the *spirit* of the program: a guided tour from "first shipped thing" to "Mostly Harmless" to "Life, the Universe, and Everything."

- 01 Mini Messenger — your first end-to-end shipped thing.
- 03 Simple Ray Tracer — your first taste of math-as-superpower.
- 13 Physics Sandbox — your first simulation.
- 31 LLM RAG App — your first AI product.
- 41 Mostly Harmless Orbital Mechanics — your first mission to Mars.
- 42 Life, The Universe, And Everything — your answer.

*This track explicitly hands you a tour of five different domains and trusts you to discover which one you love. Lab 42 then asks you to act on what you discovered.*

**Don't Panic.** Pick this if you're stuck. It's the program's official answer to *"I don't know."*

---

## Two-track combinations (when 6 labs feel too few)

Some students finish a 6-lab track in 4–5 months and want more. Recommended *bridges* between tracks:

- **A + E (Defense + Embedded):** identical first three labs (04, 17, 35); then choose 36 (Track E) or 37 (Track A) as the 4th.
- **B + C (AI + Full-Stack):** add 22 SPA between 31 and 32 in Track B for a deployed-AI-product flavor.
- **B + H (AI + Graphics):** 32 NN From Scratch slots beautifully into Track H between 13 and 14.
- **C + F (Web + Security):** 21 REST API does double duty as the start of both tracks.
- **D + H (Games + Graphics):** 13 Physics + 25 Platformer + 26 Roguelike share procgen / physics DNA.
- **E + F (Embedded + Security):** 35 + 38 + 36 makes you uniquely employable in firmware-security niches.

---

## How to actually use this

1. Read this document end-to-end (~10 minutes).
2. Pick a track. Write it down somewhere visible.
3. Open `labs/lab-NN-...md` for the first lab in that track.
4. Don't switch tracks for at least 2 labs. (Track-hopping is the #1 way students fail to ship.)
5. After lab 2, you may swap *one* lab in your track if you've discovered you don't love it. Do this *once*.
6. After lab 4, freeze the track. Finish the rest.
7. Lab 42 is non-negotiable. Plan it. Ship it. Defend it.

---

## A small reminder

The tracks are guides, not prisons. The 42-lab program was written so that *any* combination of 4–6 labs makes a coherent portfolio if the student writes good READMEs and ships honestly. The tracks just save you the energy of choosing.

If by Lab 42 you've discovered a sixth domain you want to explore — write the next 41 labs yourself. *That* would be the highest compliment the program could ever receive.

Don't Panic.

42.
