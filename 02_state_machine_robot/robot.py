"""
A robot controlled by a finite state machine.

This builds on the idea of internal state from Project 01, but now the
state is explicit behaviour mode rather than only numeric variables.
"""

from enum import Enum, auto

from environment import Environment, SensorReading
from state_machine import StateMachine


class RobotState(Enum):
  IDLE = auto()
  PATROL = auto()
  AVOID = auto()
  SEEK_CHARGE = auto()
  CHARGING = auto()


class RobotEvent(Enum):
  START_PATROL = auto()
  OBSTACLE_DETECTED = auto()
  PATH_CLEAR = auto()
  BATTERY_LOW = auto()
  AT_CHARGER = auto()
  BATTERY_FULL = auto()
  REST_COMPLETE = auto()


class Robot:
  """A simple mobile robot with battery and directional movement."""

  BATTERY_MAX = 100.0
  BATTERY_LOW_THRESHOLD = 25.0
  MOVE_COST = 4.0
  CHARGE_GAIN = 12.0
  REST_GAIN = 2.0

  def __init__(self, x: int, y: int, direction: str = "east") -> None:
    self.x = x
    self.y = y
    self.direction = direction
    self.battery = self.BATTERY_MAX
    self.environment = Environment()
    self.fsm = self._build_state_machine()

  def _build_state_machine(self) -> StateMachine:
    fsm = StateMachine(RobotState.IDLE)

    transitions = [
      (RobotState.IDLE, RobotEvent.START_PATROL, RobotState.PATROL),
      (RobotState.PATROL, RobotEvent.OBSTACLE_DETECTED, RobotState.AVOID),
      (RobotState.PATROL, RobotEvent.BATTERY_LOW, RobotState.SEEK_CHARGE),
      (RobotState.AVOID, RobotEvent.PATH_CLEAR, RobotState.PATROL),
      (RobotState.AVOID, RobotEvent.BATTERY_LOW, RobotState.SEEK_CHARGE),
      (RobotState.SEEK_CHARGE, RobotEvent.AT_CHARGER, RobotState.CHARGING),
      (RobotState.SEEK_CHARGE, RobotEvent.OBSTACLE_DETECTED, RobotState.AVOID),
      (RobotState.CHARGING, RobotEvent.BATTERY_FULL, RobotState.IDLE),
    ]

    for from_state, event, to_state in transitions:
      fsm.add_transition(from_state, event, to_state)

    fsm.set_action(RobotState.IDLE, self._act_idle)
    fsm.set_action(RobotState.PATROL, self._act_patrol)
    fsm.set_action(RobotState.AVOID, self._act_avoid)
    fsm.set_action(RobotState.SEEK_CHARGE, self._act_seek_charge)
    fsm.set_action(RobotState.CHARGING, self._act_charging)

    return fsm

  def read_sensors(self) -> SensorReading:
    next_x, next_y = self.environment.next_position(self.x, self.y, self.direction)
    obstacle_ahead = not self.environment.can_move_to(next_x, next_y)

    return SensorReading(
      obstacle_ahead=obstacle_ahead,
      at_charger=self.environment.is_charger(self.x, self.y),
      battery_low=self.battery <= self.BATTERY_LOW_THRESHOLD,
      battery_full=self.battery >= self.BATTERY_MAX,
    )

  def events_from_sensors(self, sensors: SensorReading) -> list[RobotEvent]:
    """Convert sensor readings into FSM events for the current state."""
    events: list[RobotEvent] = []

    if self.fsm.state == RobotState.IDLE and not sensors.battery_low:
      events.append(RobotEvent.START_PATROL)

    if sensors.obstacle_ahead and not (
      sensors.at_charger and self.fsm.state == RobotState.SEEK_CHARGE
    ):
      events.append(RobotEvent.OBSTACLE_DETECTED)

    if not sensors.obstacle_ahead and self.fsm.state == RobotState.AVOID and not sensors.battery_low:
      events.append(RobotEvent.PATH_CLEAR)

    if sensors.at_charger and self.fsm.state == RobotState.SEEK_CHARGE:
      events.append(RobotEvent.AT_CHARGER)

    if sensors.battery_low and self.fsm.state != RobotState.CHARGING:
      events.append(RobotEvent.BATTERY_LOW)

    if sensors.battery_full and self.fsm.state == RobotState.CHARGING:
      events.append(RobotEvent.BATTERY_FULL)

    return events

  def step(self) -> dict[str, object]:
    """Advance the robot by one simulation tick."""
    sensors = self.read_sensors()
    events = self.events_from_sensors(sensors)
    changes = self.fsm.process_events(events)
    self.fsm.act(self)

    return {
      "state": self.fsm.state.name,
      "position": (self.x, self.y),
      "direction": self.direction,
      "battery": round(self.battery, 1),
      "events": [event.name for event in events],
      "transitions": [(old.name, new.name) for old, new in changes],
    }

  def _act_idle(self, _: "Robot") -> None:
    self.battery = min(self.BATTERY_MAX, self.battery + self.REST_GAIN)

  def _act_patrol(self, _: "Robot") -> None:
    self._move_forward()

  def _act_avoid(self, _: "Robot") -> None:
    self._turn_right()

  def _act_seek_charge(self, _: "Robot") -> None:
    self._move_toward_charger()

  def _act_charging(self, _: "Robot") -> None:
    self.battery = min(self.BATTERY_MAX, self.battery + self.CHARGE_GAIN)

  def _move_forward(self) -> None:
    next_x, next_y = self.environment.next_position(self.x, self.y, self.direction)
    if self.environment.can_move_to(next_x, next_y):
      self.x = next_x
      self.y = next_y
      self.battery = max(0.0, self.battery - self.MOVE_COST)

  def _turn_right(self) -> None:
    order = ["north", "east", "south", "west"]
    index = order.index(self.direction)
    self.direction = order[(index + 1) % 4]
    self.battery = max(0.0, self.battery - 1.0)

  def _move_toward_charger(self) -> None:
    target_x, target_y = self.environment.charger_position

    if self.x < target_x:
      self.direction = "east"
    elif self.x > target_x:
      self.direction = "west"
    elif self.y > target_y:
      self.direction = "north"
    elif self.y < target_y:
      self.direction = "south"
    else:
      return

    self._move_forward()
