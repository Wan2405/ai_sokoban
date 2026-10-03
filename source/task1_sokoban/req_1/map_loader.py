from source.task1_sokoban.req_1.state import SokobanState

class SokobanMap:
    """Du lieu co dinh cua ban do va trang thai ban dau."""

    def __init__(
        self,
        walls,
        goals,
        floor_cells,
        initial_state,
        row_count,
        column_count,
    ):
        self.walls = frozenset(walls)
        self.goals = frozenset(goals)
        self.floor_cells = frozenset(floor_cells)
        self.initial_state = initial_state
        self.row_count = row_count
        self.column_count = column_count


class MapLoader:
    """Doc file text va chuyen thanh doi tuong SokobanMap."""

    VALID_SYMBOLS = {"%", "A", "B", "C", "D", " "}

    def load(self, file_path):
        with open(file_path, "r", encoding="utf-8") as map_file:
            # splitlines() chi xoa ky tu xuong dong, khong xoa dau cach.
            map_lines = map_file.read().splitlines()

        # Bo qua cac dong rong vo tinh nam sau dong cuoi cua ban do.
        while len(map_lines) > 0 and map_lines[-1] == "":
            map_lines.pop()

        if len(map_lines) == 0:
            raise ValueError("Map file is empty.")

        walls = set()
        goals = set()
        floor_cells = set()
        box_positions = set()
        player_positions = []

        row_count = len(map_lines)
        column_count = 0

        for map_line in map_lines:
            if len(map_line) > column_count:
                column_count = len(map_line)

        for row_index in range(row_count):
            map_line = map_lines[row_index]

            for column_index in range(len(map_line)):
                symbol = map_line[column_index]
                position = (row_index, column_index)

                if symbol not in self.VALID_SYMBOLS:
                    raise ValueError(
                        "Invalid symbol '"
                        + symbol
                        + "' at row "
                        + str(row_index + 1)
                        + ", column "
                        + str(column_index + 1)
                        + "."
                    )

                if symbol == "%":
                    walls.add(position)
                else:
                    floor_cells.add(position)

                if symbol == "A":
                    player_positions.append(position)
                elif symbol == "B":
                    box_positions.add(position)
                elif symbol == "D":
                    goals.add(position)
                elif symbol == "C":
                    box_positions.add(position)
                    goals.add(position)

        if len(player_positions) != 1:
            raise ValueError("The map must contain exactly one player symbol A.")

        if len(box_positions) == 0:
            raise ValueError("The map must contain at least one box.")

        if len(box_positions) != len(goals):
            raise ValueError("The number of boxes must equal the number of goals.")

        initial_state = SokobanState(player_positions[0], box_positions)

        return SokobanMap(
            walls,
            goals,
            floor_cells,
            initial_state,
            row_count,
            column_count,
        )
