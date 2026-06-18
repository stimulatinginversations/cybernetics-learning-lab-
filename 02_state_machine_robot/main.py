"""
Run the state machine robot simulation.

Usage:
  python main.py
  python main.py --steps 40
"""

import argparse

from robot import Robot


def render_grid(robot: Robot) -> str:
  """Build a simple ASCII map of the world."""
  env = robot.environment
  lines: list[str] = []

  for y in range(env.height):
    row = []
    for x in range(env.width):
      if (x, y) == (robot.x, robot.y):
        symbol = {"north": "^", "east": ">", "south": "v", "west": "<"}[robot.direction]
        row.append(symbol)
      elif env.is_charger(x, y):
        row.append("+")
      elif env.is_obstacle(x, y):
        row.append("#")
      else:
        row.append(".")
    lines.append(" ".join(row))

  return "\n".join(lines)


def run_simulation(steps: int) -> None:
  robot = Robot(x=5, y=5, direction="east")

  print("State Machine Robot")
  print("Legend: robot=^>v<  charger=+  obstacle=#  empty=.")
  print()

  for tick in range(1, steps + 1):
    result = robot.step()

    print(f"--- Tick {tick} ---")
    print(f"State: {result['state']}")
    print(f"Position: {result['position']}  Direction: {result['direction']}")
    print(f"Battery: {result['battery']}")

    if result["events"]:
      print(f"Events: {', '.join(result['events'])}")

    if result["transitions"]:
      for old_state, new_state in result["transitions"]:
        print(f"Transition: {old_state} -> {new_state}")

    print(render_grid(robot))
    print()


def main() -> None:
  parser = argparse.ArgumentParser(description="Simulate a finite state machine robot.")
  parser.add_argument("--steps", type=int, default=30, help="Number of simulation ticks.")
  args = parser.parse_args()
  run_simulation(args.steps)


if __name__ == "__main__":
  main()
