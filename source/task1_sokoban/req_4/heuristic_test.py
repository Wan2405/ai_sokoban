import csv
import os
import sys
from collections import deque

from openpyxl import Workbook
from openpyxl.styles import Font

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(TASK_DIR))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from source.task1_sokoban.req_1.map_loader import MapLoader
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_2.heuristic import BoxGoalDistanceHeuristic
from source.task1_sokoban.req_2.uniform_cost_search import UniformCostSearch

MAP_NAMES = [
    "example_map.txt",
    "map_already_solved.txt",
    "map_test.txt",
    "map_two_boxes.txt",
]
MAX_STATES_PER_MAP = 40


class StateProblem:
    """Adapter that reuses SokobanProblem logic with a chosen start state."""

    def __init__(self, original_problem, initial_state):
        self._problem = original_problem
        self.initial_state = initial_state

    def is_goal(self, state):
        return self._problem.is_goal(state)

    def get_successors(self, state):
        return self._problem.get_successors(state)


def collect_states(problem, limit):
    """Collect up to `limit` reachable states by BFS, including the initial state."""
    queue = deque([problem.initial_state])
    seen = {problem.initial_state}
    transitions = []

    while queue:
        state = queue.popleft()
        successors = problem.get_successors(state)

        for _, next_state, cost in successors:
            transitions.append((state, next_state, cost))
            if next_state not in seen and len(seen) < limit:
                seen.add(next_state)
                queue.append(next_state)

    return list(seen), transitions


def exact_remaining_cost(problem, state):
    """Exact shortest remaining cost from state using the original UCS implementation."""
    adapter = StateProblem(problem, state)
    return UniformCostSearch(adapter).search().total_cost


def write_excel(output_xlsx, fields, rows):
    """Write the same heuristic results to an Excel workbook."""
    os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Heuristic Results"

    sheet.append(fields)
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    for row in rows:
        sheet.append([row[field] for field in fields])

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    # Keep the worksheet readable without changing the result data.
    widths = {
        "A": 22, "B": 18, "C": 42, "D": 42,
        "E": 12, "F": 12, "G": 12, "H": 12, "I": 10,
    }
    for column, width in widths.items():
        sheet.column_dimensions[column].width = width

    workbook.save(output_xlsx)


def run_req4(output_csv=None, output_xlsx=None):
    if output_csv is None:
        output_csv = os.path.join(CURRENT_DIR, "results", "heuristic_results.csv")
    if output_xlsx is None:
        output_xlsx = os.path.join(CURRENT_DIR, "results", "heuristic_results.xlsx")

    rows = []
    maps_dir = os.path.join(TASK_DIR, "maps")

    for map_name in MAP_NAMES:
        sokoban_map = MapLoader().load(os.path.join(maps_dir, map_name))
        problem = SokobanProblem(sokoban_map)
        heuristic = BoxGoalDistanceHeuristic(sokoban_map)
        states, transitions = collect_states(problem, MAX_STATES_PER_MAP)

        # Goal-state sanity check: use UCS to obtain a real goal state for the map.
        goal_result = UniformCostSearch(problem).search()
        goal_state = goal_result.final_state if goal_result.found else None

        if goal_state is not None:
            h_goal = heuristic.calculate(goal_state)
            rows.append({
                "Map": map_name,
                "Property": "GoalZero",
                "State": repr(goal_state),
                "Next_State": "",
                "h_s": h_goal,
                "cost": "",
                "h_next": "",
                "h_star": 0,
                "Pass": h_goal == 0,
            })

        # Admissibility: h(s) <= h*(s).
        for state in states:
            optimal = exact_remaining_cost(problem, state)
            if optimal is None:
                # Unsolvable sampled states have h*(s) = infinity, so they are
                # excluded from the finite admissibility comparison.
                continue

            h_s = heuristic.calculate(state)
            rows.append({
                "Map": map_name,
                "Property": "Admissibility",
                "State": repr(state),
                "Next_State": "",
                "h_s": h_s,
                "cost": "",
                "h_next": "",
                "h_star": optimal,
                "Pass": h_s <= optimal,
            })

        # Consistency: h(s) <= c(s,s') + h(s').
        for state, next_state, cost in transitions:
            h_s = heuristic.calculate(state)
            h_next = heuristic.calculate(next_state)
            rows.append({
                "Map": map_name,
                "Property": "Consistency",
                "State": repr(state),
                "Next_State": repr(next_state),
                "h_s": h_s,
                "cost": cost,
                "h_next": h_next,
                "h_star": "",
                "Pass": h_s <= cost + h_next,
            })

    fields = ["Map", "Property", "State", "Next_State", "h_s", "cost", "h_next", "h_star", "Pass"]
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    write_excel(output_xlsx, fields, rows)

    return rows


def print_summary(rows):
    for prop in ("GoalZero", "Admissibility", "Consistency"):
        subset = [r for r in rows if r["Property"] == prop]
        passed = sum(r["Pass"] is True for r in subset)
        print(f"{prop}: {passed}/{len(subset)} checks passed")


if __name__ == "__main__":
    rows = run_req4()
    print("REQ 4 heuristic experiment completed.")
    print("Rows:", len(rows))
    print_summary(rows)
    print("CSV:", os.path.join(CURRENT_DIR, "results", "heuristic_results.csv"))
    print("Excel:", os.path.join(CURRENT_DIR, "results", "heuristic_results.xlsx"))
