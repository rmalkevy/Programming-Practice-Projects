#!/usr/bin/env python3
"""Insert a domain-aware `> **Portfolio tip:**` blockquote into each lab's
`## The target` section.

Same pattern as add_reference_videos.py: a dict of lab-number -> tip text.
- For labs 04-38 the tip is inserted right after the `> **Reference ...**` line.
- For labs 39-41 (no Reference line) it is inserted right after the blank line
  that follows the `## The target` header.
- Labs 01-03 already have a tip; lab 42 (capstone) is intentionally skipped.

Also runs a cosmetic pass over every lab file, normalizing single-digit lab
link display text: `[Lab 7](...)` -> `[Lab 07](...)`.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABS_DIR = os.path.join(ROOT, "labs")

TIPS = {
    4: """> **Portfolio tip:** hardware projects live or die on the demo. Put a **60-90 second video** at the top of your README showing real sensor values change as you breathe on the sensor, shine a light, or move the board, plus one clear wiring photo or diagram. A recruiter who can *see* it work in 90 seconds trusts it far more than a table of numbers.""",
    5: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *use in the browser*. Aim to ship a small web build (drag in an image, pick a filter, see the result instantly) deployed to GitHub Pages / Vercel, with before/after pairs in the README. A tool people can try in one click beats a folder of output PNGs.""",
    6: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *watch grow, live*. Aim to ship a browser build (adjust parameters with sliders, watch the tree redraw) to GitHub Pages / Vercel, and put a short GIF at the top of the README. An interactive visualization reads as far more alive than a static screenshot.""",
    7: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *play with in the browser*. Aim to ship a web build where they draw walls, drop start/end points, and watch the search explore, deployed to GitHub Pages / Vercel, with a GIF of the search animating in the README. Watching A* fan out and find the path sells the algorithm instantly.""",
    8: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *zoom into, live*. Aim to ship a browser build with click-to-zoom deep into the Mandelbrot set, deployed to GitHub Pages / Vercel, plus your best high-res render at the top of the README. Endless zoom in one click is unforgettable; a static image is not.""",
    9: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *play in one click*. If you port it to the browser (canvas or a WASM build), deploy it to GitHub Pages / itch.io and link it at the top of the README; otherwise put a short GIF of a real rally. A game someone can actually play beats a description of one.""",
    10: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *run live*. Aim to ship a browser build that animates both generation and solving, deployed to GitHub Pages / Vercel, with a GIF at the top of the README. Watching the maze carve itself and then get solved is a 5-second sell.""",
    11: """> **Portfolio tip:** the strongest version of a CLI/TUI is one a recruiter can *run without a toolchain*. Ship prebuilt binaries for Windows / macOS / Linux on GitHub Releases, and put an **asciinema recording or GIF** at the top of the README. A one-download-and-run tool with a recording reads as a finished product.""",
    12: """> **Portfolio tip:** the single strongest version of this project is one a recruiter can *click and use*. If you go past Basic, deploy it (Vercel / Render / Fly.io) with a seeded demo account, and link the live URL at the top of the README. A working app they can add a task to beats any screenshot.""",
    13: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *poke at, live*. Aim to ship a browser build where they spawn objects and watch them collide and settle, deployed to GitHub Pages / Vercel, with a GIF at the top of the README. Interactive physics is mesmerizing; a still frame isn't.""",
    14: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *run in the browser*. Aim to ship a web build (draw a pattern, hit play, watch it evolve) to GitHub Pages / Vercel, with a GIF of a glider gun or your own pattern at the top of the README. Watching life emerge from rules is the whole magic - show it moving.""",
    15: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *search, live*. Aim to ship a web front end over a real corpus (a Wikipedia dump, your course notes, a subreddit) deployed to a public URL, so they can type a query and see ranked results. A working search box over real data beats a description of TF-IDF.""",
    16: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *watch update, live*. Aim for a **public telemetry dashboard URL** that updates as your device sends data, plus a 60-second video of readings changing in real time and a wiring photo. Live telemetry going from a physical device to a web page is a strong, memorable demo.""",
    17: """> **Portfolio tip:** this project is sold entirely by motion. Put a **short video** at the top of the README - the thing balancing (or the simulator holding setpoint under a disturbance you introduce) - plus a plot of the response settling. Seeing it recover from a shove is worth a thousand words about control theory.""",
    18: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *watch, live*. Aim for a public dashboard URL showing your plant's real readings over time, plus a 60-second video and a wiring photo. A live graph of real soil-moisture data (and an alert firing when it's dry) reads as a real product.""",
    19: """> **Portfolio tip:** this project is sold by seeing it *actually control something*. Put a **video** at the top of the README of your controller playing a real game (or your own [Lab 02](lab-02-ray-casting-engine.md) engine), plus a photo of the build. A custom stick moving a real game is one of the most memorable demos in this whole program.""",
    20: """> **Portfolio tip:** this *is* the recruiter's entry point, so treat it as the hub for everything else. Deploy it to a **custom domain**, and embed or link every other finished lab (live demos, videos, repos) from it. The strongest version is a site where one click leads to a working thing you built.""",
    21: """> **Portfolio tip:** the strongest version of a backend is one a recruiter can *call without cloning it*. Deploy it (Render / Fly.io / Railway) and link a **public interactive API docs URL** (Swagger / OpenAPI) plus a ready-to-run request collection. A live endpoint they can hit - with auth actually working - beats a repo they have to boot themselves.""",
    22: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *click and use*. Deploy it (Vercel / Netlify) with a seeded demo account, link the live URL at the top of the README, and make sure the failure cases (offline, expired token, invalid input) are visible in the demo. A polished frontend running against a real API is a 1-in-30 portfolio piece.""",
    23: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *see sync in real time*. Deploy it to a public URL and put a GIF at the top showing **two windows side by side**, an action in one instantly updating the other. Live sync across tabs is the entire wow - make it the first thing they see.""",
    24: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *install in one click*. Aim to publish it to the Chrome Web Store (or ship a one-download unpacked zip with clear load instructions), and put a short demo video at the top of the README. An extension they can actually add to their browser beats a code walkthrough.""",
    25: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *play in one click*. Export an HTML5 build and host it on itch.io / GitHub Pages, link it at the top of the README, and add a GIF of the best moment. A playable level in the browser beats any amount of description.""",
    26: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *play in the browser*. Ship a web build (or an itch.io HTML5 export), link it at the top of the README, and add a GIF plus a shareable seed. Letting someone generate their own dungeon in one click is the whole pitch.""",
    27: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *join and play, live*. Deploy the server and client to a public URL, and put a GIF at the top showing **two players in two windows** moving together. A multiplayer game a stranger can jump into is one of the strongest pieces you can show.""",
    28: """> **Portfolio tip:** the strongest version of a jam game is one a recruiter can *play in one click*. Publish it to **itch.io** (that's the culture) with an HTML5 build, a cover image, and a GIF, and link it at the top of the README. A finished, playable, themed game - shipped - says more than a big unfinished one.""",
    29: """> **Portfolio tip:** the strongest version of a mobile app is one a recruiter can *install and try*. Attach a signed **APK to a GitHub Release** and put a 30-second screen recording at the top of the README. Store publishing is optional - a sideloadable build plus a video is enough to prove it's real.""",
    30: """> **Portfolio tip:** the strongest version of a mobile app is one a recruiter can *open on their own phone*. Publish an **Expo / EAS preview link** (and a signed APK on a GitHub Release), plus a 30-second screen recording showing it running on both platforms. One QR code they can scan beats a wall of screenshots.""",
    31: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *ask a question and get an answer*. Deploy a demo (Vercel / a Hugging Face Space) with a rate-limited key or your own funded budget, and link it at the top of the README with 2-3 example questions. A live RAG chatbot over real docs beats a screenshot of one.""",
    32: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *run without setup*. Add an **"Open in Colab" badge** so they can train your net in the browser, and put your loss curves and sample outputs at the top of the README. A notebook that runs end-to-end in one click proves you actually built the thing.""",
    33: """> **Portfolio tip:** this project is sold by seeing it *track things on real video*. Put a **short output clip** (boxes + IDs following objects) at the top of the README, and ship a Gradio / Streamlit demo on a Hugging Face Space where a recruiter can upload their own clip. Watching your tracker follow a moving object is the entire pitch.""",
    34: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *use as a real product*. Deploy it to a public URL with a clear first-run experience (no setup, an example prepared), and link it at the top of the README with a 60-second demo video. "Narrow and polished and live" beats "broad and impressive in a screenshot."\
""",
    35: """> **Portfolio tip:** this project is sold by motion and traces. Put a **short video** at the top of the README - the craft holding attitude in the simulator (or on hardware) while you introduce a disturbance - plus a task-timing / scheduler trace. Seeing tasks meet their deadlines under load is what makes an RTOS project real.""",
    36: """> **Portfolio tip:** this project is sold by the boot. Put an **asciinema recording (or video)** at the top of the README of your custom image booting from power-on into your own userspace, plus the size and config of what you built. A recruiter watching a Linux you assembled boot into a shell trusts you did the deep work.""",
    37: """> **Portfolio tip:** this project is sold by seeing the drone *fly your code*. Put a **screen recording** at the top of the README of your mission running in the PX4 simulator (QGroundControl plus your ROS 2 / MAVLink node commanding it), plus an architecture diagram. A drone executing your autonomous mission in sim is a standout aerospace portfolio piece.""",
    38: """> **Portfolio tip:** in security, the deliverable is the **write-up**. Publish a clear, blog-style report (the vulnerability, your exploit, the fix) with a terminal recording of the exploit landing a shell, and link it at the top of the README. A readable exploit walkthrough - done ethically, on your own targets - is what a security recruiter actually reads. Keep the ethics framing front and center.""",
    39: """> **Portfolio tip:** in security, the deliverable is the **write-up**, not a public deploy. Keep the vulnerable app **local, launchable with one Docker command**, and publish a blog-style report per OWASP category (the exploit, a screenshot / PoC, and the fix) with a short demo video. Never expose the intentionally-vulnerable app on the public internet - the ethics framing above is part of the grade.""",
    40: """> **Portfolio tip:** in security, the deliverable is the **write-up**. Publish a blog-style report with your capture screenshots, what a plaintext protocol leaked vs what TLS protected, and the defensive fix, plus a short demo video - all on your own lab network only. A clear, ethical report reads as far more employable than raw tooling output. Keep the ethics framing front and center.""",
    41: """> **Portfolio tip:** the strongest version of this project is one a recruiter can *watch orbit, live*. Aim to ship a browser visualization (Three.js / canvas) of your trajectories and transfers, deployed to GitHub Pages / Vercel, with a GIF of a Hohmann transfer or gravity assist at the top of the README. A mission you can watch play out beats a plot of numbers.""",
}

SINGLE_DIGIT_LINK_RE = re.compile(r"\[Lab (\d)\]\(")


def lab_path(num: int) -> str:
    matches = glob.glob(os.path.join(LABS_DIR, f"lab-{num:02d}-*.md"))
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one file for lab {num}, got {matches}")
    return matches[0]


def insert_tip(num: int, tip: str) -> str:
    path = lab_path(num)
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if "Portfolio tip" in text:
        return f"lab {num:02d}: already has a tip, skipped"

    lines = text.split("\n")
    ref_idx = next(
        (i for i, ln in enumerate(lines) if ln.startswith("> **Reference")), None
    )
    if ref_idx is not None:
        lines[ref_idx + 1 : ref_idx + 1] = ["", tip]
    else:
        target_idx = next(
            (i for i, ln in enumerate(lines) if ln.strip() == "## The target"), None
        )
        if target_idx is None:
            raise SystemExit(f"lab {num:02d}: no anchor found")
        # header, "", <content> -> insert tip + blank after the blank line
        lines[target_idx + 2 : target_idx + 2] = [tip, ""]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return f"lab {num:02d}: tip inserted ({'after Reference' if ref_idx is not None else 'after The target'})"


def normalize_single_digit_links() -> int:
    changed = 0
    for path in glob.glob(os.path.join(LABS_DIR, "lab-*.md")):
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        new_text = SINGLE_DIGIT_LINK_RE.sub(r"[Lab 0\1](", text)
        if new_text != text:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_text)
            changed += 1
    return changed


def main() -> None:
    for num in sorted(TIPS):
        print(insert_tip(num, TIPS[num].strip()))
    print(f"normalized single-digit lab links in {normalize_single_digit_links()} files")


if __name__ == "__main__":
    main()
