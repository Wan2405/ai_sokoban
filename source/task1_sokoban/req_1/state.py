class SokobanState:
    """Trang thai thay doi trong qua trinh choi Sokoban."""

    def __init__(self, player_position, box_positions):
        self.player_position = player_position
        self.box_positions = frozenset(box_positions)

    def __eq__(self, other):
        if not isinstance(other, SokobanState):
            return False

        return (
            self.player_position == other.player_position
            and self.box_positions == other.box_positions
        )

    def __hash__(self):
        return hash((self.player_position, self.box_positions))

    def __str__(self):
        return (
            "Player: "
            + str(self.player_position)
            + ", Boxes: "
            + str(sorted(self.box_positions))
        )

    def __repr__(self):
        return self.__str__()

