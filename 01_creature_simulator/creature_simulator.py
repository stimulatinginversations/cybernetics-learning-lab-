"""
Project 01: Creature Simulator

This program is a tiny simulation of a creature with internal state.

The goal is not to build a realistic animal. The goal is to practice beginner
Python while seeing how a system can change over time.
"""


def clamp(value, smallest, largest):
    """Keep a number between a smallest and largest allowed value."""
    if value < smallest:
        return smallest
    if value > largest:
        return largest
    return value


def show_status(name, energy, hunger):
    """Print the creature's current internal state."""
    print()
    print(f"{name}'s status")
    print(f"Energy: {energy}")
    print(f"Hunger: {hunger}")


def choose_action(turn):
    """Choose the creature's next action using simple rules."""
    if turn % 3 == 0:
        return "eat"
    if turn % 2 == 0:
        return "rest"
    return "explore"


def update_state(action, energy, hunger):
    """Return the new energy and hunger after one action."""
    if action == "eat":
        print("The creature eats some food.")
        energy = energy - 1
        hunger = hunger - 3
    elif action == "rest":
        print("The creature rests quietly.")
        energy = energy + 2
        hunger = hunger + 1
    elif action == "explore":
        print("The creature explores its environment.")
        energy = energy - 2
        hunger = hunger + 2

    energy = clamp(energy, 0, 10)
    hunger = clamp(hunger, 0, 10)

    return energy, hunger


def can_continue(energy, hunger):
    """Decide whether the simulation should keep running."""
    return energy > 0 and hunger < 10


def main():
    name = "Ada"
    energy = 8
    hunger = 3
    turn = 1

    print("Creature Simulator")
    print("Watch how a simple internal state changes over time.")

    while turn <= 10 and can_continue(energy, hunger):
        print(f"\n--- Turn {turn} ---")
        show_status(name, energy, hunger)

        action = choose_action(turn)
        print(f"Action: {action}")

        energy, hunger = update_state(action, energy, hunger)
        turn = turn + 1

    print("\nSimulation ended.")
    show_status(name, energy, hunger)

    if energy == 0:
        print(f"{name} ran out of energy.")
    elif hunger == 10:
        print(f"{name} became too hungry.")
    else:
        print(f"{name} completed all turns.")


if __name__ == "__main__":
    main()
