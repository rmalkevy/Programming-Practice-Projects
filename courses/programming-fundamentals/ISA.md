# The `ember` machine — memory map and instruction set

[English](ISA.md) · [Українською](ISA.uk.md) · Course: [EN](README.md) · [UK](README.uk.md)

> Це довідник, а не текст для читання підряд. Тримайте його відкритим у сусідній
> вкладці весь семестр. Кожна лаба додає сюди кілька рядків — і жодна не змінює
> те, що вже є.

This page is the **contract** between your CPU and your assembler. Lab 2 freezes
it; Labs 3–8 each add a few rows. Nothing already in the table ever changes
meaning — that is the point of having one table instead of a paragraph per lab.

If your `step()` and your assembler ever disagree about an instruction, **this
table wins** and both are wrong.

---

## 1. The machine at a glance

| Part | Size | Notes |
|---|---|---|
| RAM | 4096 bytes | addresses `0x000`–`0xFFF` |
| `A`, `B` | 8 bits each | the working registers |
| `H` | 16 bits | the **address** register — a pointer, held in the CPU (Lab 3) |
| `PC` | 16 bits | program counter: address of the *next* instruction. Starts at `0x000` |
| `SP` | 16 bits | stack pointer. Starts at `0xFFF` (Lab 7) |
| `Z` `N` `C` | 1 bit each | the flags (Lab 2) |
| Display | 64 × 32 pixels | 1 bit per pixel, **inside RAM** (Lab 5) |

`A` and `B` hold **values**. `H` holds an **address**. That difference is the
whole of [Lab 3](lab-03-addresses-not-names.md), built into the hardware.

---

## 2. Memory map

```txt
0x000 ┌─────────────────────────────┐
      │  CODE                       │  2048 bytes
      │  your program. PC starts    │  instructions live here
      │  at 0x000                   │
0x800 ├─────────────────────────────┤
      │  DATA                       │  512 bytes
      │  strings, arrays, counters  │
0xA00 ├─────────────────────────────┤
      │  VRAM   64 x 32, 1 bit/px   │  256 bytes   <- the screen IS memory
0xB00 ├─────────────────────────────┤
      │  (spare - yours)            │  256 bytes
0xC00 ├─────────────────────────────┤
      │  HEAP     ▼ to higher addr  │  768 bytes
      │                             │  ALLOC hands out blocks from 0xC00 up
0xF00 ├─────────────────────────────┤
      │  STACK    ▲ to lower addr   │  256 bytes
      │                             │  SP starts at 0xFFF and walks down
0xFFF └─────────────────────────────┘
```

| Region | Range | Constant | Appears in |
|---|---|---|---|
| Code | `0x000`–`0x7FF` | `CODE_LO`, `CODE_HI` | [Lab 2](lab-02-bits-dont-lie.md) |
| Data | `0x800`–`0x9FF` | `DATA_LO`, `DATA_HI` | [Lab 3](lab-03-addresses-not-names.md) |
| VRAM | `0xA00`–`0xAFF` | `VRAM_LO`, `VRAM_HI` | [Lab 5](lab-05-many-of-one-thing.md) |
| Heap | `0xC00`–`0xEFF` | `HEAP_LO`, `HEAP_HI` | [Lab 6](lab-06-named-bundles.md) |
| Stack | `0xF00`–`0xFFF` | `STACK_LO`, `STACK_HI` | [Lab 7](lab-07-call-and-return.md) |

Nothing enforces these boundaries — a program *can* `STORE` into its own code.
That is not a bug in `ember`; that is what "von Neumann machine" means, and it is
why real operating systems spend so much effort on memory protection.

### Output port and timer (*opt*, Lab 5)

Two addresses in the spare region can behave like hardware instead of memory. This
is optional: required programs never touch them, and before Lab 5 they are plain
bytes.

| Address | Name | What it does |
|---|---|---|
| `0xB00` | `PORT_OUT` | a guest write (`STORE [0x0B00], A`, `STORE [H], A`, …) prints the byte as a character **immediately**. The byte also stays in memory |
| `0xB01` | `TICKS` | a guest read (`LOAD A, [0x0B01]`, `LOAD A, [H]`) returns how many instructions have run, including this one, modulo 256 |

Only a **guest** write is a port write: the host's `set` command prints nothing. The
difference from video memory is that writing VRAM is just a write, and you need
`SHOW` to see anything. Writing the port *is* the action. That is how the
peripherals of real microcontrollers work ([HARDWARE.md](HARDWARE.md#lab-3--адреси-а-не-імена),
in Ukrainian), and it is why C and C++ mark such addresses `volatile`.

Heap and stack grow **towards each other**: the heap bumps upward from `0xC00`,
`SP` walks downward from `0xFFF`. `ember` puts a fixed fence between them at
`0xF00`, so each one runs out on its own. A real machine has no fence — the two
grow until they collide, and *that* is the picture behind the words "stack
overflow". Draw it once.

---

## 3. Flags

Set by the ALU group and by `CMP`, read by the conditional jumps.

| Flag | Name | Set when |
|---|---|---|
| `Z` | zero | the result is `0` |
| `N` | negative | bit 7 of the result is `1` (the sign bit, if you read it as signed) |
| `C` | carry | the result did not fit in 8 bits (`ADD`), a borrow happened (`SUB`, `CMP`), or the bit shifted out (`SHL`, `SHR`) |

**The trap everyone falls into:** `LOAD` and `LOADI` do **not** touch the flags.
Loading a zero into `A` does not set `Z`. If you want to branch on a value you
just loaded, put a `CMP` (or `DEC`/`INC`) in between. Real CPUs differ on this;
ours is explicit on purpose.

---

## 4. Encoding

- One instruction = **1 opcode byte**, plus 0–2 operand bytes.
- 16-bit operands are stored **little-endian**: low byte first. `JMP 0x0123`
  assembles to `30 23 01`.
- The **high nibble of the opcode is the group**. That is what the mask and
  shift in [Lab 2](lab-02-bits-dont-lie.md) are for:
  `group = (op >> 4) & 0x0F`.

| Group | Meaning |
|---|---|
| `0x0_` | control and output |
| `0x1_` | ALU |
| `0x2_` | moving data |
| `0x3_` | jumps |
| `0x4_` | display |
| `0x5_` | stack and calls |
| `0x6_` | system |
| `0x7_`–`0xF_` | **free — your extensions go here** |

---

## 5. The instruction set

**Size** is the total length in bytes, and therefore how much `PC` advances.
**Lab** is the lab that adds the instruction. `opt` means optional — build it if
you want it, the required programs do not need it.

### `0x0_` — control and output

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x00` | `HALT` | 1 | — | stop; further `step` refuses | 2 |
| `0x01` | `NOP` | 1 | — | do nothing | 2 |
| `0x02` | `OUT` | 1 | — | print `A` to stdout as a **character** | 3 |
| `0x03` | `OUTN` | 1 | — | print `A` to stdout as a **decimal number**, then a space | 3 |
| `0x04` | `OUTS addr16` | 3 | — | print bytes from `addr` until a `0` byte, or 256 bytes, whichever comes first | 5 |

### `0x1_` — ALU

All of these read and write `A` (and read `B` where shown), and wrap at 8 bits.

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x10` | `ADD A, B` | 1 | Z N C | `A = A + B` | 2 |
| `0x11` | `SUB A, B` | 1 | Z N C | `A = A - B` | 2 |
| `0x12` | `AND A, B` | 1 | Z N, C=0 | `A = A & B` | 2 |
| `0x13` | `OR A, B` | 1 | Z N, C=0 | `A = A \| B` | 2 |
| `0x14` | `XOR A, B` | 1 | Z N, C=0 | `A = A ^ B` | 2 |
| `0x15` | `NOT A` | 1 | Z N, C=0 | `A = ~A` | 2 |
| `0x16` | `SHL A` | 1 | Z N C | `A = A << 1`; `C` = the bit pushed out of bit 7 | 2 |
| `0x17` | `SHR A` | 1 | Z N C | `A = A >> 1`; `C` = the bit pushed out of bit 0 | 2 |
| `0x18` | `INC A` | 1 | Z N | `A = A + 1` | 2 |
| `0x19` | `DEC A` | 1 | Z N | `A = A - 1` | 2 |
| `0x1A` | `CMP A, B` | 1 | Z N C | compute `A - B`, set flags, **discard the result** | 4 |
| `0x1B` | `MUL A, B` | 1 | Z N C | `A = A * B`, low 8 bits; `C` set if the real product did not fit | 7 |

### `0x2_` — moving data

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x20` | `LOADI A, imm8` | 2 | — | `A = imm8` | 3 |
| `0x21` | `LOADI B, imm8` | 2 | — | `B = imm8` | 3 |
| `0x22` | `LOAD A, [addr16]` | 3 | — | `A = mem[addr]` | 3 |
| `0x23` | `LOAD B, [addr16]` | 3 | — | `B = mem[addr]` | 3 |
| `0x24` | `STORE [addr16], A` | 3 | — | `mem[addr] = A` | 3 |
| `0x25` | `STORE [addr16], B` | 3 | — | `mem[addr] = B` | 3 |
| `0x26` | `MOV A, B` | 1 | — | `A = B` | 3 |
| `0x27` | `MOV B, A` | 1 | — | `B = A` | 3 |
| `0x28` | `LOADH H, imm16` | 3 | — | `H = imm16` — put an address in the address register | 3 |
| `0x29` | `LOAD A, [H]` | 1 | — | `A = mem[H]` — follow the pointer | 3 |
| `0x2A` | `STORE [H], A` | 1 | — | `mem[H] = A` | 3 |
| `0x2B` | `INCH` | 1 | — | `H = H + 1` — walk to the next cell | 3 |
| `0x2C` | `DECH` | 1 | — | `H = H - 1` | 3 |
| `0x2D` | `HLOW` | 1 | — | *opt* `A = H & 0xFF` — the low byte of `H`, handy for printing an index | 4 |

`LOADH` / `LOAD A, [H]` / `INCH` are the three instructions that make a loop over
memory possible. Without them a program can only touch addresses it knew when it
was assembled — which is exactly the difference between a name and an address.

### `0x3_` — jumps

All 3 bytes. On a **taken** jump, `PC` becomes the operand; do **not** also add
the size. On a not-taken jump, `PC += 3` as usual.

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x30` | `JMP addr16` | 3 | — | always jump | 4 |
| `0x31` | `JZ addr16` | 3 | — | jump if `Z` is set | 4 |
| `0x32` | `JNZ addr16` | 3 | — | jump if `Z` is clear | 4 |
| `0x33` | `JC addr16` | 3 | — | *opt* jump if `C` is set | 4 |
| `0x34` | `JNC addr16` | 3 | — | *opt* jump if `C` is clear | 4 |

### `0x4_` — display

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x40` | `CLS` | 1 | — | write `0` to all 256 VRAM bytes | 5 |
| `0x41` | `PLOT` | 1 | C | set the pixel at `x = A`, `y = B`. Off-screen: set `C`, change nothing | 5 |
| `0x42` | `UNPLOT` | 1 | C | *opt* clear that pixel | 5 |
| `0x43` | `SHOW` | 1 | — | draw VRAM into the terminal | 5 |

### `0x5_` — stack and calls

The stack is **empty-descending**: `SP` always points at the next free byte.

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x50` | `PUSH A` | 1 | — | `mem[SP] = A; SP = SP - 1` | 7 |
| `0x51` | `POP A` | 1 | — | `SP = SP + 1; A = mem[SP]` | 7 |
| `0x52` | `PUSH B` | 1 | — | same, with `B` | 7 |
| `0x53` | `POP B` | 1 | — | same, with `B` | 7 |
| `0x54` | `CALL addr16` | 3 | — | push the return address (2 bytes), then `PC = addr` | 7 |
| `0x55` | `RET` | 1 | — | pop 2 bytes into `PC` | 7 |
| `0x56` | `PUSH H` | 1 | — | *opt* push `H` (2 bytes: low, then high) | 7 |
| `0x57` | `POP H` | 1 | — | *opt* pop 2 bytes into `H` | 7 |

`SP` below `STACK_LO` is a **stack overflow**; `SP` at or above `STACK_HI` on a
pop is a **stack underflow**. Both must stop the machine with a message, never
crash the host process and never silently wrap.

### `0x6_` — system

| Op | Mnemonic | Size | Flags | Meaning | Lab |
|---|---|---|---|---|---|
| `0x60` | `ALLOC` | 1 | C | allocate `A` bytes on the heap: `H` = the block's address, heap pointer advances. No room: set `C`, leave `H` alone | 6 |

There is no `FREE`. A bump allocator only ever moves forward — say so in your
README and explain what that costs.

---

## 6. How `CALL` and `RET` work, exactly

This is the one place where being vague costs you two days.

```txt
CALL addr16, sitting at address P (so the instruction occupies P, P+1, P+2):

    ret  = P + 3                 ; the address AFTER the CALL, not P
    mem[SP] = ret & 0x00FF       ; low byte
    SP      = SP - 1
    mem[SP] = ret >> 8           ; high byte
    SP      = SP - 1
    PC      = addr16

RET:

    SP = SP + 1 ;  hi = mem[SP]  ; high byte comes off first
    SP = SP + 1 ;  lo = mem[SP]
    PC = (hi << 8) | lo
```

Push low-then-high, pop high-then-low. Get that backwards and `RET` jumps
somewhere plausible-looking, which is far worse than crashing.

### A worked example

`fact(5) = 120`, verified. Thirty bytes. Type it in, `run` it, then trace it —
this listing is **given** so that Lab 7 is about the stack, not about hexadecimal.

```txt
addr  bytes        source
0000  20 05        LOADI A, 5        ; n = 5
0002  54 07 00     CALL  fact
0005  03           OUTN              ; prints 120
0006  00           HALT

; fact(n): argument in A, result in A. Clobbers B.
0007  21 00        fact:  LOADI B, 0
0009  1A                  CMP   A, B       ; n == 0 ?
000A  31 1B 00            JZ    base
000D  21 01               LOADI B, 1
000F  1A                  CMP   A, B       ; n == 1 ?
0010  31 1B 00            JZ    base
0013  50                  PUSH  A          ; save n -- the call will destroy A
0014  19                  DEC   A
0015  54 07 00            CALL  fact       ; A = fact(n-1)
0018  53                  POP   B          ; B = the n we saved
0019  1B                  MUL   A, B       ; A = fact(n-1) * n
001A  55                  RET
001B  20 01        base:  LOADI A, 1
001D  55                  RET
```

`fact(0)` and `fact(1)` both return 1 in 9 and 12 steps; `fact(5)` takes 60 steps
and leaves `SP` back at `0xFFF`. If yours does not, one of `CALL`, `RET` or the
`PUSH`/`POP` pairing is wrong — and a stack that does not return to `0xFFF` is
the fastest way to find out.

Note what the two `JZ base` operands share: `1B 00`. Insert one instruction
anywhere above `base` and **both** of them change. That is the argument for
[Lab 8](lab-08-give-it-a-language.md) in one sentence.

### Calling convention

The CPU does not save your registers. **You** do. The convention this course
uses, and which the four programs in Lab 8 follow:

- **Argument** goes in `A`.
- **Return value** comes back in `A`.
- `B` and `H` are **caller-saved**: if you need them after a `CALL`, `PUSH` them
  before it and `POP` them after.
- Anything else a function needs, it pushes on entry and pops before `RET`.

Write this paragraph in your own README too. Two functions that disagree about
who saves `B` is the classic bug of Labs 7–8, and it is unfindable unless the
convention is written down somewhere you can point at.

---

## 7. The display is memory

VRAM is 256 bytes at `0xA00`. 64 pixels per row ÷ 8 bits = **8 bytes per row**,
32 rows.

```txt
byte address = VRAM_LO + y * 8 + (x / 8)
bit number   = 7 - (x % 8)            ; bit 7 is the LEFTMOST pixel of the byte
pixel is lit = (mem[byte address] >> bit number) & 1
```

`PLOT` exists because computing that in bytecode every time is miserable. But it
is not magic, and you should prove it: `STORE` the byte `0x80` at `0xA00` by hand
and `SHOW`. The top-left pixel lights up. **Your screen is just a dump you know
how to look at** — which is the sentence this whole course exists to earn.

---

## 8. Your extensions

Opcodes `0x70`–`0xFF` are free. Add whatever you like — `MUL`, `JG`, a random
number generator, a keyboard port. Two rules:

1. Add a row to a table in **your** README, in exactly this format, with the
   size and the flags filled in.
2. Never redefine an opcode that is already in this file. Other people's
   programs — and next semester's you — assume the table above.

---

## 9. Two programs to check yourself against

### Count down from 3 and print each number

```txt
addr  bytes       source
0000  20 03       LOADI A, 3
0002  03          loop:  OUTN
0003  19                 DEC A
0004  32 02 00           JNZ loop
0007  00                 HALT
```

Output: `3 2 1 `. Note `JNZ`'s operand `02 00` — little-endian for `0x0002`.

### Light the top-left pixel without using `PLOT`

```txt
addr  bytes       source
0000  40          CLS
0001  20 80       LOADI A, 0x80
0003  28 00 0A    LOADH H, 0x0A00
0006  2A          STORE [H], A
0007  43          SHOW
0008  00          HALT
```

If one pixel appears in the corner, your memory map, your bit order and your
`SHOW` all agree. If it appears anywhere else, exactly one of those three is
wrong — and now you know which three things to check.
