import csv
import os
import statistics
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(TASK_DIR))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from source.task1_sokoban.req_1.map_loader import MapLoader
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_2.a_star_search import AStarSearch
from source.task1_sokoban.req_2.heuristic import BoxGoalDistanceHeuristic
from source.task1_sokoban.req_2.uniform_cost_search import UniformCostSearch

MAP_NAMES = [
    "example_map.txt",
    "map_already_solved.txt",
    "map_test.txt",
    "map_two_boxes.txt",
]
RUNS = 5


def run_once(map_path, algorithm_name):
    sokoban_map = MapLoader().load(map_path)
    problem = SokobanProblem(sokoban_map)
    if algorithm_name == "UCS":
        solver = UniformCostSearch(problem)
    else:
        solver = AStarSearch(problem, BoxGoalDistanceHeuristic(sokoban_map))
    return solver.search()


def run_benchmark(output_csv=None):
    if output_csv is None:
        output_csv = os.path.join(CURRENT_DIR, "results", "sokoban_results.csv")
    rows = []
    maps_dir = os.path.join(TASK_DIR, "maps")

    for map_name in MAP_NAMES:
        map_path = os.path.join(maps_dir, map_name)
        for algorithm in ("UCS", "A*"):
            for run_number in range(1, RUNS + 1):
                result = run_once(map_path, algorithm)
                rows.append({
                    "Map": map_name,
                    "Algorithm": algorithm,
                    "Run": run_number,
                    "Solved": result.found,
                    "Time_ms": result.elapsed_seconds * 1000.0,
                    "Path_Cost": result.total_cost,
                    "Path_Length": len(result.actions),
                    "Expanded_Nodes": result.expanded_nodes,
                    "Generated_Nodes": result.generated_nodes,
                    "Max_Frontier_Size": result.max_frontier_size,
                })

    fieldnames = list(rows[0].keys())
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return rows


def make_summary(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault((row["Map"], row["Algorithm"]), []).append(row)

    summary = []
    for (map_name, algorithm), group in grouped.items():
        summary.append({
            "Map": map_name,
            "Algorithm": algorithm,
            "Runs": len(group),
            "Solved_Runs": sum(bool(r["Solved"]) for r in group),
            "Avg_Time_ms": statistics.mean(r["Time_ms"] for r in group),
            "Min_Time_ms": min(r["Time_ms"] for r in group),
            "Max_Time_ms": max(r["Time_ms"] for r in group),
            "Avg_Path_Cost": statistics.mean(
                r["Path_Cost"] for r in group if r["Path_Cost"] is not None
            ) if any(r["Path_Cost"] is not None for r in group) else None,
            "Avg_Path_Length": statistics.mean(r["Path_Length"] for r in group),
            "Avg_Expanded_Nodes": statistics.mean(r["Expanded_Nodes"] for r in group),
            "Avg_Generated_Nodes": statistics.mean(r["Generated_Nodes"] for r in group),
            "Avg_Max_Frontier_Size": statistics.mean(r["Max_Frontier_Size"] for r in group),
        })
    return summary


def write_excel(rows, output_xlsx=None):
    try:
        from openpyxl import Workbook
    except ImportError:
        return None

    if output_xlsx is None:
        output_xlsx = os.path.join(CURRENT_DIR, "results", "sokoban_results.xlsx")

    wb = Workbook()
    raw = wb.active
    raw.title = "Raw_Data"
    fields = list(rows[0].keys())
    raw.append(fields)
    for row in rows:
        raw.append([row[f] for f in fields])

    summary_ws = wb.create_sheet("Summary")
    summary = make_summary(rows)
    sf = list(summary[0].keys())
    summary_ws.append(sf)
    for row in summary:
        summary_ws.append([row[f] for f in sf])

    wb.save(output_xlsx)
    return output_xlsx


if __name__ == "__main__":
    rows = run_benchmark()
    xlsx = write_excel(rows)
    print("REQ 3 benchmark completed.")
    print("Rows:", len(rows))
    print("CSV:", os.path.join(CURRENT_DIR, "results", "sokoban_results.csv"))
    if xlsx:
        print("Excel:", xlsx)
