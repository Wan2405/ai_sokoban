"""Req 5: chuyển dữ liệu của GUI sang core và trả lời giải về GUI.

Core dùng (hàng, cột). GUI dùng (cột, hàng), còn gọi là (x, y).
File này không nhập Pygame; nó chỉ đọc dữ liệu từ đối tượng bàn chơi.
"""

from source.task1_sokoban.req_1.map_loader import SokobanMap
from source.task1_sokoban.req_1.sokoban_problem import SokobanProblem
from source.task1_sokoban.req_1.state import SokobanState
from source.task1_sokoban.req_2.a_star_search import AStarSearch
from source.task1_sokoban.req_2.heuristic import BoxGoalDistanceHeuristic
from source.task1_sokoban.req_2.uniform_cost_search import UniformCostSearch


def create_map_from_board(board):
    """Tạo bản đồ core với trạng thái HIỆN TẠI của người chơi và thùng."""
    player_column, player_row = board.state.player
    player_position = (player_row, player_column)

    walls = set()
    goals = set()
    floor_cells = set()
    box_positions = set()

    for column, row in board.walls:
        walls.add((row, column))

    for column, row in board.goals:
        goals.add((row, column))

    for column, row in board.floor:
        floor_cells.add((row, column))

    for column, row in board.state.boxes:
        box_positions.add((row, column))

    # Đích lấy riêng từ board.goals nên không bị mất khi người chơi đứng trên đích.
    initial_state = SokobanState(player_position, box_positions)
    return SokobanMap(
        walls,
        goals,
        floor_cells,
        initial_state,
        board.level.height,
        board.level.width,
    )


def solve_board(board, algorithm_name):
    """GUI gọi hàm này với 'UCS' hoặc 'A*', nhận (actions, total_cost)."""
    sokoban_map = create_map_from_board(board)
    problem = SokobanProblem(sokoban_map)

    if algorithm_name == "UCS":
        search_algorithm = UniformCostSearch(problem)
    elif algorithm_name == "A*":
        heuristic = BoxGoalDistanceHeuristic(sokoban_map)
        search_algorithm = AStarSearch(problem, heuristic)
    else:
        raise ValueError("Thuật toán phải là UCS hoặc A*.")

    result = search_algorithm.search()

    if not result.found:
        raise ValueError("Không tìm được lời giải từ trạng thái hiện tại.")

    # Core vẫn trả SearchResult đầy đủ; GUI nhận hai trường mà nó cần.
    return result.actions, result.total_cost
