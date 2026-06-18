"""
A simple 2D world for the state machine robot.

The robot senses obstacles, a charging station, and its own battery level.
"""

from dataclasses import dataclass


@dataclass
class SensorReading:
  """What the robot can observe in one timestep."""

  obstacle_ahead: bool
  at_charger: bool
  battery_low: bool
  battery_full: bool


class Environment:
  """A small grid world with walls, obstacles, and a charger."""

  def __init__(self, width: int = 10, height: int = 10) -> None:
    self.width = width
    self.height = height
    self.obstacles: set[tuple[int, int]] = {
      (3, 2),
      (3, 3),
      (3, 4),
      (6, 6),
      (7, 6),
      (8, 6),
    }
    self.charger_position = (0, 0)

  def in_bounds(self, x: int, y: int) -> bool:
    return 0 <= x < self.width and 0 <= y < self.height

  def is_obstacle(self, x: int, y: int) -> bool:
    return (x, y) in self.obstacles

  def is_charger(self, x: int, y: int) -> bool:
    return (x, y) == self.charger_position

  def next_position(self, x: int, y: int, direction: str) -> tuple[int, int]:
    """Return the cell in front of the robot without moving it."""
    moves = {
      "north": (x, y - 1),
      "east": (x + 1, y),
      "south": (x, y + 1),
      "west": (x - 1, y),
    }
    return moves[direction]

  def can_move_to(self, x: int, y: int) -> bool:
    return self.in_bounds(x, y) and not self.is_obstacle(x, y)
