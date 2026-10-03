"""Requirement 7: run two agent files against each other without the GUI.

    python -m source.task1_sokoban.req_7.arena --agent1 path/to/agent1.py --agent2 path/to/agent2.py --steps 40

Each decision is limited to 1000 ms; late or invalid answers repeat the
agent's previous action and are counted in the report.
"""

import argparse
from dataclasses import dataclass, field

from .agent_api import TIME_LIMIT, AgentRunner, load_agent
from ..req_6.competition import COMPETITION_LEVEL, CompetitiveBoard
from ..req_5.gui_model import Level


@dataclass
class MatchReport:
    names: tuple[str, str]
    scores: tuple[int, int]
    winner: int | None
    max_ms: list[float] = field(default_factory=lambda: [0.0, 0.0])
    total_ms: list[float] = field(default_factory=lambda: [0.0, 0.0])
    timeouts: list[int] = field(default_factory=lambda: [0, 0])
    errors: list[int] = field(default_factory=lambda: [0, 0])
    turns: int = 0


def play_match(level, second_player, steps, specs, time_limit=TIME_LIMIT, verbose=False):
    game = CompetitiveBoard(level, tuple(second_player), steps)
    runners = [AgentRunner(load_agent(spec), i, time_limit) for i, spec in enumerate(specs)]
    report = MatchReport((runners[0].name, runners[1].name), (0, 0), None)
    while not game.finished:
        decisions = [runner.decide(game) for runner in runners]
        for i, d in enumerate(decisions):
            report.max_ms[i] = max(report.max_ms[i], d.elapsed * 1000)
            report.total_ms[i] += d.elapsed * 1000
            report.timeouts[i] += d.timed_out
            report.errors[i] += bool(d.error)
        game.step(tuple(d.action for d in decisions))
        if verbose:
            print(f"Lượt {game.state.steps:3d}: {decisions[0].action:5s} "
                  f"{decisions[1].action:5s} · Điểm {game.scores[0]}-{game.scores[1]}")
    report.scores, report.winner, report.turns = game.scores, game.winner, game.state.steps
    return report


def main():
    # Windows consoles may still expose a legacy code page to Python.
    import sys
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Cho hai agent thi đấu (mục 7/8).")
    parser.add_argument("--agent1", required=True, help="Tên module hoặc đường dẫn .py")
    parser.add_argument("--agent2", required=True, help="Tên module hoặc đường dẫn .py")
    parser.add_argument("--steps", type=int, default=40, help="Số lượt n")
    parser.add_argument("--map", help="Bản đồ có một A; tác nhân 2 đặt bằng --second-player")
    parser.add_argument("--second-player", type=int, nargs=2, default=(8, 5), metavar=("X", "Y"))
    parser.add_argument("--games", type=int, default=1, help="Số ván; ván chẵn đổi vị trí xuất phát")
    parser.add_argument("--verbose", action="store_true", help="In từng lượt")
    args = parser.parse_args()
    try:
        level = Level.from_file(args.map) if args.map else COMPETITION_LEVEL
        wins = [0, 0, 0]
        for index in range(args.games):
            specs = (args.agent1, args.agent2)
            swap = index % 2 == 1
            report = play_match(level, args.second_player, args.steps,
                                specs[::-1] if swap else specs, verbose=args.verbose)
            order = (1, 0) if swap else (0, 1)
            scores = tuple(report.scores[i] for i in order)
            winner = None if report.winner is None else order.index(report.winner)
            wins[2 if winner is None else winner] += 1
            print(f"Ván {index+1}: {args.agent1} {scores[0]} - {scores[1]} {args.agent2} · "
                  + ("Hòa" if winner is None else f"{(args.agent1, args.agent2)[winner]} thắng"))
            for i in order:
                print(f"  {report.names[i]:6s} max {report.max_ms[i]:7.1f} ms · "
                      f"TB {report.total_ms[i]/max(1, report.turns):6.1f} ms · "
                      f"quá giờ {report.timeouts[i]} · lỗi {report.errors[i]}")
        print(f"Tổng: {args.agent1} thắng {wins[0]}, {args.agent2} thắng {wins[1]}, hòa {wins[2]}")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Không thể chạy trận: {exc}\n")


if __name__ == "__main__":
    main()
