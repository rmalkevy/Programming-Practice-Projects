# Lab 02: Wolfenstein-like Ray Casting Engine

## Goal

Create a simple pseudo-3D engine inspired by early games like **Wolfenstein 3D**.

The goal is not to build a full game, but to understand how a **2D map** can be transformed into a **first-person pseudo-3D view** using **ray casting**.

You will practice:

- working with 2D arrays;
- basic geometry and trigonometry;
- keyboard input;
- collision detection;
- rendering loop;
- simple software architecture.

---

## Idea

The world is stored as a 2D grid:

```txt
1111111111
1000000001
1011110101
1000010101
1011010001
1000000001
1111111111
```

Where:

- `1` means wall;
- `0` means empty space.

The player is located somewhere inside the map and looks in some direction.

For every vertical column of the screen, the program sends a ray from the player’s position. When the ray hits a wall, the distance to that wall is used to calculate how tall the wall should look on the screen.

Closer wall = taller vertical slice. Farther wall = smaller vertical slice.

---

## Ray Casting Engine Workflow

```mermaid
flowchart TD
    A[Start application] --> B[Initialize map and player]
    B --> C[Main loop]
    C --> D[Read keyboard input]
    D --> E[Update player position and rotation]
    E --> F[Check wall collision]
    F --> G[Cast rays across field of view]
    G --> H[Find wall hit for each ray]
    H --> I[Calculate distance to wall]
    I --> J[Calculate wall slice height]
    J --> K[Render pseudo-3D view]
    K --> L[Render minimap]
    L --> M[Display frame]
    M --> N{Exit?}
    N -- No --> C
    N -- Yes --> O[Close application]
```

---

## Task

Implement a small ray casting application where the user can move inside a 2D maze and see a pseudo-3D view.

Your application must have:

- a 2D map;
- a player position and direction;
- keyboard movement;
- collision detection with walls;
- ray casting;
- pseudo-3D wall rendering;
- a simple minimap or debug 2D view.

---

## Functional Requirements

### 1. Map

The map must be stored as a 2D array, string array, or loaded from a file.

Requirements:

- `1` means wall;
- `0` means empty space;
- the player cannot walk through walls;
- map borders should be closed by walls.

### 2. Player Movement

The player must be able to:

- move forward;
- move backward;
- rotate left;
- rotate right.

Optional:

- strafe left/right;
- mouse rotation;
- sprint mode.

### 3. Ray Casting

The program must cast multiple rays from the player’s position.

Each ray should:

- have its own angle;
- move through the map until it hits a wall;
- calculate the distance to the wall;
- return information needed for rendering.

Minimum requirement: cast at least **60 rays** per frame.

### 4. Rendering

The application must draw a pseudo-3D view.

Requirements:

- close walls look taller;
- far walls look smaller;
- the screen updates when the player moves;
- wall slices are drawn based on ray distances.

### 5. Minimap

Add a simple minimap or debug view.

It should show:

- map walls;
- empty cells;
- player position;
- player direction;
- optionally, visible rays.

---

## Suggested Project Structure

```txt
ray-casting-engine/
  README.md
  src/
    main.*
    GameMap.*
    Player.*
    Raycaster.*
    Renderer.*
    InputHandler.*
  maps/
  assets/
```

---

## Difficulty Levels

### Basic

Implement:

- hardcoded map;
- forward/backward movement;
- left/right rotation;
- collision detection;
- simple ray casting;
- pseudo-3D wall rendering;
- basic minimap.

### Standard

Implement everything from Basic plus:

- configurable field of view;
- strafe movement;
- visible rays on minimap;
- distance-based wall shading;
- fish-eye correction;
- map loaded from a file.

### Advanced

Implement some of the following:

- textured walls;
- doors;
- different wall types;
- simple sprites or enemies;
- mouse control;
- multiple maps;
- optimized DDA ray casting.

---

## Implementation Plan

1. Create a 2D map.
2. Draw the map as a simple 2D view.
3. Add player position and direction.
4. Add keyboard movement.
5. Add collision detection.
6. Cast one ray and find where it hits a wall.
7. Cast many rays across the field of view.
8. Draw rays on the minimap.
9. Convert ray distances into wall heights.
10. Draw vertical wall slices.
11. Add simple floor and ceiling.
12. Refactor the code into modules.
13. Write README and prepare demo.

---

## Testing

Test at least the following:

- wall collisions work
- rays hit walls
- distance is calculated
- program does not crash near map borders
- map can be changed

Automated tests are recommended but not strictly required. If you do not write automated tests, describe manual test cases in `README.md`.

---

## Demo

During the demo, show:

- move inside the map
- show collision with walls
- show pseudo-3D rendering
- show minimap
- explain how one ray finds a wall

---

## README Requirements

Your repository must include `README.md` with:

1. Project name.
2. Short description.
3. Selected difficulty level.
4. Technologies used.
5. How to run the project.
6. Main features.
7. Short explanation of the main algorithm or architecture.
8. Screenshots or demo link, if possible.
9. Known problems or limitations.

---

## Defense Questions

Be ready to answer:

1. How is your map stored?
2. How do you check wall collisions?
3. What is a ray?
4. How do you calculate ray direction?
5. Why do close walls look taller?
6. What is field of view?
7. What is fish-eye distortion?
8. What does your game loop do?

---

## Evaluation Criteria

| Criterion | Points |
|---|---:|
| Map representation | 10 |
| Player movement and collision detection | 15 |
| Ray casting logic | 20 |
| Pseudo-3D rendering | 20 |
| Minimap/debug view | 10 |
| Code structure | 10 |
| README | 10 |
| Demo and defense | 5 |
| **Total** | **100** |

---

## Expected Result

At the end of this lab, you should have a working project called **Wolfenstein-like Ray Casting Engine**.

The project should demonstrate both programming skills and the ability to structure, explain, and present a small but non-trivial software system.
