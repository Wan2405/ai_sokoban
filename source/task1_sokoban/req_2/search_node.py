class SearchNode:
    """Node trong cay/do thi tim kiem, khac voi SokobanState."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def get_solution_actions(self):
        actions = []
        current_node = self

        while current_node.parent is not None:
            actions.append(current_node.action)
            current_node = current_node.parent

        actions.reverse()
        return actions

