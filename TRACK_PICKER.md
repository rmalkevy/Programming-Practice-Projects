# Track Picker — Find Your 4–6 Labs

> "If you don't know where you're going, any road will get you there."
> — paraphrased from Lewis Carroll
>
> "If you *do* know where you're going, the road is much shorter."
> — paraphrased from every senior engineer ever

This is a decision tree. Read top-down. Answer each question. The leaves are **suggested 4–6-lab tracks** drawn from the 42-lab program, ending (almost always) with [**Lab 42**](labs/lab-42-life-the-universe-and-everything.md) as your capstone.

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
- **(3c)** *Things millions of people might use* → **Track C — Full-Stack Engineer**, then add [**Lab 24 (browser extension)**](labs/lab-24-browser-extension.md) as a side project for product flavor.
- **(3d)** *Things that think* → **Track B — AI / ML.**
- **(3e)** *Things that fly* → **Track A — Defense / Aerospace / Drones.**
- **(3f)** *All of the above and I refuse to choose* → **Track Z — The Hitchhiker's Path.**

---

## Question 4 — *Fun and curiosity* — what's the texture of "fun" for you?

- **(4a)** *I love mathematics; I want to feel it as a superpower* → **Track H — Math / Graphics / Simulation.**
- **(4b)** *I love games and want to make my own* → **Track D — Game Developer.**
- **(4c)** *I love taking things apart to see how they work* → **Track F — Security Engineer.**
- **(4d)** *I love making physical things blink, move, beep, and behave* → **Track E — Embedded / Systems.**
- **(4e)** *I love teaching, explaining, and writing* → **Track Z — The Hitchhiker's Path** + [Lab 42](labs/lab-42-life-the-universe-and-everything.md) in the *Path B (The Question)* mode.

---

## The tracks

Each track is a 4–6-lab path. They all end in [Lab 42](labs/lab-42-life-the-universe-and-everything.md) unless explicitly noted. *Don't skip [Lab 42](labs/lab-42-life-the-universe-and-everything.md) — it is the program.*

### Track A — Defense / Aerospace / Drones (Ukrainian-flagship)

[**04**](labs/lab-04-stm32-sensor-logger.md) → [**17**](labs/lab-17-pid-self-balancer.md) → [**35**](labs/lab-35-rtos-mini-autopilot.md) → [**37**](labs/lab-37-px4-mavlink-drone-stack.md) → [**40**](labs/lab-40-network-wireless-drone-security.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [04 Embedded Sensor Logger](labs/lab-04-stm32-sensor-logger.md) — *first firmware*.
- [17 PID Self-Balancing Robot](labs/lab-17-pid-self-balancer.md) — *first control loop*.
- [35 RTOS Mini-Autopilot](labs/lab-35-rtos-mini-autopilot.md) — *first real-time system*.
- [37 PX4 + MAVLink + ROS 2 Drone Stack](labs/lab-37-px4-mavlink-drone-stack.md) — *first autonomous mission*.
- [40 Network / Wireless / Drone-Link Security](labs/lab-40-network-wireless-drone-security.md) — *first secured link*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — fuse [35](labs/lab-35-rtos-mini-autopilot.md) + [37](labs/lab-37-px4-mavlink-drone-stack.md) + [40](labs/lab-40-network-wireless-drone-security.md) into one secure autonomous-drone reference (popular Lab 42 outcome).

*Add [41 Orbital Mechanics](labs/lab-41-mostly-harmless-orbital-mechanics.md) for satellite-flavored extension.*
*Add [33 Object Detection](labs/lab-33-object-detection-tracking.md) for vision-guidance extension.*

**Why this track in Ukraine:** Firefly Aerospace, Promin Aerospace, Skyrora, Yuzhmash heritage, dual-use defense industry — the most direct hire path that exists right now.

---

### Track B — AI / ML

[**31**](labs/lab-31-llm-rag-app.md) → [**32**](labs/lab-32-neural-net-from-scratch.md) → [**33**](labs/lab-33-object-detection-tracking.md) → [**34**](labs/lab-34-ai-capstone.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [31 LLM RAG App](labs/lab-31-llm-rag-app.md) — *first deployed AI product*.
- [32 Neural Net From Scratch (Karpathy-style)](labs/lab-32-neural-net-from-scratch.md) — *first time you understand what's inside the framework*.
- [33 Object Detection And Tracking](labs/lab-33-object-detection-tracking.md) — *first vision system*.
- [34 AI Capstone](labs/lab-34-ai-capstone.md) — *first portfolio-grade AI artifact*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — usually a multimodal or production-flavored synthesis of [31](labs/lab-31-llm-rag-app.md) + [33](labs/lab-33-object-detection-tracking.md) + [34](labs/lab-34-ai-capstone.md).

*Add [22 SPA](labs/lab-22-spa-frontend.md) for the deployable UI layer.*
*Add [23 Realtime](labs/lab-23-realtime-multiplayer.md) if streaming inference matters.*
*Add [41 Orbital Mechanics](labs/lab-41-mostly-harmless-orbital-mechanics.md) + RL controller for a uniquely-yours capstone.*

**Why this track:** AI hiring is currently the highest-paid junior pipeline in software, full stop. *And* the local market is hungry for engineers who can ship inference, not just talk about prompts.

---

### Track C — Full-Stack Engineer

[**12**](labs/lab-12-task-tracker.md) → [**21**](labs/lab-21-rest-api-auth.md) → [**22**](labs/lab-22-spa-frontend.md) → [**23**](labs/lab-23-realtime-multiplayer.md) → [**20**](labs/lab-20-personal-portfolio.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [12 Task Tracker](labs/lab-12-task-tracker.md) — *the friendliest first product*.
- [21 REST API With Auth](labs/lab-21-rest-api-auth.md) — *first real backend*.
- [22 SPA Frontend](labs/lab-22-spa-frontend.md) — *first real frontend*.
- [23 Real-Time Multiplayer Service](labs/lab-23-realtime-multiplayer.md) — *first websocket/SSE service*.
- [20 Personal Portfolio](labs/lab-20-personal-portfolio.md) — *deploy your own brand*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — usually a small SaaS / civic-tech / community-tool.

*Add [24 Browser Extension](labs/lab-24-browser-extension.md) for product breadth.*
*Add [39 OWASP](labs/lab-39-web-security-owasp.md) for "I can both build and break web apps" credibility.*

**Why this track:** the single most-hired junior pipeline in software globally. Web companies will always be hiring.

---

### Track D — Game Developer

[**09**](labs/lab-09-console-paddle-game.md) → [**10**](labs/lab-10-maze-generator-solver.md) → [**25**](labs/lab-25-platformer-game.md) → [**26**](labs/lab-26-procedural-roguelike.md) → [**27**](labs/lab-27-multiplayer-browser-game.md) → [**28**](labs/lab-28-game-jam.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [09 Console Paddle Game](labs/lab-09-console-paddle-game.md) — *first game loop*.
- [10 Maze Generator and Solver](labs/lab-10-maze-generator-solver.md) — *first procedural content*.
- [25 Platformer Game](labs/lab-25-platformer-game.md) — *first real engine work*.
- [26 Procedural Roguelike](labs/lab-26-procedural-roguelike.md) — *first deep procgen*.
- [27 Multiplayer Browser Game](labs/lab-27-multiplayer-browser-game.md) — *first multiplayer*.
- [28 Game Jam](labs/lab-28-game-jam.md) — *first shipped polished game with constraints*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — usually the polished final game.

*Add [13 Physics Sandbox](labs/lab-13-physics-sandbox.md) for game-physics depth.*
*Add [14 Cellular Automata](labs/lab-14-cellular-automata.md) for organic procgen.*

**Why this track:** game studios hire on portfolio, full stop. A polished demo on itch.io is more valuable than any degree.

---

### Track E — Embedded / Systems Programmer

[**04**](labs/lab-04-stm32-sensor-logger.md) → [**16**](labs/lab-16-smart-telemetry-beacon.md) → [**19**](labs/lab-19-custom-game-controller.md) → [**35**](labs/lab-35-rtos-mini-autopilot.md) → [**36**](labs/lab-36-embedded-linux-from-inside.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [04 Embedded Sensor Logger](labs/lab-04-stm32-sensor-logger.md) — *first firmware*.
- [16 Smart Telemetry Beacon](labs/lab-16-smart-telemetry-beacon.md) — *first network-connected device*.
- [19 Custom Game Controller](labs/lab-19-custom-game-controller.md) — *first USB-HID protocol implementation*.
- [35 RTOS Mini-Autopilot](labs/lab-35-rtos-mini-autopilot.md) — *first real-time system*.
- [36 Embedded Linux From The Inside](labs/lab-36-embedded-linux-from-inside.md) — *first kernel module + custom distro*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — typically a hardware product with companion app, or a hardened firmware platform.

*Add [38 Binary Exploitation](labs/lab-38-binary-exploitation.md) for the systems-security angle.*
*Add [17 PID Self-Balancing Robot](labs/lab-17-pid-self-balancer.md) for the controls angle.*

**Why this track:** the Ukrainian and global defense / IoT / automotive industries are perpetually short of firmware engineers. This is one of the highest-leverage tracks in the program.

---

### Track F — Security Engineer

[**21**](labs/lab-21-rest-api-auth.md) → [**38**](labs/lab-38-binary-exploitation.md) → [**39**](labs/lab-39-web-security-owasp.md) → [**40**](labs/lab-40-network-wireless-drone-security.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [21 REST API With Auth](labs/lab-21-rest-api-auth.md) — *build your own thing first; the rest is pen-testing your own work*.
- [38 Smash The Stack](labs/lab-38-binary-exploitation.md) — *first memory-corruption exploit*.
- [39 OWASP Top 10](labs/lab-39-web-security-owasp.md) — *first web pen-test*.
- [40 Network / Wireless / Drone-Link Security](labs/lab-40-network-wireless-drone-security.md) — *first network-level security*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — typically a small open-source security tool, a CVE-style writeup, or a hardened reference platform.

*Add [36 Embedded Linux](labs/lab-36-embedded-linux-from-inside.md) for kernel-module exploitation extension.*
*Add [35 RTOS](labs/lab-35-rtos-mini-autopilot.md) for embedded vulnerability-research extension.*

**Why this track:** AppSec / DevSecOps / red team / blue team are all currently understaffed; CTF / bug-bounty profiles are *uniquely portable* to any country.

**⚠ Read the security labs' opening ethics blocks before starting.**

---

### Track G — Mobile Developer

[**20**](labs/lab-20-personal-portfolio.md) → [**22**](labs/lab-22-spa-frontend.md) → [**29**](labs/lab-29-android-native-app.md) → [**30**](labs/lab-30-cross-platform-app.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [20 Personal Portfolio](labs/lab-20-personal-portfolio.md) — *first deployed thing*.
- [22 SPA Frontend](labs/lab-22-spa-frontend.md) — *first reactive UI*.
- [29 Android Native App](labs/lab-29-android-native-app.md) — *first Android app*.
- [30 Cross-Platform App (React Native)](labs/lab-30-cross-platform-app.md) — *first cross-platform app*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — typically shipped as a sideloadable APK or a published cross-platform app.

*Add [31 LLM RAG](labs/lab-31-llm-rag-app.md) for AI-flavored mobile features.*
*Add [16 Telemetry Beacon](labs/lab-16-smart-telemetry-beacon.md) for IoT-companion-app extension.*

**Why this track:** mobile shippers are perennially hireable and the App Store / Play Store are public credibility tokens.

---

### Track H — Math / Graphics / Simulation

[**02**](labs/lab-02-ray-casting-engine.md) → [**03**](labs/lab-03-ray-tracer.md) → [**08**](labs/lab-08-fractal-generator.md) → [**13**](labs/lab-13-physics-sandbox.md) → [**14**](labs/lab-14-cellular-automata.md) → [**41**](labs/lab-41-mostly-harmless-orbital-mechanics.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

- [02 Wolfenstein-like Ray Casting Engine](labs/lab-02-ray-casting-engine.md) — *first 3D-style render*.
- [03 Simple Ray Tracer](labs/lab-03-ray-tracer.md) — *first real lighting math*.
- [08 Fractal Generator](labs/lab-08-fractal-generator.md) — *first iterative-math beauty*.
- [13 Physics Sandbox](labs/lab-13-physics-sandbox.md) — *first physics engine*.
- [14 Cellular Automata](labs/lab-14-cellular-automata.md) — *first emergent-behavior sim*.
- [41 Mostly Harmless Orbital Mechanics](labs/lab-41-mostly-harmless-orbital-mechanics.md) — *first interplanetary mission planner*.
- [42 Capstone](labs/lab-42-life-the-universe-and-everything.md) — typically a "math made beautiful" interactive visualizer or simulator.

*Add [32 NN From Scratch](labs/lab-32-neural-net-from-scratch.md) for the gradient-math angle.*
*Add [25](labs/lab-25-platformer-game.md) / [26](labs/lab-26-procedural-roguelike.md) Game Dev for game-engine-style synthesis.*

**Why this track:** the "math-into-pixels" path produces the most visually-striking portfolios in the program. Recruiters in graphics, ML, simulation, and aerospace open these portfolios twice.

---

### Track Z — The Hitchhiker's Path

> "If you've nothing else to do, you might as well try and find one of those things, the Earth, you know, while there's still — well, isn't a — well, while there's still a — well, while there's still — well, well, well —" said Slartibartfast.
> — *Hitchhiker's Guide*

[**01**](labs/lab-01-messenger.md) → [**03**](labs/lab-03-ray-tracer.md) → [**13**](labs/lab-13-physics-sandbox.md) → [**31**](labs/lab-31-llm-rag-app.md) → [**41**](labs/lab-41-mostly-harmless-orbital-mechanics.md) → [**42**](labs/lab-42-life-the-universe-and-everything.md)

For the student who has no domain preference, no clear job-target, and just wants the *spirit* of the program: a guided tour from "first shipped thing" to "Mostly Harmless" to "Life, the Universe, and Everything."

- [01 Mini Messenger](labs/lab-01-messenger.md) — your first end-to-end shipped thing.
- [03 Simple Ray Tracer](labs/lab-03-ray-tracer.md) — your first taste of math-as-superpower.
- [13 Physics Sandbox](labs/lab-13-physics-sandbox.md) — your first simulation.
- [31 LLM RAG App](labs/lab-31-llm-rag-app.md) — your first AI product.
- [41 Mostly Harmless Orbital Mechanics](labs/lab-41-mostly-harmless-orbital-mechanics.md) — your first mission to Mars.
- [42 Life, The Universe, And Everything](labs/lab-42-life-the-universe-and-everything.md) — your answer.

*This track explicitly hands you a tour of five different domains and trusts you to discover which one you love. [Lab 42](labs/lab-42-life-the-universe-and-everything.md) then asks you to act on what you discovered.*

**Don't Panic.** Pick this if you're stuck. It's the program's official answer to *"I don't know."*

---

## Two-track combinations (when 6 labs feel too few)

Some students finish a 6-lab track in 4–5 months and want more. Recommended *bridges* between tracks:

- **A + E (Defense + Embedded):** identical first three labs ([04](labs/lab-04-stm32-sensor-logger.md), [17](labs/lab-17-pid-self-balancer.md), [35](labs/lab-35-rtos-mini-autopilot.md)); then choose [36](labs/lab-36-embedded-linux-from-inside.md) (Track E) or [37](labs/lab-37-px4-mavlink-drone-stack.md) (Track A) as the 4th.
- **B + C (AI + Full-Stack):** add [22 SPA](labs/lab-22-spa-frontend.md) between [31](labs/lab-31-llm-rag-app.md) and [32](labs/lab-32-neural-net-from-scratch.md) in Track B for a deployed-AI-product flavor.
- **B + H (AI + Graphics):** [32 NN From Scratch](labs/lab-32-neural-net-from-scratch.md) slots beautifully into Track H between [13](labs/lab-13-physics-sandbox.md) and [14](labs/lab-14-cellular-automata.md).
- **C + F (Web + Security):** [21 REST API](labs/lab-21-rest-api-auth.md) does double duty as the start of both tracks.
- **D + H (Games + Graphics):** [13 Physics](labs/lab-13-physics-sandbox.md) + [25 Platformer](labs/lab-25-platformer-game.md) + [26 Roguelike](labs/lab-26-procedural-roguelike.md) share procgen / physics DNA.
- **E + F (Embedded + Security):** [35](labs/lab-35-rtos-mini-autopilot.md) + [38](labs/lab-38-binary-exploitation.md) + [36](labs/lab-36-embedded-linux-from-inside.md) makes you uniquely employable in firmware-security niches.

---

## How to actually use this

1. Read this document end-to-end (~10 minutes).
2. Pick a track. Write it down somewhere visible.
3. Open `labs/lab-NN-...md` for the first lab in that track.
4. Don't switch tracks for at least 2 labs. (Track-hopping is the #1 way students fail to ship.)
5. After lab 2, you may swap *one* lab in your track if you've discovered you don't love it. Do this *once*.
6. After lab 4, freeze the track. Finish the rest.
7. [Lab 42](labs/lab-42-life-the-universe-and-everything.md) is non-negotiable. Plan it. Ship it. Defend it.

---

## A small reminder

The tracks are guides, not prisons. The 42-lab program was written so that *any* combination of 4–6 labs makes a coherent portfolio if the student writes good READMEs and ships honestly. The tracks just save you the energy of choosing.

If by [Lab 42](labs/lab-42-life-the-universe-and-everything.md) you've discovered a sixth domain you want to explore — write the next 41 labs yourself. *That* would be the highest compliment the program could ever receive.

Don't Panic.

42.
