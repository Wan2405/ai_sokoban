import os
import sys

from source.task1_sokoban.req_1.map_loader import MapLoader
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_2.a_star_search import AStarSearch
from source.task1_sokoban.req_2.heuristic import BoxGoalDistanceHeuristic
from source.task1_sokoban.req_2.uniform_cost_search import UniformCostSearch


def print_usage():
    print("Usage:")
    print("  python main_cli.py <map_path> ucs")
    print("  python main_cli.py <map_path> astar")


def print_result(problem, result):
    print()
    print(result)

    if result.found:
        print()
        print("Final state:")
        print(problem.render(result.final_state))


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    default_map_path = os.path.join(current_directory, "source", "task1_sokoban", "maps", "map_test.txt")

    map_path = default_map_path
    algorithm_name = "astar"

    if len(sys.argv) >= 2:
        map_path = sys.argv[1]

    if len(sys.argv) >= 3:
        algorithm_name = sys.argv[2].lower()

    if algorithm_name not in ("ucs", "astar"):
        print("Unknown algorithm: " + algorithm_name)
        print_usage()
        return

    try:
        sokoban_map = MapLoader().load(map_path)
    except (OSError, ValueError) as error:
        print("Cannot load map: " + str(error))
        return

    problem = SokobanProblem(sokoban_map)

    print("Initial state:")
    print(problem.render(problem.initial_state))
    print()
    print("Algorithm: " + algorithm_name.upper())

    if algorithm_name == "ucs":
        search_algorithm = UniformCostSearch(problem)
    else:
        heuristic = BoxGoalDistanceHeuristic(sokoban_map)
        search_algorithm = AStarSearch(problem, heuristic)

    result = search_algorithm.search()
    print_result(problem, result)


if __name__ == "__main__":
    main()

