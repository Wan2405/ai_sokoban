"""Requirement 7/8: shared contract between the game and agent source files.

An agent file only has to define

    NAME = "short name"                      # optional, shown in the GUI
    def choose_action(view, time_limit):     # -> "North" | "East" | "South" | "West"

``view`` is an ``AgentView``. The game enforces the 1000 ms limit per decision;
an agent that is late, crashes or returns an invalid action loses that turn
(its previous action is repeated).
"""

import importlib
import importlib.util
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from ..req_6.competition import CompetitiveBoard, CompetitiveState
from ..req_5.gui_model import Cell, DIRECTIONS

TIME_LIMIT = 1.0
ACTIONS = tuple(DIRECTIONS)


@dataclass(frozen=True)
class AgentView:
    """Read-only information an agent receives each turn."""
    agent_id: int
    floor: frozenset[Cell]
    goals: frozenset[Cell]
    step_limit: int
    state: CompetitiveState

    @classmethod
    def from_game(cls, game: CompetitiveBoard, agent_id: int) -> "AgentView":
        return cls(agent_id, game.floor, game.goals, game.step_limit, game.state)

    @property
    def me(self) -> Cell:
        return self.state.players[self.agent_id]

    @property
    def opponent(self) -> Cell:
        return self.state.players[1 - self.agent_id]

    @property
    def steps_left(self) -> int:
        return self.step_limit - self.state.steps


@dataclass(frozen=True)
class Decision:
    action: str
    elapsed: float          # seconds spent inside choose_action
    timed_out: bool = False
    error: str = ""


def load_agent(spec: str):
    """Load an agent from a module name in this package or from a .py path."""
    if spec.endswith(".py"):
        path = Path(spec).resolve()
        loader = importlib.util.spec_from_file_location(f"sokoban_agent_{path.stem}", path)
        if loader is None:
            raise ValueError(f"Không đọc được file agent: {spec}")
        module = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(module)
    else:
        if spec.startswith("sokoban_ui."):
            module_name = spec
        elif spec.startswith("memberD."):
            module_name = f"sokoban_ui.{spec}"
        elif "." in spec:
            module_name = spec
        else:
            module_name = f"{__package__}.{spec}"
        module = importlib.import_module(module_name)
    if not callable(getattr(module, "choose_action", None)):
        raise ValueError(f"Agent {spec} thiếu hàm choose_action(view, time_limit).")
    return module


def agent_name(module) -> str:
    return getattr(module, "NAME", module.__name__.rsplit(".", 1)[-1])


class AgentRunner:
    """Runs one agent in a background thread so the GUI never freezes.

    start() begins a decision for the current game state; poll() returns
    None while the agent is still thinking, or a Decision once it is done
    or once the time limit has passed.
    """

    def __init__(self, module, agent_id: int, time_limit: float = TIME_LIMIT):
        self.module = module
        self.agent_id = agent_id
        self.time_limit = time_limit
        self.name = agent_name(module)
        self.last_action = "South"
        self.state = None           # state the current request was made for
        self._started = 0.0
        self._result = None
        self._token = 0

    @property
    def busy(self) -> bool:
        return self.state is not None

    def cancel(self) -> None:
        """Forget the running request (undo, reset...). Its late result is ignored."""
        self._token += 1
        self.state = None
        self._result = None

    def start(self, game: CompetitiveBoard) -> None:
        self.cancel()
        view = AgentView.from_game(game, self.agent_id)
        token, self.state = self._token, game.state
        self._started = time.perf_counter()

        def work():
            begin = time.perf_counter()
            try:
                action, error = self.module.choose_action(view, self.time_limit), ""
            except Exception as exc:  # A faulty agent must not crash the game.
                action, error = None, f"{type(exc).__name__}: {exc}"
            if token == self._token:
                self._result = (action, time.perf_counter() - begin, error)

        threading.Thread(target=work, daemon=True).start()

    def poll(self) -> Decision | None:
        if not self.busy:
            return None
        result = self._result
        if result is None:
            waited = time.perf_counter() - self._started
            if waited <= self.time_limit:
                return None
            decision = Decision(self.last_action, waited, timed_out=True)
        else:
            action, elapsed, error = result
            if elapsed > self.time_limit:
                decision = Decision(self.last_action, elapsed, True, error)
            elif action not in ACTIONS:
                decision = Decision(self.last_action, elapsed, False,
                                    error or f"Hành động không hợp lệ: {action!r}")
            else:
                decision = Decision(action, elapsed)
        self.last_action = decision.action
        self.cancel()
        return decision

    def decide(self, game: CompetitiveBoard) -> Decision:
        """Blocking version used by the arena and the tests."""
        self.start(game)
        while True:
            decision = self.poll()
            if decision is not None:
                return decision
            time.sleep(0.002)
