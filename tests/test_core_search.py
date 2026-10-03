import os
import unittest

from source.task1_sokoban.req_1.map_loader import MapLoader
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_2.a_star_search import AStarSearch
from source.task1_sokoban.req_2.heuristic import BoxGoalDistanceHeuristic
from source.task1_sokoban.req_2.uniform_cost_search import UniformCostSearch


class CoreSearchTests(unittest.TestCase):
    def setUp(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        project_directory = os.path.dirname(current_directory)
        map_path = os.path.join(project_directory, "source", "task1_sokoban", "maps", "map_test.txt")

        self.sokoban_map = MapLoader().load(map_path)
        self.problem = SokobanProblem(self.sokoban_map)

    def test_map_loader(self):
        self.assertEqual(self.problem.initial_state.player_position, (2, 2))
        self.assertEqual(self.problem.initial_state.box_positions, frozenset({(2, 4)}))
        self.assertEqual(self.sokoban_map.goals, frozenset({(2, 6)}))

    def test_result_when_player_moves_east(self):
        next_state = self.problem.result(self.problem.initial_state, "East")

        self.assertEqual(next_state.player_position, (2, 3))
        self.assertEqual(next_state.box_positions, frozenset({(2, 4)}))

    def test_result_when_player_pushes_box(self):
        first_state = self.problem.result(self.problem.initial_state, "East")
        second_state = self.problem.result(first_state, "East")

        self.assertEqual(second_state.player_position, (2, 4))
        self.assertEqual(second_state.box_positions, frozenset({(2, 5)}))

    def test_uniform_cost_search(self):
        result = UniformCostSearch(self.problem).search()

        self.assertTrue(result.found)
        self.assertEqual(result.actions, ["East", "East", "East"])
        self.assertEqual(result.total_cost, 3)

    def test_a_star_search(self):
        heuristic = BoxGoalDistanceHeuristic(self.sokoban_map)
        result = AStarSearch(self.problem, heuristic).search()

        self.assertTrue(result.found)
        self.assertEqual(result.actions, ["East", "East", "East"])
        self.assertEqual(result.total_cost, 3)

    def test_ucs_and_a_star_have_same_optimal_cost(self):
        ucs_result = UniformCostSearch(self.problem).search()

        heuristic = BoxGoalDistanceHeuristic(self.sokoban_map)
        a_star_result = AStarSearch(self.problem, heuristic).search()

        self.assertEqual(ucs_result.total_cost, a_star_result.total_cost)

    def test_original_example_map_can_be_loaded(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        project_directory = os.path.dirname(current_directory)
        map_path = os.path.join(project_directory, "source", "task1_sokoban", "maps", "example_map.txt")

        example_map = MapLoader().load(map_path)

        self.assertEqual(len(example_map.initial_state.box_positions), 7)
        self.assertEqual(len(example_map.goals), 7)


if __name__ == "__main__":
    unittest.main()
