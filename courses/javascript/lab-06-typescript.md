# Lab 06 — TypeScript: Types for the Protocol, the Simulation, and Both Sides of the Wire

> "TypeScript is JavaScript with a linter so good it needed its own compiler."

**Weeks:** 11–12 · **Language focus:** structural typing and inference; `unknown` vs `any`; union types and discriminated unions with exhaustive `switch`; generics; utility and mapped types; `readonly`; branded types; type guards, narrowing, and `satisfies`; `strict` `tsconfig`; running TS on Node and Vite; runtime validation at boundaries · **Project step:** the whole codebase typed under `strict`; one shared, typed protocol; validation of every incoming message; optional UI framework for lobby/HUD · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 05](lab-05-realtime-networking.md)

---

## This lab's feature

You now have three packages, a binary protocol with a dozen message types, entities of several kinds, and a simulation that runs in two runtimes. You've also, almost certainly, spent an afternoon on a bug that was a typo in a message field or a `undefined` that travelled three modules before exploding. That is the moment TypeScript pays for itself, and the reason this lab comes *now* rather than in week one: you have a real system with real seams, and you'll feel exactly what types buy.

**TypeScript** is a superset of JavaScript that adds a static type system, then erases it — the output is the same JavaScript you've been writing, with the same runtime behavior (which is why the event loop, prototypes, and promises you learned still apply unchanged). Its type system is unusual: **structural** (types are shapes, not names), heavily **inferred** (you write fewer annotations than in Java or C#), and expressive enough to describe a discriminated union of message types so precisely that the compiler *proves* your handler covers every case. It has become the default for professional JavaScript — the 2026 job market rarely says "JavaScript developer" without meaning TypeScript — and knowing it *well*, not just annotating parameters, is a differentiator.

---

## Theory

### 1. Structural typing and inference

In TypeScript, a type is a **shape**. `{ x: number; y: number }` is satisfied by any object with numeric `x` and `y`, whatever class or literal produced it. There is no `implements` needed; compatibility is checked by structure. This fits JavaScript's duck-typed reality and Lab 2's composition-over-inheritance design perfectly — a `Movable` interface is satisfied by anything with the right fields.

**Inference** does most of the work: `const ship = { x: 0, y: 0, angle: 0 }` is typed without annotation; `function len(v: Vec2)` needs only the parameter typed, the return is inferred. Annotate **function boundaries** (parameters, exported return types) and **let inference handle locals**. Hover in your editor to see what TypeScript inferred — that feedback loop is how you learn the type system.

### 2. `any`, `unknown`, and `strict`

`any` turns type-checking off for a value — and for everything it touches. It's how TypeScript projects rot. `unknown` is the *safe* top type: you can hold anything, but must **narrow** it (with `typeof`, `instanceof`, `in`, or a type guard) before using it. Data from the network, `JSON.parse`, or a `catch` clause is `unknown` until proven otherwise — which is exactly the discipline Lab 4 asked for ("validate every incoming message").

`"strict": true` in `tsconfig.json` turns on the checks that matter — `strictNullChecks` (`null`/`undefined` are types; `map.get(id)` returns `T | undefined` and you *must* handle it), `noImplicitAny`, `strictFunctionTypes`. Add `noUncheckedIndexedAccess` (array indexing returns `T | undefined` — annoying and correct) and `verbatimModuleSyntax` (forces `import type`, keeping runtime imports honest). Matt Pocock's [tsconfig cheat sheet](https://www.totaltypescript.com/tsconfig-cheat-sheet) is the current-best baseline; start from it.

### 3. Unions, discriminated unions, and exhaustiveness

The single most valuable TypeScript pattern for your project — and for most real code:

```ts
type ClientMessage =
  | { type: "join"; room: string; name: string }
  | { type: "input"; seq: number; tick: number; thrust: boolean; turn: -1 | 0 | 1; fire: boolean }
  | { type: "chat"; text: string };

function handle(msg: ClientMessage) {
  switch (msg.type) {
    case "join":  return onJoin(msg);     // msg is narrowed: msg.room exists here
    case "input": return onInput(msg);
    case "chat":  return onChat(msg);
    default: { const _exhaustive: never = msg; return _exhaustive; }  // compile error if a case is missing
  }
}
```

A **discriminated union** is a union of object types sharing a literal-typed field (`type`). Checking the discriminant **narrows** the union — TypeScript knows which members are possible in each branch. The `never` trick in `default` makes the compiler *fail* when you add a message type and forget a handler. Your protocol becomes a type that documents itself and can't drift from its handlers. Literal types (`"join"`, `-1 | 0 | 1`), template literal types, and `as const` are the supporting cast.

### 4. Generics, utility types, and `readonly`

Generics are type parameters: `function first<T>(xs: readonly T[]): T | undefined`. Use them when a function or class works over many types *and the relationship between input and output types matters*; don't use them to look clever. A typed event bus is the natural example for this project:

```ts
type GameEvents = { fired: { shooter: EntityId }; hit: { target: EntityId; damage: number } };
class Bus<E extends Record<string, unknown>> {
  on<K extends keyof E>(name: K, fn: (payload: E[K]) => void): () => void { … }
  emit<K extends keyof E>(name: K, payload: E[K]): void { … }
}
bus.emit("hit", { target, damage: 10 });   // payload shape checked against the event name
```

The built-in **utility types** — `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Extract`, `Exclude`, `ReturnType`, `Parameters` — are mapped/conditional types you should know by name. **`readonly`** on fields and `readonly T[]` on arrays turn Lab 2's "pure methods, no mutation" convention into a compiler-enforced rule for `Vector2` and snapshot data; `as const` freezes literals into readonly tuples with literal types.

### 5. Branded types, guards, and `satisfies`

`type EntityId = number` is documentation, not safety — any number is accepted. A **branded type** — `type EntityId = number & { readonly __brand: "EntityId" }` with a constructor `asEntityId(n)` — makes passing a `tick` where an `EntityId` was expected a compile error at zero runtime cost. Use it for ids, ticks, sequence numbers, and radians vs degrees if you've ever mixed them.

**Type guards** — `function isSnapshot(m: unknown): m is Snapshot` — let you write the narrowing logic once and reuse it. **`satisfies`** checks that a value matches a type without widening it: `const config = { port: 3000, host: "0.0.0.0" } satisfies ServerConfig` keeps `port` as the literal `3000` while verifying the shape.

### 6. Types stop at the wire: runtime validation

Types are erased. The `ClientMessage` type says nothing about what a malicious or buggy client *actually* sends. At every **boundary** — WebSocket message, HTTP body, environment variables, files — parse `unknown` data into a typed value with a runtime **schema validator**. [Zod](https://zod.dev) is the standard: define the schema once, **infer the TypeScript type from it** (`type ClientMessage = z.infer<typeof ClientMessage>`), and `ClientMessage.safeParse(json)` gives you a typed value or a structured error. One source of truth for shape *and* type; Lab 4's hand-written `validate()` gets deleted. For the **binary** protocol, the decoder is the validator: it must check lengths, ranges, and the version byte, and return a typed message or throw.

### 7. Running TypeScript: Vite, Node, and the toolchain

TypeScript has two jobs — **checking** (`tsc --noEmit`) and **transpiling** to JavaScript — and modern tools split them. Vite transpiles `.ts` instantly with esbuild and does *not* type-check; run `tsc --noEmit` separately (and in CI). On the server, Node **22.6+ strips types natively** with `--experimental-strip-types` (unflagged in 23.6+/24) for erasable syntax — `node server.ts` just works, no build step, as long as you avoid `enum` and parameter properties; or use `tsx` for a zero-config runner. For a **workspace**, each package has its own `tsconfig.json` extending a root one; the `shared/` package exports types the others import. A **project reference** setup (`tsc -b`) is the formal way; a flat "root tsconfig + `paths`" is often enough for three packages.

### 8. What TypeScript is not

It is not a runtime safety net (Section 6). It is not a sound type system — `any`, unchecked casts (`as`), and array index access can lie; treat `as` as a code smell requiring a comment. It does not change how JavaScript *runs*: your `this` rules, prototypes, event loop, and promises are exactly as before. And it is a **tool for design**: if a type is hard to write, the code's shape is probably wrong — listen to it.

### Prove it to yourself (editor + `tsc`, 15 minutes)

1. `const p = { x: 1, y: 2 }; const q: { x: number } = p;` compiles. `const r: { x: number; z: number } = p;` doesn't. Now try passing an *object literal* with an extra property directly — a different error. Why?
2. `const m = new Map<number, string>(); const s: string = m.get(1);` under `strict`. Fix it three ways (`!`, `??`, an `if`), and rank them.
3. Write the `ClientMessage` union and `handle` with the `never` default; add a fourth message type and watch the compiler point at the missing case.
4. `JSON.parse("…")` returns `any`. Wrap it as `unknown` and try to read `.type` — then write a zod schema and `safeParse`; hover the result type.
5. `node --experimental-strip-types x.ts` (or plain `node x.ts` on Node 24) with an `enum` inside. Read the error; replace the enum with a union of literals `as const`.

---

## Project step: type everything, keep the runtime identical

### Milestones

**M1 — Toolchain and `shared/` first.**
Root `tsconfig.base.json` from the tsconfig cheat sheet (`strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`, `module: "NodeNext"` or `"ESNext"`/`"bundler"` per package); per-package `tsconfig.json`; `npm run typecheck` = `tsc --noEmit -p .` in each workspace and at the root. Convert **`shared/` to TypeScript** first: `Vector2` with `readonly x, y`; entity kinds as a discriminated union of snapshot data (`{ kind: "ship"; … } | { kind: "bullet"; … }`); branded `EntityId`, `Tick`, `Seq`; the PRNG typed; `World.step` signatures explicit. Zero `any`. Rename `.js` → `.ts` file by file; the runtime behavior must not change (your Lab 5 determinism test proves it).

**M2 — The protocol: one schema, one type, both directions.**
`shared/protocol.ts`: zod schemas for every JSON message (client → server and server → client), types inferred from them, and a `parseClientMessage(data: unknown): ClientMessage` that returns a `Result`-style value (never throws on bad input — log and close, as in Lab 4). The binary codec becomes `encode(msg: Snapshot): ArrayBuffer` / `decode(buf: ArrayBuffer): Snapshot` with range checks and a version guard, and the JSON-vs-binary flag is a `Codec` interface with two implementations. Every `switch` on `type` or `kind` ends in the `never` default. Delete Lab 4's hand-rolled validator.

**M3 — Server and client, under `strict`.**
Convert `server/` (run with Node's native type stripping or `tsx`; avoid `enum`) and `client/` (Vite handles `.ts`; add `tsc --noEmit` to the scripts). Typed `EventEmitter` subclasses (`Room` with a typed events map — the Section 4 generic bus, or Node's `EventEmitter<T>` generic) and a typed `Bus<GameEvents>` on the client. Config from env through a zod schema with defaults (`ServerConfig`). `catch (e)` handles `unknown` properly everywhere. Reach **zero type errors** with **fewer than five `as` casts** in the whole codebase, each with a one-line justification comment. Add `typecheck` to CI (Lab 7 formalizes CI; a minimal GitHub Actions workflow running `npm ci && npm run typecheck` is enough now).

**M4 — Optional framework, and the write-up.**
*Optional but recommended:* rebuild the **lobby and HUD** in Svelte, Vue, or React with TypeScript, consuming your typed protocol and `Bus`; the canvas and game loop stay vanilla. If you do, write down what the framework gave you that `EventTarget` + DOM didn't, and what it cost (bundle size, build complexity). If you don't, say why. Either way, a README section: **"What TypeScript found"** — the concrete bugs the migration surfaced (there will be several — a `Map.get` unchecked, a message field misspelled, a nullable never handled), each with a one-liner. And: the three most interesting types you wrote, with an explanation a JavaScript-only developer could follow.

### Definition of done

- Every package is TypeScript under `strict` + `noUncheckedIndexedAccess`; `npm run typecheck` passes at the root; typecheck runs in CI.
- `shared/protocol.ts` is the single source of truth: zod schemas → inferred types → runtime parsing at every boundary; binary decoder validates.
- Discriminated unions with exhaustive `never` defaults for messages and entity kinds; branded ids; `readonly` vectors and snapshots.
- < 5 `as` casts, each justified; zero `any`.
- Determinism test still passes (runtime unchanged).
- Framework decision documented; "What TypeScript found" list; three types explained.
- Repo tagged `lab-06`.

---

## Deliverable checklist

- [ ] Root + per-package `tsconfig`; `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`; `npm run typecheck` at root; CI runs it.
- [ ] `shared/` fully typed: `readonly Vector2`, discriminated entity kinds, branded `EntityId`/`Tick`/`Seq`.
- [ ] `protocol.ts`: zod schemas, inferred types, `parseClientMessage` returning a result; hand validator deleted.
- [ ] Binary codec typed with range/version checks; `Codec` interface with JSON and binary implementations.
- [ ] Exhaustive `switch` + `never` on every `type`/`kind` dispatch.
- [ ] Typed events (`Room`, client `Bus<GameEvents>`); zod-validated `ServerConfig`; `unknown` in every `catch`.
- [ ] Zero `any`; < 5 justified `as`; determinism test green.
- [ ] Framework decision + "What TypeScript found" + three explained types in README.
- [ ] Git tag `lab-06`.

---

## Reflection — explain it at the whiteboard

1. What does "structural typing" mean? Give an example where two unrelated classes are interchangeable in TypeScript and would not be in C# or Java.
2. `any` vs `unknown` — what can you do with each? Where does `unknown` enter your system, and how does it leave?
3. Write a discriminated union for three message types and a handler with an exhaustive `switch`. What exactly does the `never` default catch, and when?
4. Types are erased at runtime — so what stops a malicious client sending `{ type: "input", turn: 1e9 }`? Where does that check live and why there?
5. What is a branded type? Show the definition and a bug it prevents in your code.
6. When should a function be generic? Show your typed event bus and explain how `K extends keyof E` and `E[K]` link the name to the payload.
7. Why does Vite not type-check? How do you get checking anyway, and where does it run?
8. Name three bugs TypeScript found in your migration. Were any of them *not* type errors in the naive sense (e.g., a missing `undefined` check)?
9. When is `as` acceptable? Explain each of your casts.

---

## Stretch

Make the **binary protocol layout type-driven**: describe each message's fields as a `const` schema (`[["tick", "u32"], ["x", "f32"], …] as const`) and derive both the TypeScript message type (via mapped and conditional types) and the `DataView` encoder/decoder from that one definition — so adding a field changes the type and the codec together. Then add **`tsc -b` project references** across the workspaces with incremental builds, and measure typecheck time before and after. Finally, write **five Type Challenges** of your own drawn from the codebase (e.g., "extract all message types whose payload has a `seq`") and solve them.

---

## Resources

**Watch**

- Fireship — [TypeScript in 100 Seconds](https://www.youtube.com/watch?v=zQnBQ4tB3ZA). Two minutes of orientation, if you've never touched it.
- Franziska Hinkelmann — [JavaScript engines: how do they even? (JSConf EU 2017)](https://www.youtube.com/watch?v=p-iiEDtpy6I) — optional preview for Lab 7, relevant here because it explains why *type stability* (objects keeping the same shape) makes JavaScript fast — which TypeScript nudges you toward.

**Read**

- [The TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — "The Basics" through "Object Types," then "Narrowing," "Generics," and "Modules." The official reference; well written; the spine of Sections 1–5.
- Matt Pocock — [Total TypeScript Essentials](https://www.totaltypescript.com/books/total-typescript-essentials) (free online book). The modern, opinionated path through the language; chapters on unions and narrowing, objects, `unknown`/`never`, and "Designing your types." Also his [tsconfig cheat sheet](https://www.totaltypescript.com/tsconfig-cheat-sheet) and [Discriminated Unions are a Frontend Dev's Best Friend](https://www.totaltypescript.com/discriminated-unions-are-a-devs-best-friend).
- Basarat Ali Syed — [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) (free). Older but excellent on *why*: structural typing, type guards, `never`, and the "types stop at the runtime" boundary.
- [Zod documentation](https://zod.dev). Schemas, `z.infer`, `safeParse`, discriminated unions (`z.discriminatedUnion`). Section 6.
- Node.js — [Running TypeScript natively](https://nodejs.org/en/learn/typescript/run-natively). Type stripping, what's erasable, and the limits.
- [Type Challenges](https://github.com/type-challenges/type-challenges) — when you want to go deeper; do the "easy" set and a few "medium" (e.g., `Pick`, `Readonly`, `TupleToObject`, `DeepReadonly`).
