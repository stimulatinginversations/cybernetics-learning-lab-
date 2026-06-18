"""
A minimal finite state machine (FSM) for behaviour switching.

An FSM has:
- A fixed set of states (modes of behaviour)
- Transitions triggered by events or conditions
- Actions performed while in each state
"""

from enum import Enum
from typing import Callable, Hashable


class Transition:
  """Maps one state and one event to the next state."""

  def __init__(self, from_state: Hashable, event: Hashable, to_state: Hashable) -> None:
    self.from_state = from_state
    self.event = event
    self.to_state = to_state


class StateMachine:
  """
  Runs a finite state machine.

  The machine stays in one state at a time. Each update:
  1. Reads events from the environment
  2. Applies matching transitions
  3. Runs the action for the current state
  """

  def __init__(self, initial_state: Hashable) -> None:
    self.state = initial_state
    self._transitions: dict[tuple[Hashable, Hashable], Hashable] = {}
    self._actions: dict[Hashable, Callable[[object], None]] = {}

  def add_transition(self, from_state: Hashable, event: Hashable, to_state: Hashable) -> None:
    self._transitions[(from_state, event)] = to_state

  def set_action(self, state: Hashable, action: Callable[[object], None]) -> None:
    self._actions[state] = action

  def process_events(self, events: list[Hashable]) -> list[tuple[Hashable, Hashable]]:
    """Apply transitions for each event. Returns (old_state, new_state) pairs."""
    changes: list[tuple[Hashable, Hashable]] = []

    for event in events:
      key = (self.state, event)
      if key not in self._transitions:
        continue

      old_state = self.state
      self.state = self._transitions[key]
      changes.append((old_state, self.state))

    return changes

  def act(self, context: object) -> None:
    """Run the behaviour associated with the current state."""
    action = self._actions.get(self.state)
    if action is not None:
      action(context)
