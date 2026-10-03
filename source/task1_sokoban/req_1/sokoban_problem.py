from collections import deque
from source.task1_sokoban.req_1.state import SokobanState

class SokobanProblem:
    """Mo hinh bai toan tim kiem trong khong gian trang thai."""

    ACTIONS = (
        ("North", -1, 0),
        ("East", 0, 1),
        ("West", 0, -1),
        ("South", 1, 0),
    )

    def __init__(self, sokoban_map):
        self.sokoban_map = sokoban_map
        self.initial_state = sokoban_map.initial_state
        self.box_reachable_cells = self._find_box_reachable_cells()

    def _find_box_reachable_cells(self):
        """
        Tim cac o ma mot thung co the duoc day tu do den mot dich.

        Qua trinh duyet nguoc tu cac dich va tam thoi bo qua cac thung khac.
        """
        reachable_cells = set(self.sokoban_map.goals)
        frontier = deque(self.sokoban_map.goals)

        while len(frontier) > 0:
            current_box_position = frontier.popleft()

            for action_name, row_change, column_change in self.ACTIONS:
                previous_box_position = (
                    current_box_position[0] - row_change,
                    current_box_position[1] - column_change,
                )
                player_support_position = (
                    previous_box_position[0] - row_change,
                    previous_box_position[1] - column_change,
                )

                if previous_box_position not in self.sokoban_map.floor_cells:
                    continue

                if player_support_position not in self.sokoban_map.floor_cells:
                    continue

                if previous_box_position in reachable_cells:
                    continue

                reachable_cells.add(previous_box_position)
                frontier.append(previous_box_position)

        return frozenset(reachable_cells)

    def is_deadlock(self, state):
        """Phat hien deadlock tinh: thung nam o o khong the day den bat ky dich nao."""
        for box_position in state.box_positions:
            if box_position in self.sokoban_map.goals:
                continue

            if box_position not in self.box_reachable_cells:
                return True

        return False

    def get_actions(self, state):
        """Tra ve danh sach hanh dong hop le tai state."""
        valid_actions = []
        player_row, player_column = state.player_position

        for action_name, row_change, column_change in self.ACTIONS:
            next_position = (
                player_row + row_change,
                player_column + column_change,
            )

            if next_position not in self.sokoban_map.floor_cells:
                continue

            if next_position not in state.box_positions:
                valid_actions.append(action_name)
                continue

            box_next_position = (
                next_position[0] + row_change,
                next_position[1] + column_change,
            )

            if box_next_position not in self.sokoban_map.floor_cells:
                continue

            if box_next_position in state.box_positions:
                continue

            valid_actions.append(action_name)

        return valid_actions

    def result(self, state, action):
        """Tra ve trang thai moi sau khi thuc hien mot hanh dong hop le."""
        if action not in self.get_actions(state):
            raise ValueError("Invalid action: " + str(action))

        row_change = 0
        column_change = 0

        for action_name, action_row_change, action_column_change in self.ACTIONS:
            if action_name == action:
                row_change = action_row_change
                column_change = action_column_change
                break

        player_row, player_column = state.player_position
        new_player_position = (
            player_row + row_change,
            player_column + column_change,
        )

        new_box_positions = set(state.box_positions)

        if new_player_position in state.box_positions:
            new_box_position = (
                new_player_position[0] + row_change,
                new_player_position[1] + column_change,
            )

            new_box_positions.remove(new_player_position)
            new_box_positions.add(new_box_position)

        return SokobanState(new_player_position, new_box_positions)

    def is_goal(self, state):
        """Dung khi tat ca thung deu nam tren cac vi tri dich."""
        return state.box_positions == self.sokoban_map.goals

    def get_step_cost(self, state, action, next_state):
        """Moi hanh dong hop le co chi phi bang 1."""
        return 1

    def get_successors(self, state):
        """Sinh cac bo (action, next_state, step_cost)."""
        successors = []
        valid_actions = self.get_actions(state)

        for action in valid_actions:
            next_state = self.result(state, action)

            if self.is_deadlock(next_state):
                continue

            step_cost = self.get_step_cost(state, action, next_state)
            successors.append((action, next_state, step_cost))

        return successors

    def render(self, state):
        """Chuyen mot state thanh chuoi de xem nhanh tren terminal."""
        output_lines = []

        for row_index in range(self.sokoban_map.row_count):
            output_line = ""

            for column_index in range(self.sokoban_map.column_count):
                position = (row_index, column_index)

                if position in self.sokoban_map.walls:
                    symbol = "%"
                elif position == state.player_position:
                    symbol = "A"
                elif position in state.box_positions and position in self.sokoban_map.goals:
                    symbol = "C"
                elif position in state.box_positions:
                    symbol = "B"
                elif position in self.sokoban_map.goals:
                    symbol = "D"
                else:
                    symbol = " "

                output_line = output_line + symbol

            output_lines.append(output_line)

        return "\n".join(output_lines)
