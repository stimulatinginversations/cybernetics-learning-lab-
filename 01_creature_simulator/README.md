# Project 01 - Creature Simulator

## Purpose

This first project introduces the idea that a program can represent a small
system with an internal state.

The creature in this project has:

- a name
- an energy level
- a hunger level
- a simple rule for choosing an action

That may sound like a toy, but it is the beginning of an important idea in
cybernetics and robotics:

> An intelligent system is not just a list of commands. It has a condition,
> senses or estimates that condition, acts, and changes over time.

## Concepts introduced

This project uses only beginner Python ideas:

- variables
- functions
- `if`, `elif`, and `else`
- `while` loops
- returning values from functions
- updating state over time

No classes, external libraries, files, graphics, or advanced Python features are
needed yet.

## How to run the project

From the repository root, run:

```bash
python3 01_creature_simulator/creature_simulator.py
```

You should see the creature act for several turns.

## What to notice

The program repeats this basic cycle:

1. Show the creature's current state.
2. Choose an action.
3. Update the creature's state.
4. Check whether the simulation should continue.

This is an early version of the same pattern used in adaptive systems:

```text
sense state -> choose action -> act -> state changes -> repeat
```

Later projects will make this loop more realistic by adding feedback,
controllers, disturbances, memory, prediction, and learning.

## Your role as the learner

Do not treat the starter program as something to memorize.

Instead:

1. Run it.
2. Change one number.
3. Run it again.
4. Predict what will happen before reading the output.
5. Explain the result in your own words.

That habit is more important than typing the code perfectly.

## Understanding checks

Before moving on, try to answer these questions:

1. Which variables represent the creature's internal state?
2. Which function decides what the creature does next?
3. Which function changes the creature's state?
4. Why does the program need a loop?
5. What condition causes the simulation to stop?

## Connection to cybernetics

Cybernetics studies systems that regulate themselves through information and
action.

This creature does not truly regulate itself yet, but it already has the pieces
we will need:

- **state**: energy and hunger
- **action**: eat, rest, or explore
- **change over time**: each turn updates the state
- **rules**: simple logic decides what happens

In later projects, the creature will become more controller-like by comparing
its current state with a desired state and acting to reduce the difference.
