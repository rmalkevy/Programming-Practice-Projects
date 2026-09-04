# Lab 02 — Objects, Prototypes, and `this`: The Entity Model

> "JavaScript doesn't have classes. It has objects that delegate to other objects, and a `class` keyword that politely pretends otherwise."

**Weeks:** 3–4 · **Language focus:** objects as property bags, the prototype chain, constructor functions and `class` sugar, the four rules of `this`, composition over inheritance, `Map`/`Set`/`WeakMap`, destructuring and spread, iterables and generators · **Project step:** ships, bullets, obstacles; an entity manager; collisions; shooting and respawn · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 01](lab-01-event-loop-and-game-loop.md)

---

## This lab's feature

Your game has one ship, described as a plain object. Now it needs many things — ships, bullets, asteroids, pickups, explosions — that share behavior (position, velocity, collision radius, `update`, `draw`) but differ in the details. Every language has an answer to "how do many things share behavior." JavaScript's answer is unlike anything in C++, Java, or Python, and understanding it is what separates people who *use* JavaScript from people who *know* it.

The answer is **prototypes**: objects that delegate property lookups to other objects. The `class` keyword, added in 2015, is a friendlier syntax over exactly that mechanism — nothing more. And `this`, the most misunderstood word in the language, follows four simple rules that you'll be able to recite by the end of the lab. Along the way you'll adopt **composition over inheritance** — the design principle that game programmers arrived at decades ago and that JavaScript's flexibility makes natural — and you'll meet JavaScript's *iteration protocol*, which is the same idea as Python's (and lets your entity collection work in a `for…of`).

---

## Theory

### 1. Objects are property bags; properties are looked up at runtime

A JavaScript object is a dynamic map from string (or Symbol) keys to values, plus a hidden link to another object — its **prototype**. `obj.x` means: look for own property `x`; if absent, look in `obj`'s prototype; then in *its* prototype; and so on up the **prototype chain** until `null`. Method calls are just property lookups that happen to find a function.

That's it. That's the entire object model. Everything else — constructors, `class`, `extends`, `super`, "inheritance" — is a way of *setting up chains*. Lydia Hallie's diagrams make this concrete; MDN's [Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain) is the reference.

You can build the chain by hand: `const bullet = Object.create(entityProto)` creates an empty object whose prototype is `entityProto`. `Object.getPrototypeOf(bullet) === entityProto`. Add `bullet.x = 3` and it's an *own* property; `bullet.update` (if defined on `entityProto`) is *inherited* — found by delegation, not copied. Change `entityProto.update` and every object delegating to it sees the change immediately. There's no copying, ever.

### 2. Constructor functions and `class`: two syntaxes, one mechanism

Before 2015:

```js
function Entity(x, y) { this.x = x; this.y = y; }       // a constructor: called with `new`
Entity.prototype.update = function (dt) { this.x += this.vx * dt; };
const e = new Entity(0, 0);   // new: create {}, set its prototype to Entity.prototype, call Entity with this = {}
```

`new F()` does three things: creates an object, sets its prototype to `F.prototype`, and calls `F` with `this` bound to the new object (returning it unless `F` returns another object). Every function has a `.prototype` property for exactly this purpose. `e.update` is found on `Entity.prototype`.

After 2015:

```js
class Entity {
  constructor(x, y) { this.x = x; this.y = y; }
  update(dt) { this.x += this.vx * dt; }
}
```

**Identical result.** `typeof Entity === "function"`; `Entity.prototype.update` exists; `new Entity()` builds the same chain. `class` adds real conveniences — methods are non-enumerable, class bodies are strict, calling without `new` throws, `extends` sets up the *two* chains correctly (instances → `Sub.prototype` → `Super.prototype`, and `Sub` → `Super` for statics), `super` works — plus features with no pre-2015 equivalent: **private fields** (`#hp`, truly inaccessible from outside), static blocks, and accessors (`get radius()`). Use `class`. But know what it compiles to; interviewers ask, and debugging inheritance bugs requires it.

### 3. `this`: four rules, applied in order

`this` is not "the object the method belongs to." It is determined **at call time**, by *how* the function was called. Kyle Simpson's rules, in precedence order:

1. **`new` binding** — `new F()`: `this` is the newly created object.
2. **Explicit binding** — `f.call(obj)`, `f.apply(obj)`, or `f.bind(obj)()`: `this` is `obj`. `bind` returns a permanently bound copy.
3. **Implicit binding** — `obj.f()`: `this` is `obj`, the object to the left of the dot *at the call site*.
4. **Default binding** — plain `f()`: `this` is `undefined` in strict mode (which modules and classes always are), `globalThis` otherwise.

And the exception that makes it all workable: **arrow functions have no `this` of their own.** They capture `this` lexically from the enclosing scope, exactly like any other variable in a closure. `bind`/`call`/`apply` can't change it.

The bug you *will* hit this lab: `button.addEventListener("click", ship.fire)` — you passed the function, not the call; the event system calls it with `this` = the button (or `undefined`). Fixes: `() => ship.fire()`, `ship.fire.bind(ship)`, or define `fire = () => {…}` as a class field (an arrow per instance — costs memory, reads cleanly). Know all three and their trade-offs.

### 4. Composition over inheritance

The tempting design: `Entity → MovingEntity → Ship → PlayerShip`, `Entity → MovingEntity → Bullet`. It breaks the moment you need a bullet that homes (moving + targeting), a stationary turret that shoots (shooting but not moving), or a ship that's also a pickup. Deep hierarchies fossilize; the game changes weekly.

The alternative game developers converged on (Nystrom's [Component](https://gameprogrammingpatterns.com/component.html) chapter): an entity is a **bag of small, independent behaviors** — a position component, a physics component, a collider, a weapon, a health pool — and systems operate on whatever has the components they need. In JavaScript you can do this lightly without a full ECS framework:

- **Mixins via object spread / `Object.assign`:** `Object.assign(Ship.prototype, Movable, Shooter)` copies methods onto a prototype; or `const makeShip = () => ({ ...position(), ...physics(), ...weapon(), kind: "ship" })` builds plain objects with factory functions.
- **Explicit components as fields:** `ship.body = new Body(...)`, `ship.weapon = new Weapon(...)`; systems check `if (e.body)`.
- **Behavior as data:** `{ kind: "bullet", ttl: 2, damage: 10 }` and a `switch` in the update system. Boring, fast, easy to serialize — which matters a lot in Lab 5.

Rule: **inherit at most one level** (`class Ship extends Entity` is fine); anything richer is composition. The Fun Fun Function talk demonstrates why in ten minutes.

### 5. `Map`, `Set`, `WeakMap`, and iteration

Don't use plain objects as dictionaries for entity storage. `Map` has any key type (numbers stay numbers), a real `.size`, guaranteed insertion order, no prototype pollution (`obj["constructor"]` is a real bug people hit), and is faster for frequent add/remove. **`Map<id, Entity>`** is your entity store; **`Set<Entity>`** for tags or pending-removal lists; **`WeakMap`** to attach data to objects without preventing garbage collection (e.g., per-DOM-element caches).

`for…of` works on anything **iterable** — arrays, strings, `Map`, `Set`, and any object with a `[Symbol.iterator]()` method returning an iterator (`{ next() → { value, done } }`). **Generators** (`function*` + `yield`) are the shortcut for writing iterators, exactly as in Python:

```js
class World {
  #entities = new Map();
  *[Symbol.iterator]() { yield* this.#entities.values(); }
  *ofKind(kind) { for (const e of this) if (e.kind === kind) yield e; }
}
for (const bullet of world.ofKind("bullet")) { … }   // lazy; no intermediate array
```

Destructuring and spread are the ergonomics layer: `const { x, y } = ship`; `const next = { ...ship, x: ship.x + 1 }` (shallow copy — nested objects are shared); `[a, b] = [b, a]`; rest parameters. Learn to read them at a glance — modern codebases are made of them.

### 6. Mutation, copies, and equality

Objects are **reference types**: `a === b` is identity, not structural equality; assignment copies the reference. `{ ...obj }` and `Array.from` are shallow copies; `structuredClone(obj)` is a deep copy (and the right tool for snapshotting state). `Object.freeze` makes an object shallowly immutable (silently ignored in sloppy mode, throws in strict — another reason modules are strict). For the simulation, decide deliberately: **mutate in place** (fast, cache-friendly, the norm in games — your `integrate` from Lab 1 does this) or **produce new state** (easier to reason about and snapshot). This lab uses in-place mutation with an explicit *previous-state copy* for interpolation; know what you chose and why.

### Prove it to yourself (console, 10 minutes)

1. `const a = {}; const b = Object.create(a); a.hello = 1; b.hello` → then `b.hasOwnProperty("hello")` and `Object.getPrototypeOf(b) === a`. Now `a.hello = 2; b.hello`. No copying happened — prove it.
2. `class A { m() { return this; } }; const a = new A(); const m = a.m; m()` → what and why? `m.call(a)`? Now make `m` an arrow class field and repeat.
3. `class B extends A {}` — inspect `Object.getPrototypeOf(B.prototype) === A.prototype` and `Object.getPrototypeOf(B) === A`. Draw both chains.
4. `const o = { "1": "x" }; const m = new Map([[1, "x"]]); o[1], m.get("1")` — explain the difference. Then `const k = {}; o[k] = 1; Object.keys(o)`.
5. A generator that yields the Fibonacci numbers forever; take the first 10 with a `for…of` and `break`. Then `[...gen()]` — what happens, and why is this Lab 1's "don't block the loop" in disguise?

---

## Project step: entities, bullets, and collisions

### Milestones

**M1 — `Vector2` and a base `Entity`.**
`sim/vector.js`: a `Vector2` class with `add`, `sub`, `scale`, `length`, `normalize`, `rotate`, `dot`, `static fromAngle` — **pure methods returning new vectors** (so `a.add(b)` never mutates `a`), plus `addInPlace`-style variants for hot paths if you measure the need. `sim/entity.js`: `class Entity` with `id`, `pos`, `vel`, `angle`, `radius`, `alive`, `kind`, `update(dt)`, and a private `#id` counter via a static field. Refactor Lab 1's ship into `class Ship extends Entity` — one level, no more.

**M2 — The world: a `Map`-based entity manager.**
`sim/world.js`: `class World` holding `#entities: Map<number, Entity>`, with `spawn(e)`, `despawn(id)` (deferred: mark dead, sweep at end of step — mutating a `Map` while iterating it is legal but a source of subtle bugs), `get(id)`, `[Symbol.iterator]`, and `*ofKind(kind)`. `World.step(dt, inputs)` updates all entities, resolves collisions, sweeps the dead. Add `Bullet` (with a time-to-live) and `Asteroid`/`Obstacle` (drifting, bouncing). `Ship.fire()` spawns a bullet from the ship's nose with inherited velocity — and this is where you hit the `this` bug from Section 3 if you wire a keyboard handler naively. Document it when you do.

**M3 — Collisions, damage, respawn.**
`sim/collision.js`: circle–circle tests; a naive O(n²) pass is fine for now (Lab 7 measures it), but write it as a separate *system* that takes the world and emits `(a, b)` pairs so it can be swapped for a spatial hash later. Bullets damage ships and asteroids; ships have `#hp` (private field) with a public `get hp()`; a destroyed ship spawns an explosion entity (particles — many short-lived objects; remember this for Lab 7) and respawns after 2 s at a random safe spot. Score on the HUD.

**M4 — Composition, and a design write-up.**
Add two features that would break a class hierarchy, and implement them with composition instead: (a) a **homing** behavior that can attach to a bullet *or* an asteroid, and (b) a **pickup** (shield / rapid fire) that is stationary and collidable but not a ship. Use whichever technique from Section 4 you prefer — mixins, component fields, or behavior-as-data — and write a README section (≤ 1 page) comparing what the inheritance version would have looked like and why you chose your approach. Include a diagram of the prototype chains in your final design (`Object.getPrototypeOf` all the way up).

### Definition of done

- `Vector2`, `Entity`, `Ship`, `Bullet`, `Asteroid`, `Pickup`, `Explosion` exist; inheritance is at most one level deep.
- `World` stores entities in a `Map`, is iterable, exposes `ofKind` as a generator, and sweeps dead entities safely.
- Shooting works; the `this` bug was encountered (or deliberately demonstrated) and fixed, with the fix explained in the README.
- Collisions, damage with private `#hp`, explosions, respawn, and score.
- Homing and pickups implemented via composition; the design write-up and prototype-chain diagram are in the README.
- Repo tagged `lab-02`.

---

## Resources

**Watch**

- Fun Fun Function — [Prototypes in JavaScript (15 min)](https://www.youtube.com/watch?v=riDVvXZ_Kb4). Builds the prototype chain from `Object.create` up, live, with no `class` in sight. Watch first so `class` has something to be sugar *for*.
- Fun Fun Function — [Composition over Inheritance (11 min)](https://www.youtube.com/watch?v=wfMtDGfHWpA). The dog-that-can-also-clean-the-house problem; the clearest short argument for Section 4, in JavaScript.

**Read**

- Lydia Hallie — [JavaScript Visualized: Prototypal Inheritance](https://dev.to/lydiahallie/javascript-visualized-prototypal-inheritance-47co). Animated diagrams of exactly what `new`, `class`, and `extends` build. Ten minutes; read before Section 2.
- javascript.info — [Prototypes, inheritance](https://javascript.info/prototypes) (all four articles) and [Classes](https://javascript.info/classes) (all articles, especially "Class inheritance" and "Private and protected properties"). This is the textbook for the lab.
- MDN — [Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain) (the reference), [`this`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this) (read the whole page once), and [Iterators and generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_generators).
- Kyle Simpson — [*You Don't Know JS Yet: Objects & Classes*](https://github.com/getify/You-Dont-Know-JS/blob/2nd-ed/objects-classes/README.md). Chapters 1–4 for objects and `this` in depth; the source of the four rules.
- Robert Nystrom — [Game Programming Patterns: Component](https://gameprogrammingpatterns.com/component.html). Why game engines abandoned deep hierarchies, with code. The design rationale for M4.

---

## Deliverable checklist

- [ ] `Vector2` with pure methods; `Entity` base with private static id counter; `Ship extends Entity` (one level).
- [ ] `World` over `Map`, iterable via `[Symbol.iterator]`, `*ofKind`, deferred despawn sweep.
- [ ] `Bullet` (TTL), `Asteroid`, `Explosion` (particles), `Pickup`; `Ship.fire()`.
- [ ] The `this` bug documented with the fix chosen and alternatives listed.
- [ ] Circle collision system as a swappable function; damage via `#hp`; respawn; score HUD.
- [ ] Homing and pickups via composition; ≤ 1-page design write-up with prototype-chain diagram.
- [ ] Git tag `lab-02`.

---

## Reflection — explain it at the whiteboard

1. Draw the prototype chain for `const s = new Ship()` where `class Ship extends Entity`. Include `Ship`, `Entity`, `Ship.prototype`, `Entity.prototype`, `Object.prototype`, and `Function.prototype`. What does `s.update` do, step by step?
2. What exactly does `new` do? Write `new` as a function using `Object.create` and `.call`.
3. State the four `this` rules in precedence order. What's `this` in `setTimeout(ship.fire, 100)`? Give three fixes and one downside of each.
4. Why do arrow functions ignore `.bind`? What are they good for and where are they wrong (hint: methods on prototypes)?
5. Why is `class` "just sugar"? Name three things `class` does that the constructor-function version doesn't.
6. Why `Map` over a plain object for the entity store? Give three concrete reasons.
7. What is an iterable? What is an iterator? Show how `for…of` uses both, and why `[...world]` could be a problem in a game loop.
8. Argue for composition over inheritance using your homing-bullet-and-homing-asteroid case. What would the hierarchy have had to look like?

---

## Stretch

Replace the ad-hoc composition with a **tiny data-oriented ECS**: components stored as parallel typed arrays (`Float32Array` for positions and velocities), entities as integer indices, systems as functions over ranges. Measure `World.step` time at 5,000 entities against the object-based version (you'll revisit this in Lab 7 with a profiler — write the number down now). Then implement a **spatial hash** for the collision system and show the O(n²) → ~O(n) change on the same benchmark.
