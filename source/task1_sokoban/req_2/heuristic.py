from collections import deque


class BoxGoalDistanceHeuristic:
    """
    Tong so lan day uoc luong nho nhat khi ghep moi thung voi mot dich rieng.

    BFS duyet nguoc tu dich, co xet tuong va o dung can thiet de day thung.
    Qua trinh uoc luong tam thoi bo qua cac thung khac.
    """

    def __init__(self, sokoban_map):
        self.floor_cells = sokoban_map.floor_cells
        self.goals = sorted(sokoban_map.goals)
        self.goal_distances = {}
        self.cached_values = {}

        self._build_goal_distances()

    def _build_goal_distances(self):
        for goal in self.goals:
            self.goal_distances[goal] = self._breadth_first_distances(goal)

    def _breadth_first_distances(self, start_position):
        distances = {start_position: 0}
        frontier = deque([start_position])

        directions = (
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 0),
        )

        while len(frontier) > 0:
            current_box_position = frontier.popleft()
            current_distance = distances[current_box_position]

            for row_change, column_change in directions:
                previous_box_position = (
                    current_box_position[0] - row_change,
                    current_box_position[1] - column_change,
                )
                player_support_position = (
                    previous_box_position[0] - row_change,
                    previous_box_position[1] - column_change,
                )

                if previous_box_position not in self.floor_cells:
                    continue

                if player_support_position not in self.floor_cells:
                    continue

                if previous_box_position in distances:
                    continue

                distances[previous_box_position] = current_distance + 1
                frontier.append(previous_box_position)

        return distances

    def calculate(self, state):
        box_key = state.box_positions

        if box_key in self.cached_values:
            return self.cached_values[box_key]

        boxes = sorted(state.box_positions)
        used_goals = [False] * len(self.goals)

        heuristic_value = self._minimum_assignment_cost(
            boxes,
            0,
            used_goals,
        )

        self.cached_values[box_key] = heuristic_value
        return heuristic_value

    def _minimum_assignment_cost(self, boxes, box_index, used_goals):
        if box_index == len(boxes):
            return 0

        current_box = boxes[box_index]
        minimum_cost = float("inf")

        for goal_index in range(len(self.goals)):
            if used_goals[goal_index]:
                continue

            goal = self.goals[goal_index]
            distances_from_goal = self.goal_distances[goal]

            if current_box not in distances_from_goal:
                continue

            used_goals[goal_index] = True

            remaining_cost = self._minimum_assignment_cost(
                boxes,
                box_index + 1,
                used_goals,
            )

            used_goals[goal_index] = False

            if remaining_cost == float("inf"):
                continue

            total_cost = distances_from_goal[current_box] + remaining_cost

            if total_cost < minimum_cost:
                minimum_cost = total_cost

        return minimum_cost
