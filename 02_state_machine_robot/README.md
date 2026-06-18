# 02 - State Machine Robot

## Purpose

This project introduces **finite state machines (FSMs)** as a way to organise robot behaviour.

Project 01 showed that a system can hold internal variables (hunger, energy) and update them over time. Project 02 adds a new layer: the robot switches between named **behaviour modes** based on what it senses.

That pattern appears everywhere in engineering:

- Robot navigation (patrol, avoid, dock)
- Game AI (idle, chase, flee)
- User interfaces (loading, ready, error)
- Industrial controllers (run, fault, shutdown)

## Concepts

### Finite State Machine

An FSM has:

1. **States** — discrete modes of behaviour (`IDLE`, `PATROL`, `AVOID`, ...)
2. **Events** — signals that can trigger a change (`OBSTACLE_DETECTED`, `BATTERY_LOW`, ...)
3. **Transitions** — rules that map `(current_state, event)` to a new state
4. **Actions** — what the robot does while it remains in a state

Only one state is active at a time. Behaviour is predictable because transitions are explicit.

### Behaviour Switching

Instead of one large `if/elif` block that mixes every situation, each state owns a small piece of logic. The robot **senses**, **decides** (via transitions), then **acts**.

### Decision Making

Decisions are not magic. They are table lookups:

| Current State | Event              | Next State   |
|---------------|--------------------|--------------|
| PATROL        | OBSTACLE_DETECTED  | AVOID        |
| PATROL        | BATTERY_LOW        | SEEK_CHARGE  |
| AVOID         | PATH_CLEAR         | PATROL       |
| SEEK_CHARGE   | AT_CHARGER         | CHARGING     |
| CHARGING      | BATTERY_FULL       | IDLE         |

## Files

| File                 | Role                                      |
|----------------------|-------------------------------------------|
| `state_machine.py`   | Reusable FSM engine                       |
| `environment.py`     | Grid world, obstacles, charger            |
| `robot.py`           | Robot body, sensors, states, and actions  |
| `main.py`            | Simulation loop and ASCII visualisation   |

## How to Run

From this directory:

```bash
python main.py
```

Run more ticks:

```bash
python main.py --steps 50
```

You should see the robot:

1. Start in `IDLE`, then enter `PATROL`
2. Turn in `AVOID` when it detects obstacles
3. Switch to `SEEK_CHARGE` when battery is low
4. Move to the charger (`+` on the map) and enter `CHARGING`
5. Return to `IDLE` when the battery is full

## How the Loop Works

Each simulation tick:

1. **Sense** — read obstacles, charger proximity, battery level
2. **Emit events** — translate readings into FSM events
3. **Transition** — update the active state if a rule matches
4. **Act** — run the action for the current state (move, turn, charge, rest)

This is a basic **sense → decide → act** cycle used in robotics and cybernetics.

## State Diagram

```text
                    START_PATROL
         +--------------------------------+
         |                                v
      +------+   OBSTACLE_DETECTED    +--------+
      | IDLE | ---------------------> | AVOID  |
      +------+                         +--------+
         ^                                  |
         | BATTERY_FULL                     | PATH_CLEAR
         |                                  v
    +----------+   AT_CHARGER          +--------+
    | CHARGING | <--------------------- | PATROL |
    +----------+                        +--------+
         ^                                  |
         |                                  | BATTERY_LOW
         |                                  v
         |                             +-------------+
         +-----------------------------| SEEK_CHARGE |
                                       +-------------+
```

## Experiments to Try

After you understand the code, modify the system yourself:

1. Add a `STUCK` state when the robot spins in place too long
2. Change `BATTERY_LOW_THRESHOLD` and observe earlier or later charging
3. Add a second charger and let the robot pick the nearest one
4. Log how many ticks are spent in each state
5. Replace ASCII output with a simple matplotlib animation (optional)

## Lessons Learned

- Explicit states make complex behaviour easier to reason about than one giant conditional tree.
- Separation of **sensing**, **transition logic**, and **actions** mirrors real control architectures.
- The same FSM engine can control different robots by changing states, events, and actions.
- Finite state machines are a foundation for later projects involving feedback, goals, and adaptation.

## Connection to the Roadmap

| Project | New Idea                                      |
|---------|-----------------------------------------------|
| 01      | Internal variables change over time           |
| 02      | Named behaviour modes switch by rules         |
| 03      | Continuous feedback loops (thermostat)        |
| 06      | Goal-directed homeostasis                     |

## Next Step

Move on to **03 - Thermostat Controller** to introduce continuous feedback and error signals.
