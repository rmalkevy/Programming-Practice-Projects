# Instructor Handbook — The 42-Lab Program

> "I refuse to prove that I exist," says God, "for proof denies faith, and without faith I am nothing."
> — *The Hitchhiker's Guide to the Galaxy*

> "I refuse to grade by exam," says the instructor, "for exams deny shipping, and without shipping the program is nothing."
> — every effective programming-school instructor, paraphrased

This handbook is for instructors, mentors, and TAs running the 42-lab program. It assumes you've read at least two labs end-to-end (recommended: `labs/lab-01-messenger.md` and `labs/lab-42-life-the-universe-and-everything.md`).

The program was designed for **first-year aviation-institute students in Ukraine, ~2026**, but adapts cleanly to any first- or second-year CS/SE/aerospace cohort.

---

## 1. Philosophy in one paragraph

The program rejects the textbook "exercise → quiz → exam" loop. It replaces it with a **shipping loop**: every two to three weeks, the student turns an empty repo into a runnable, documentable, defensible artifact. Across one academic year, this produces ~15–18 portfolio-grade projects per student. By Lab 42, the student has a public GitHub that any junior recruiter would happily open. Grades are secondary to artifacts.

If you remember nothing else: **shipping > grading.**

---

## 2. The student we're building

The student we're building, by the end of the program, is one who:

- ships every two weeks without being told,
- can read a packet, an assembly listing, and a learning-rate schedule,
- writes a clean README without prompting,
- defends architectural choices in plain language,
- knows the difference between *I read about X* and *I built X*,
- and has at least one project at the top of their GitHub that *they care about*.

If a student finishes the program with all six of those traits, the program succeeded — regardless of grades.

---

## 3. Pacing recipes

### 3.1 The classic year (recommended)
**~16 labs across 32 weeks (one per fortnight).**
- Fall semester: 8 labs from a coherent track (e.g., Track A or C).
- Spring semester: 6 labs broadening domain coverage + 2 weeks for Lab 42.
- Lab 42 is always the closer.

### 3.2 The intensive summer (École 42 spirit)
**~6 labs across 10 weeks** during a summer intensive.
- Pick one track, work in pairs / trios, daily standups, weekly demos.
- Closing week is Lab 42, defended at a public showcase.
- Incredibly productive, exhausting, transformative; not for everyone.

### 3.3 The four-lab semester (light-touch elective)
**4 labs across 14 weeks.**
- Use this as a one-semester elective.
- Pick from the *Make it yours* sections aggressively; let students self-direct.
- Skip Lab 42 unless you can give them at least 3 weeks at the end.

### 3.4 The self-paced track
**Solo, no instructor.**
- Refer student to `TRACK_PICKER.md`.
- Suggest one mentor (any senior they know) for the defense step.
- Make `MANIFESTO.md` (Lab 42) the exit ticket.

---

## 4. Time budgets and the Extension-Challenge dial

Every lab is **2 weeks** by default (3 for the more ambitious labs in the 16–42 range). Each lab also has an explicit *Extension Challenges* section that bumps it to **3–5 weeks**.

| Default | Extension dial |
|---|---|
| Lab 01–15 | 2 weeks → up to 4 weeks with extensions |
| Lab 16–34 | 2–3 weeks → up to 5 weeks |
| Lab 35–41 | 3 weeks → up to 5 weeks |
| Lab 42 | 3 weeks → up to a summer |

Practical rule: if a student is ahead, **don't add more labs — extend the current one.** Depth beats breadth in this program.

---

## 5. Solo / pair / team rules

- Default is **solo**. Solo work is what most labs assume.
- Up to **3 students per team** is allowed.
- Teams must:
  1. Use **Git from day one**.
  2. Maintain a **who-did-what** section in the README.
  3. Be able to **demo and defend individually** — every team member explains *some* part of the project end-to-end.
- Teams of 4+ are not permitted in this program. They produce silent-passenger problems.
- Solo students can pair-review each other's labs voluntarily; *encourage this loudly.*

For Lab 42 specifically: teams *may* exist, but the *Manifesto* must be defended by each member individually for their portion.

---

## 6. Grading philosophy

**Hard recommendation: stop grading on points. Grade on artifacts.**

Use a three-tier rubric matching the lab's own *Levels* section:

- **Basic (passing):** the lab's Basic acceptance criteria are met. Submission/Deployment checklist is fully checked. README is present.
- **Standard (target):** Standard acceptance criteria met. At least one *Extension Challenge* attempted. Reflection answered cleanly during defense.
- **Advanced (distinction):** Standard plus at least one *Side Quest*. Public deployment / publishable writeup / cross-lab integration.

Map to whatever institutional system you're forced to use:

| Tier | 5-point | 100-point | ECTS |
|---|---|---|---|
| Basic | 3 | 60–74 | C |
| Standard | 4 | 75–89 | B |
| Advanced | 5 | 90–100 | A |

Reject "incomplete" submissions; require students to ship the Basic tier or ask for a one-week extension. **Lateness with a working artifact > on-time without one.**

For Lab 42, grading is binary: **shipped** (passing) / **not shipped** (not passing) — but the showcase peer-vote selects winners in three categories (clearest Question, most beautiful Answer, most ambitious shipped artifact).

---

## 7. The Defense (every lab, every student)

Each lab has a *Reflection* section with 6–8 questions. Use them. The defense is not an exam; it is a five-minute conversation:

- 60 seconds: live demo.
- 2 minutes: walk through one architectural decision and the trade-offs.
- 90 seconds: instructor picks 1–2 reflection questions.
- 30 seconds: "what would you do differently?"

Keep it conversational. Cynicism kills the program; respect builds it.

If a defense fails, the *common* failure mode is "the student shipped, but cannot explain why." Schedule a 30-minute office-hour follow-up rather than failing the lab.

---

## 8. Showcase nights (every 4–6 weeks)

**The single most important institutional ritual in the program.**

Run a **gallery showcase** every 4–6 weeks (or once per semester at minimum). Logistics:

- Long tables, one project per laptop.
- Anonymous peer voting in 3 categories (varies per night, e.g., *most beautiful UI*, *most clever algorithm*, *biggest ambition*).
- Invite **alumni, hiring managers, parents, friends-of-the-program**.
- Provide coffee. *This is non-negotiable.* Coffee dramatically increases interaction quality.
- 5-minute "lightning talks" optional but encouraged.
- Photograph everything; post a public gallery album to the course website with student permission.

The showcase is where:
- recruiters find students,
- juniors meet seniors,
- parents see what their kids built (especially impactful in Ukraine),
- and the program's culture becomes visible.

Skip showcases at your peril. They are 80% of the program's institutional memory.

---

## 9. Recommended hardware budget

The program is mostly software; hardware is optional in *every* lab. But these one-time purchases per cohort are recommended:

| Item | Approx. UAH (2026) | Use |
|---|---|---|
| 5× Raspberry Pi Pico (RP2040) | ~1500 UAH | Labs 04, 19 |
| 5× ESP32 dev boards | ~2000 UAH | Labs 04, 16, 18 |
| 3× IMU breakouts (MPU-6050) | ~500 UAH | Lab 17 |
| 3× DHT22 sensors | ~600 UAH | Lab 04, 18 |
| 2× USB-to-serial adapters | ~600 UAH | Labs 04, 36 |
| 2× SD-card readers | ~500 UAH | Lab 36 |
| 1× Alfa AWUS036NHA Wi-Fi adapter | ~1500 UAH | Lab 40 |
| 1× RTL-SDR dongle | ~1000 UAH | Lab 40 (optional) |
| 1× cheap travel router (TP-Link) | ~700 UAH | Lab 40 |

Total: ~9,000 UAH (~$220) per cohort if shared. Many institutes can absorb this. If not, every lab supports a "simulator-only" path explicitly.

For aviation-institute deployments specifically: the existing PCB / hand-tools / soldering benches usually cover Labs 04, 16–19, 35.

---

## 10. Software stack (cohort-wide)

**Encourage but don't enforce.** Standardizing helps grading; over-standardizing kills curiosity.

- **Editor**: VS Code or any. Cursor is fine. Vim/Emacs welcome.
- **VCS**: Git, GitHub. *Mandatory*. Set up a class GitHub Classroom (free).
- **Languages**: Python, TypeScript / JavaScript, C, C++, Rust, C#. Allow any; tactically nudge toward Python for AI labs and TypeScript for web labs.
- **Cloud**: Vercel / Netlify / Render / Fly.io / Hugging Face Spaces. All free tiers.
- **CI**: GitHub Actions. *One workflow per repo, minimum.*

---

## 11. Common failure modes (and how to handle them)

### *"I'm stuck and didn't ask for help."*
Solution: institute a **30-minute rule** — if blocked for 30 minutes, post in the class channel. No shame. *Quietly stuck students are the program's silent killer.*

### *"I rewrote it three times and shipped nothing."*
Solution: enforce vertical-slice-by-Day-X (per the lab's own day plan). Better an ugly working thing than a beautiful unbuilt one.

### *"I copied a tutorial."*
Solution: required *Make it yours* defense — student must walk through the personal twist for 60 seconds. Tutorial-copying becomes obvious immediately.

### *"I let my teammate carry me."*
Solution: required who-did-what + individual defense. Silent passengers don't survive Lab 42.

### *"AI wrote my code."*
Solution: this is fine. *Defending it is what matters.* If the student can't walk through their own code line-by-line in defense, the lab fails — regardless of who or what wrote the code. Keep this position consistent and gentle; LLMs are tools, demonstrated understanding is the bar.

### *"I lost interest."*
Solution: revisit *Make it yours.* If a student is bored, it's almost always because they failed to take the *make it yours* prompt seriously. Walk them through three personal twists; let them pick.

---

## 12. Required "ethics labs"

Labs **38, 39, 40** are security labs and require a stricter posture:

1. Read the **`⚠ Read this first`** block in each before assigning.
2. Confirm the institution has a **sandbox VM policy** that allows the work.
3. Add a **mandatory ethics quiz** before the student begins (10 questions; take from the labs' opening sections).
4. Make `ETHICS.md` a non-negotiable submission requirement.
5. **Forbid** any work against real-world targets, the institute's infrastructure, or production systems.
6. **Forbid** any RF transmission without an amateur-radio license.
7. **Forbid** any operation against real aircraft / drones outside PX4 SITL.

If your institution can't provide a sandbox VM policy, *swap these three labs for an alternative track.* (Track B or H both work as substitutes.)

---

## 13. Recommended cadence (weekly)

| Weekday | What |
|---|---|
| Monday | Kickoff: lab #N briefing, 30-min Q&A, students start |
| Mid-week | Optional drop-in office hours (60 min) |
| Friday | Mid-lab checkpoint — vertical-slice demos, 5 min each |
| Following Monday | Defense + retro |

Recommend students batch their *deep work* in the second half of the lab cycle and use the first half for reading + design + spike experiments. (This matches the labs' own day plans.)

---

## 14. The instructor's defense

Every two semesters, the instructor should themselves attempt one lab they didn't write. Yes, **you, the instructor.** It will:

1. Recalibrate your sense of how long the labs *actually* take in 2026.
2. Surface dated tooling assumptions.
3. Rebuild empathy for students.
4. Give you a defensive answer when students ask "have *you* ever done this?"

This is not a soft suggestion. It's the program's accountability mechanism for instructors.

---

## 15. Updating this program

The program is text. Update it. Pull-request culture is encouraged — students who complete a lab and notice an outdated tool, broken link, or unclear sentence should send a PR. Their PR becomes part of their portfolio. *This is how the program stays alive across decades.*

For substantive changes (adding labs, removing labs, restructuring tracks), maintain a changelog in `CHANGELOG.md` at the repo root.

---

## 16. Final notes for the instructor

- Be **boring and consistent.** Show up on time. Read every README. Reply within 24 hours. *Reliability is the most underrated teaching virtue.*
- Be **publicly proud** of student work. Tweet, post, share — with permission.
- Be **harsh on dishonesty, gentle on slowness.** They're different; they need different responses.
- Take **one student each cohort under deeper mentorship.** Pick the one whose curiosity you most want to amplify; offer them an extension lab pairing or co-author a small paper. This is how alumni networks begin.
- Read **`labs/lab-42-life-the-universe-and-everything.md`** at the start of every cohort. It is the program's emotional anchor — it will tell you what to remind yourself when the term gets hard.
- And: **buy good coffee for the showcase.** Always.

42.
