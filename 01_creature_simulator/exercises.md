# Exercises for Project 01

Use these exercises after you have run `creature_simulator.py` at least once.

Try to make each change yourself before asking for a solution.

## Exercise 1 - Change the starting state

In `main()`, change:

```python
energy = 8
hunger = 3
```

Try these experiments:

1. Start with `energy = 3`.
2. Start with `hunger = 8`.
3. Start with both values low.

Before each run, predict:

- Will the creature survive all 10 turns?
- Which value will become dangerous first?

## Exercise 2 - Add a new action

Add a new action called `"play"`.

Suggested rule:

- playing costs 1 energy
- playing increases hunger by 1

Questions:

1. Where should the new action be chosen?
2. Where should the new action change the creature's state?
3. What happens if `choose_action()` returns `"play"` but `update_state()` does
   not handle it?

## Exercise 3 - Change the creature's decision rule

Right now the creature chooses actions mostly based on the turn number.

Try changing `choose_action()` so the creature eats when hunger is high.

Hint: you will need to pass `hunger` into the function:

```python
action = choose_action(turn, hunger)
```

Then change the function definition:

```python
def choose_action(turn, hunger):
```

This is an important step toward feedback control because the creature begins to
choose actions based on its own state.

## Exercise 4 - Write observations

Create a small note for yourself:

```text
What changed?
What did I expect?
What actually happened?
What did I learn?
```

Good engineers keep notes because systems can behave differently than expected.

## Exercise 5 - Explain the loop

In your own words, explain this part of the program:

```python
while turn <= 10 and can_continue(energy, hunger):
```

Use plain English. You do not need mathematical language yet.

## Stretch challenge - First feedback rule

Modify the creature so it follows this priority:

1. If hunger is 7 or higher, eat.
2. Else if energy is 3 or lower, rest.
3. Otherwise, explore.

This is the first version of a control policy:

```text
look at state -> choose action that protects the system
```

That idea will return in thermostats, robots, and adaptive controllers.
