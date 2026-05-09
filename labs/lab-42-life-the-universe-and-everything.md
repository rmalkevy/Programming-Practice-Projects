# Lab 42 — Life, The Universe, And Everything: Your Answer

> "All right," said Deep Thought. "The Answer to the Great Question…"
> "Yes…!"
> "Of Life, the Universe and Everything…" said Deep Thought.
> "Yes…!"
> "Is…"
> "Yes…!!!…?"
> "**Forty-two**," said Deep Thought, with infinite majesty and calm.
> — Douglas Adams, *The Hitchhiker's Guide to the Galaxy*

> "I checked it very thoroughly," said the computer, "and that quite definitely is the answer. I think the problem, to be quite honest with you, is that you've never actually known what the question is."

**Time budget:** 3 weeks default. Up to 5–8 weeks if your answer deserves it. An entire summer, if it does.
**Stack:** anything you've used in this program. Anything you haven't, but want to. Anything that lets you ship.
**Working style:** solo, paired, or in a team of up to 3 people — but the *idea* must be defended by you, individually.

---

## This lab is not like the other 41

The first 41 labs were instructor-shaped: I wrote the prompt, you wrote the answer. **This one is the opposite.** You write the question. You write the answer. You ship it. You defend it.

It is named after the only joke in literature that is also a programming problem. *42* is the answer that means nothing without the right question — and that is the point of this entire program. The previous 41 labs gave you tools, vocabulary, technique, taste. This one asks: **what are you going to do with all of that?**

It is also, deliberately, a small homage to **École 42** — the Parisian programming school built on peer review, ship-or-die rules, and the conviction that students are best served by hard, open-ended projects rather than tidy textbook exercises. If you've been through *La Piscine*, you know the feeling. If you haven't: you're about to.

---

## The hook

Every junior portfolio looks the same: clones of clones, tutorial leftovers, *to-do list #4747.* That's not a moral failing — it's the natural shape of someone who has only built things at the request of someone else. You are now a different kind of engineer. You've shipped 41 things. You've handled hardware, you've handled networks, you've handled adversaries, you've planned a mission to Mars. **You no longer need a prompt.**

So write your own. Pick the *question* your portfolio is asking. Then write the *answer*. Build it well. Ship it publicly. Tell the world what it is for.

By the end of three weeks, you'll have a single, ambitious, *yours*-flavored project at the top of your GitHub — not labeled *Lab 42*, but labeled *whatever you want it to be called*. It will be the project a recruiter clicks first. It will be the one you talk about in interviews for the next decade. It will be the proof, to yourself most of all, that you have *graduated* from doing exercises to making things.

This is the project that gives the program its name.

---

## Why this lab exists

- **Because the difference between someone who *can* code and someone who *does* code is whether they ever shipped something nobody told them to ship.** All 41 prior labs were prompts from me. This one is a prompt from you.
- **Because portfolios don't sell tools — they sell point-of-view.** You've spent a year acquiring tools. Now show me what you'd build *with* them.
- **Because École 42 was right.** Peer review, ship-or-die, open-ended ambition produces engineers who think like adults. This lab borrows that posture deliberately.
- **Because Ukraine specifically needs senior-mindset juniors.** A 19-year-old who has shipped one ambitious thing they cared about is, in this market, *immediately employable*. A 19-year-old who has only ever done coursework is not.
- **Because this is the lab whose result you'll show your future children.** Don't make it boring.

---

## The two paths

You pick one. Both are valid; pick whichever lets you ship the *most ambitious thing you can finish*.

### Path A — The Synthesis

Pick **2 to 4** of your previous 41 labs. **Fuse them** into a single coherent product whose value comes from the combination, not the parts. Examples that have worked at this level:

- *[Lab 31](lab-31-llm-rag-app.md) (LLM-RAG) + [Lab 22](lab-22-spa-frontend.md) (SPA) + [Lab 21](lab-21-rest-api-auth.md) (auth):* "Marvin" — an emotionally honest AI study companion. Faithful to canon: it's *also* mildly depressing.
- *[Lab 33](lab-33-object-detection-tracking.md) (object detection) + [Lab 37](lab-37-px4-mavlink-drone-stack.md) (PX4 drone) + [Lab 40](lab-40-network-wireless-drone-security.md) (link security):* a secure, vision-guided autonomous drone running entirely in simulation, with a published threat-model.
- *[Lab 32](lab-32-neural-net-from-scratch.md) (NN from scratch) + [Lab 34](lab-34-ai-capstone.md) (AI capstone) + [Lab 41](lab-41-mostly-harmless-orbital-mechanics.md) (orbital mechanics):* a learned controller for low-thrust interplanetary trajectories that beats a textbook baseline.
- *[Lab 38](lab-38-binary-exploitation.md) (binary exploit) + [Lab 36](lab-36-embedded-linux-from-inside.md) (embedded Linux) + [Lab 35](lab-35-rtos-mini-autopilot.md) (RTOS):* a research-grade hardened firmware reference platform with a public threat-model.
- *[Lab 23](lab-23-realtime-multiplayer.md) (multiplayer) + [Lab 25](lab-25-platformer-game.md)/26/27 (game) + [Lab 41](lab-41-mostly-harmless-orbital-mechanics.md) (orbits):* a multiplayer "*Heart of Gold*" trajectory-planning game where two crews race to plan the most efficient transfer.
- *[Lab 16](lab-16-smart-telemetry-beacon.md) (telemetry beacon) + [Lab 22](lab-22-spa-frontend.md) (SPA) + [Lab 31](lab-31-llm-rag-app.md) (LLM):* a "smart-monitoring" station that explains its own readings in natural language.
- *[Lab 24](lab-24-browser-extension.md) (browser extension) + [Lab 31](lab-31-llm-rag-app.md) (LLM):* an extension that turns *any* website into a structured study deck.
- *[Lab 11](lab-11-mini-file-explorer.md) (file explorer) + [Lab 36](lab-36-embedded-linux-from-inside.md) (embedded Linux) + [Lab 38](lab-38-binary-exploitation.md) (exploitation):* a forensic file-explorer that reverses unknown filesystems.
- *[Lab 26](lab-26-procedural-roguelike.md) (procedural roguelike) + [Lab 25](lab-25-platformer-game.md) (platformer) + [Lab 14](lab-14-cellular-automata.md) (cellular automata):* a roguelike whose dungeons evolve over real time according to CA rules.
- *[Lab 30](lab-30-cross-platform-app.md) (cross-platform mobile) + anything in 16-19 (embedded):* a *real*-feeling consumer hardware product with companion app.
- *[Lab 39](lab-39-web-security-owasp.md) (web security) + [Lab 21](lab-21-rest-api-auth.md) (REST API):* a verified-secure SaaS micro-product, with a public pen-test report.

The *combination* must do something neither part can do alone. That is the hardest constraint of Path A — and the most rewarding to defend.

### Path B — The Question

Build something brand-new that draws on the *vocabulary* of the program but answers your own question. The question must be specific, defensible, and *yours*. Some examples to seed your imagination:

- *"Can a Ukrainian high-school student plan and watch a real LEO satellite pass without leaving their browser?"* → an end-to-end pass-prediction web app, gamified, mobile-friendly, with educational layers.
- *"What does a tiny piece of accessibility software look like, done well?"* → a screen-reader plugin, a dyslexia-friendly font extension, a sign-language captioner.
- *"Can I build a privacy-respecting Telegram replacement for my friend group?"* → end-to-end encrypted, federated, twenty users, real.
- *"Can I help my grandmother manage her medication?"* → a single-purpose mobile app, *built for one user* but built well.
- *"What does a beautiful 1970s-style flight computer feel like in 2026?"* → a hardware + software product with a CRT-style UI.
- *"Could I make a free CS textbook that is genuinely better than the paid ones?"* → an open-source, interactive book with embedded simulations.
- *"What if the world's most useful debugger lived in your terminal?"* → a small TUI tool. Open-source. Documented.
- *"What does an honest dating app look like?"* — write the manifesto first.
- *"How do I help my city?"* — local civic-tech.
- *"What does the stack I'd build at my own startup look like?"* — show me. End-to-end.

Path B is *harder to scope* and *harder to ship*. But its ceiling is higher. Choose Path B only if you can write a one-sentence question that could fit on the cover of a book.

---

## Levels — or why levels don't apply this time

This lab does not have *Basic / Standard / Advanced*. It has **shipped** or **not shipped**.

There is, instead, an honesty contract:

- **Shipped means: a real human, who is not you and not your teammate, can use it.** Browser URL, downloadable APK, Docker image, package on `pip`/`npm`/`crates.io`, a built artifact in a release. *Something runs.*
- **Public means: there is a real public URL, repo, or release.** Not localhost. Not a screenshot. Not a "trust me, it works."
- **Defended means: you can explain, in five minutes and in plain language, the question and the answer.**

If those three are true, you've passed the lab.

If you also *delight someone* (a user, a teammate, a recruiter, an old friend), you've understood the lab.

---

## The deliverables

Every Lab 42 project includes, regardless of path:

1. **The product itself** — shipped. Public. Runnable.
2. **`MANIFESTO.md`** — a one-page document opened with **"The Question"** and closed with **"The Answer"**, the latter labeled `42`. *Yes, exactly that.* It's the lab's name. (See *The Manifesto* below.)
3. **A 60–120 second demo video** — recorded, hosted publicly. Could be Loom, YouTube unlisted, or a `.mp4` in the repo. *No live-only demos.*
4. **A clean README** with a hero image, a quickstart, the architecture, and a *Don't Panic* note.
5. **A short retrospective** in `docs/RETRO.md`: what worked, what didn't, what you'd do differently, and which prior labs flowed into this one.
6. **A public showcase post** — a tweet, a LinkedIn post, a Mastodon thread, a Telegram-channel announcement. *Tell the world.* (Optional but encouraged. Hiring loops start here.)
7. **A defense session** at the showcase — five minutes, no slides required.

---

## The Manifesto (a tiny formal document)

```
# MANIFESTO

## The Question
A single sentence, framed simply enough that a non-engineer understands it.

## The Premise
Two to three paragraphs: why this question, why now, what already exists, what is missing.

## The Stack
What you're building it with, and why.

## The Constraints
What you will *not* do. (This is the hardest part.)

## The Answer
> 42

(Where "42" is, by tradition and structural necessity, your shipped product.)
```

The Manifesto is the lab's ceremonial centerpiece. It exists for two reasons: it forces you to articulate the question (which is the *real* hard work), and it gives recruiters and peers a 90-second on-ramp to your project. Real Lab 42 README files in the wild begin with an embedded copy of the Manifesto. So should yours.

---

## Three-week plan with milestones

This plan is a default. Bend it freely.

**Week 1 — The Question**

- **Days 1–2 — Inventory.** Re-read your own previous 41 README files. Note which gave you joy, which gave you pain, which surprised you. Note where you wished you'd had more time.
- **Day 3 — Three candidates.** Write three one-sentence questions. Steelman each. Pick the one that scares you a little.
- **Day 4 — The Manifesto first draft.** Write `MANIFESTO.md` *before* writing any code. Yes, really. Premise. Constraints. The Question.
- **Day 5 — Architecture sketch.** Draw the diagram. Pick the stack. Pick the two riskiest unknowns and timebox spike experiments for them.
- **Days 6–7 — Spike + scope cut.** Run the two spike experiments. Cut your scope based on what you learned. Update the Manifesto's *Constraints* section. *Milestone: scope is small enough to ship in 14 days.*

**Week 2 — Build the spine**

- **Days 8–10 — Vertical slice.** Build the *thinnest end-to-end version* of your product. Not pretty. Not complete. *End-to-end.* A user can use it, even if it's ugly.
- **Days 11–13 — Iterate.** Show it to two friends. Take their feedback like an adult. Iterate. Polish.
- **Day 14 — Mid-checkpoint.** Working product, ugly UI, hosted somewhere. *Milestone: shipped, even if rough.*

**Week 3 — Polish, ship, defend**

- **Days 15–17 — Polish.** UI. README. Edge cases. The 80/20 of what makes a project feel professional.
- **Day 18 — Demo video.** Record it. Embed it.
- **Day 19 — Public showcase post.** Write it. Post it. *Cringe is part of the program.*
- **Day 20 — Retro.** Write `docs/RETRO.md`. Be specific. Be honest.
- **Day 21 — Defense.** Stand in front of the gallery. Explain the question. Explain the answer. Take the questions.

---

## Side quests (optional, brilliant if done)

- **Open-source it from day one.** Issues open. Contributions welcome. License chosen.
- **A landing page.** A real one. With copy that doesn't apologize.
- **Telemetry.** Privacy-respecting analytics so you actually know how many people used it. Not vanity metrics; *user-journey* metrics.
- **A blog post** explaining the architecture *and* the trade-offs. (One blog post that earns its readership is worth ten that don't.)
- **A Show HN / Product Hunt / itch.io / Reddit launch.** *Real users this week.*
- **A user feedback round.** Five users, twenty-minute interviews, written-up notes. *Genuinely* hard, *genuinely* career-shaping skill.
- **An on-ramp for contributors.** A `CONTRIBUTING.md` that a stranger could actually follow.
- **A tiny commercial test.** Charge a friendly user $1 for it. Nothing teaches a junior more about software than a single voluntary transaction.
- **Internationalization** (Ukrainian-first if appropriate). The diaspora is a real user base.
- **Accessibility.** Run a screen reader against your product. Fix what you find.
- **Performance budget.** Decide what "fast" means. Hold yourself to it.
- **Reproducible build.** A single command. From a fresh clone. To a running product.

Pick one. Pick three. Pick all. Each one *separately* lifts the lab into territory most juniors never reach.

---

## Working solo or in a team

Solo: **encouraged.** Path B in particular shines as a solo project. You will own every decision; that ownership is the lab's most valuable byproduct.

Team (up to 3):
- **The Question must still be one sentence.** Teams die on incoherent questions. *Don't*.
- *By role:* one product, one engineering, one design — even if "design" is just typography and screenshots.
- *By module:* split by clean architectural seam, not by personality.
- *By path:* two members do Path A (synthesis of three labs), one does Path B (the new question that the synthesis serves).
- **Demo together. Defend individually.** Each team member gets two minutes alone with their part of the answer.

Two team rules: **git from day one** and **list who did what.** And: **if you can't agree on the Manifesto by Day 4, split into two solo projects.** Better two clear answers than one muddled one.

---

## Tooling and platform tips

- **Pick boring tech for the spine, exciting tech for the soul.** Boring tech ships. Exciting tech demos. Mix carefully.
- **Use what you know, unless the question forces something else.** This is not the lab to learn three new frameworks at once.
- **Hosting:** Vercel / Netlify / Cloudflare Pages for web; Render / Fly.io / Railway for backends; Hugging Face Spaces for ML demos; itch.io for games; sideloadable APK for mobile (Play Store optional). Free tiers on each.
- **Domain:** consider a `.dev` or country-flavored TLD. A custom domain raises the perceived seriousness of a project by an order of magnitude. Cost: ~$15/year. *Worth it.*
- **CI from day one.** Even a one-test pipeline. The discipline is what matters.
- **Analytics:** [Plausible](https://plausible.io/), [Umami](https://umami.is/), or simple server-side log parsing. Privacy-respecting *and* career-readable.

---

## Suggested project structure

There is no required layout. Match the conventions of your stack. *But:*

```txt
your-project-name/
  README.md                  # opens with the Manifesto
  MANIFESTO.md               # the lab's ceremonial document
  src/
  ...
  docs/
    architecture.png
    RETRO.md
    user-interviews.md       # if you did them
  demo.mp4                   # or a YouTube link in the README
  LICENSE
```

The *most important* file is `MANIFESTO.md`. It is the file that turns *Lab 42* into *Your Answer*.

---

## When you get stuck

- **You can't pick a Question.** Talk to two people who care about you for 20 minutes about what's been frustrating them this year. The answer is usually in their answer.
- **The scope is too big.** Cut it in half. Then in half again. The Manifesto's *Constraints* section is where you do this on paper, before doing it in code.
- **You're 5 days in and you've written zero shipping code.** The Manifesto is finished, the architecture is sketched, but you're "still planning." Stop. Start the vertical slice. *Today.* Ugly is fine. Working is the only constraint that matters now.
- **Your teammate disagrees with the Question.** Re-read the Manifesto out loud together. If you still disagree, split into two solo projects. *No shame.*
- **You hit a hard technical wall on Day 18.** Cut the feature that's blocking you. Ship without it. Document the cut in the Retro. *Shipping is non-negotiable.*
- **You hate your own product on Day 20.** Welcome to engineering. Ship it anyway. The retrospective is where the hatred becomes wisdom.

---

## Submission checklist

- [ ] **`MANIFESTO.md`** present, signed, with `42` as The Answer.
- [ ] Product is **shipped** — public URL, public release, or working binary in the README.
- [ ] **Demo video** (60–120s) embedded in README.
- [ ] **README** has a hero, a quickstart, an architecture sketch, a *Don't Panic*.
- [ ] **`docs/RETRO.md`** present and specific.
- [ ] At least one real human, who is not you, has used the product. Note who.
- [ ] At least one prior lab is meaningfully reused (Path A) or visibly *informs* the design (Path B).
- [ ] License chosen (MIT / Apache-2.0 / AGPL — your call, but choose).
- [ ] Public showcase post link (Mastodon / X / LinkedIn / Telegram / GitHub Discussions) — optional, encouraged.
- [ ] Honest limitations section: what's left, what's broken, what's deferred.

---

## What recruiters look at

- **They open Lab 42 first.** If your portfolio README is well-organized, this is the project at the top.
- **They read the Manifesto.** If The Question is clear and *yours*, the rest of the interview goes differently. If The Question is generic, the interview goes the other way.
- **They watch the demo video.** *Sixty seconds matters here.* Open with the answer; explain the question second.
- **They look at the GitHub graph.** Did you ship steadily, or did you cram in week 3? Both are fine; the latter just means you're human.
- **They look at the retro.** A junior who can write *"here's what I'd do differently"* is hireable. A junior who can't is not.
- **They look at "real users."** Even one is a credibility multiplier.
- **They look at the cross-lab citations.** "Built on top of my [Lab 33](lab-33-object-detection-tracking.md) + [Lab 37](lab-37-px4-mavlink-drone-stack.md)" tells a coherent story. "Random new project unrelated to anything else I learned" tells the opposite story.
- **For Ukrainian recruiters specifically:** if your Question has a Ukrainian context (defense, civic-tech, accessibility, education, agriculture, energy), say so. The local-relevance signal is high.

---

## Reflection — the defense session

Five minutes, in front of the gallery. No slides required. Be ready to:

1. **State The Question** in one sentence.
2. **State The Answer** by demoing the product.
3. **Walk me through one architectural decision and the trade-off it cost you.**
4. **Walk me through one technical risk you took** that didn't pay off — and what you learned.
5. **Tell me which prior lab gave you the unlock** — the moment when the program clicked into the project.
6. **Tell me what you'd cut from the program** — *honestly*. The labs that bored you. The ones that didn't earn their place. (Yes, including this one if you feel that way. The instructor can take it.)
7. **Tell me what's next.** Will you keep maintaining this? Will you let it die honorably? Both are valid. Lying about it is not.

---

## Showcase — the gallery night

The end-of-program gallery. Every project on a laptop, every author at a table, every visitor with five questions and a coffee. Anonymous voting in three categories: **clearest Question**, **most beautiful Answer**, **most ambitious shipped artifact**. The institute publishes the winners; the winners get coffee. The losers also get coffee. *Everyone gets coffee.* This is a programming program, not a coliseum.

Recruiters are invited. Friends are invited. Family is invited. **Bring your grandmother.** Watch her use your project. Take notes. *That* is the moment the program ends.

---

## Going further

This lab has no *Going further* section in the usual sense. The whole *rest of your career* is the *Going further*.

But: a small reading list, in the spirit of the lab.

- *The Hitchhiker's Guide to the Galaxy* — Douglas Adams. Re-read at least the first book.
- *Hackers & Painters* — Paul Graham. The essays "Beating the Averages" and "Why Smart People Have Bad Ideas" in particular.
- *The Pragmatic Programmer* (20th anniversary ed.) — Hunt & Thomas. The book that taught a generation what *senior* feels like.
- *Show Your Work* — Austin Kleon. Short, kind, true.
- *Anything You Want* — Derek Sivers. 90 minutes; a different perspective on what shipping is for.
- The original *École 42* white paper and any of the public *Piscine* writeups.
- *Built to Last* (Voyager — JPL technical memos, freely available online).
- *The Mom Test* by Rob Fitzpatrick — for the user-interview side quest.

---

## A final word — and the end of the program

You've finished forty-one labs. Then you wrote one more, the one with no prompt. You picked the question. You wrote the answer. You shipped it.

The program was never the labs. **The program was the habit of shipping.** Every two weeks for a year, you turned an empty repo into something runnable. *That habit* — quietly, repeatedly, dependably making things — is the rarest skill in our industry. Most people who can write code cannot make things. You can now.

Ukraine, in 2026, has more talent than infrastructure, more drive than time, more ideas than open positions can absorb. The country needs engineers who can do exactly what you've done in this program: pick a hard problem, ship a solution, defend the choices, fix the bugs, and start again on Monday. Whether you stay here, leave and come back, leave and don't come back, or never leave — you carry that habit with you. **It will outlast every employer you ever have. It will outlast every framework you'll ever learn. It will outlast — yes, almost certainly — even *Voyager 1*'s plutonium battery.** That habit is the answer, and it always was.

The question — well, that's yours.

42.

---

> "In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move."
> "Forty-two."
> "Don't Panic."
> — Douglas Adams

> *— end of the program. now ship something.*
