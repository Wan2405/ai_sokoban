"""Kiểm thử lời giải của core khi được sử dụng trong GUI thật."""

import os
from pathlib import Path
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as pg

from source.task1_sokoban.req_5.gui_model import Board, Level, load_default_levels
from source.task1_sokoban.req_1.map_loader import MapLoader
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_5.solver_bridge import create_map_from_board, solve_board
from source.task1_sokoban.req_5.app import SokobanApp
from source.task1_sokoban.req_5.replay import Replay


MAP_DIRECTORY = Path(__file__).resolve().parent.parent / "source/task1_sokoban/maps"
EXPECTED_COSTS = {
    "map_test": 3,
    "map_two_boxes": 8,
    "example_map": 34,
    "map_already_solved": 0,
}


class IntegrationTests(unittest.TestCase):
    def tearDown(self):
        pg.quit()

    def test_default_maps_and_dimensions(self):
        levels = load_default_levels()
        self.assertEqual([level.name for level in levels], list(EXPECTED_COSTS))
        for level in levels:
            with self.subTest(map=level.name):
                core_map = MapLoader().load(MAP_DIRECTORY / (level.name + ".txt"))
                self.assertEqual(level.height, core_map.row_count)
                self.assertEqual(level.width, core_map.column_count)

    def test_gui_to_core_conversion(self):
        for level in load_default_levels():
            with self.subTest(map=level.name):
                converted = create_map_from_board(Board(level))
                loaded = MapLoader().load(MAP_DIRECTORY / (level.name + ".txt"))
                self.assertEqual(converted.walls, loaded.walls)
                self.assertEqual(converted.goals, loaded.goals)
                self.assertEqual(converted.floor_cells, loaded.floor_cells)
                self.assertEqual(converted.initial_state, loaded.initial_state)

    def test_all_solutions_replay_and_match_core_transitions(self):
        for level in load_default_levels():
            for algorithm in ("UCS", "A*"):
                with self.subTest(map=level.name, algorithm=algorithm):
                    board = Board(level)
                    original_state = board.state
                    actions, cost = solve_board(board, algorithm)
                    self.assertEqual(cost, EXPECTED_COSTS[level.name])
                    self.assertEqual(cost, len(actions))
                    self.assertEqual(board.state, original_state)
                    core_map = create_map_from_board(board)
                    problem = SokobanProblem(core_map)
                    core_state = core_map.initial_state
                    replay = Replay(board, actions, cost)
                    for action in actions:
                        core_state = problem.result(core_state, action)
                        self.assertTrue(board.redo())
                        self.assertEqual(create_map_from_board(board).initial_state, core_state)
                    self.assertTrue(board.won)
                    self.assertTrue(replay.finished)
                    for _ in actions:
                        self.assertTrue(board.undo())
                    self.assertEqual(board.state, original_state)
                    self.assertEqual(replay.index, 0)

    def test_real_gui_solve_and_step_controls(self):
        app = SokobanApp()
        for index, level in enumerate(app.levels):
            for algorithm in ("UCS", "A*"):
                with self.subTest(map=level.name, algorithm=algorithm):
                    app._load_level(index)
                    app.act(algorithm)
                    app.act("solve")
                    self.assertIsNotNone(app.replay, app.toast)
                    self.assertEqual(app.replay.total_cost, EXPECTED_COSTS[level.name])
                    app.draw()
                    for _ in app.replay.actions:
                        app.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_RIGHT))
                    self.assertTrue(app.board.won)
                    app.draw()
                    for _ in app.replay.actions:
                        app.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_LEFT))
                    self.assertEqual(app.replay.index, 0)

    def test_solve_after_manual_move(self):
        level = Level.from_file(MAP_DIRECTORY / "map_test.txt")
        app = SokobanApp((level,))
        for algorithm in ("UCS", "A*"):
            with self.subTest(algorithm=algorithm):
                app._load_level(0)
                self.assertTrue(app.board.move("East"))
                manual_state = app.board.state
                app.act(algorithm)
                app.act("solve")
                self.assertIsNotNone(app.replay, app.toast)
                self.assertEqual(app.replay.total_cost, 2)
                self.assertEqual(app.board.state, manual_state)
                while app.board.redo():
                    pass
                self.assertTrue(app.board.won)
                self.assertEqual(app.board.state.moves, 3)
                app.act("reset")
                self.assertIsNone(app.replay)
                self.assertEqual(app.board.state, app.board.initial)

    def test_player_on_goal_preserves_goal(self):
        level = Level("Người chơi trên đích", (
            "%%%%%%%%%", "%A D B  %", "%       %", "%%%%%%%%%",
        ))
        for algorithm in ("UCS", "A*"):
            with self.subTest(algorithm=algorithm):
                board = Board(level)
                self.assertTrue(board.move("East"))
                self.assertTrue(board.move("East"))
                self.assertIn(board.state.player, board.goals)
                core_map = create_map_from_board(board)
                self.assertIn(core_map.initial_state.player_position, core_map.goals)
                actions, cost = solve_board(board, algorithm)
                Replay(board, actions, cost)
                while board.redo():
                    pass
                self.assertTrue(board.won)

    def test_no_solution_message_does_not_change_board(self):
        level = Level("Thùng bị kẹt", (
            "%%%%%%%", "%AB   %", "%    D%", "%%%%%%%",
        ))
        app = SokobanApp((level,))
        for algorithm in ("UCS", "A*"):
            with self.subTest(algorithm=algorithm):
                app._load_level(0)
                initial = app.board.state
                app.act(algorithm)
                app.act("solve")
                self.assertIsNone(app.replay)
                self.assertEqual(app.board.state, initial)
                self.assertIn("Không tìm được lời giải", app.toast)

    def test_competition_can_select_external_agent_fixture(self):
        app = SokobanApp()
        app.open_menu()
        app.act("dual")
        app.act("ctrl_1")
        app.act("ctrl_1")
        app.act("ctrl_1")
        self.assertEqual(app.controllers[0], "ai")
        self.assertEqual(app.agent_specs[0],
                         "source.task1_sokoban.req_8.agent_external_test")
        app.round_input = "2"
        app.act("ctrl_2")
        app.round_input = "2"
        app.act("start")
        self.assertEqual(app.runners[0].name, "TeamOther-Test")
        app.draw()


if __name__ == "__main__":
    unittest.main()
