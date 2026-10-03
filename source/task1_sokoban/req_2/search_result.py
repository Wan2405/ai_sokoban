class SearchResult:
    """Ket qua chung de GUI va benchmark co the su dung."""

    def __init__(
        self,
        found,
        actions,
        total_cost,
        expanded_nodes,
        generated_nodes,
        max_frontier_size,
        elapsed_seconds,
        final_state=None,
    ):
        self.found = found
        self.actions = actions
        self.total_cost = total_cost
        self.expanded_nodes = expanded_nodes
        self.generated_nodes = generated_nodes
        self.max_frontier_size = max_frontier_size
        self.elapsed_seconds = elapsed_seconds
        self.final_state = final_state

    def __str__(self):
        if not self.found:
            return (
                "No solution found. Expanded nodes: "
                + str(self.expanded_nodes)
            )

        return (
            "Actions: "
            + str(self.actions)
            + "\nTotal cost: "
            + str(self.total_cost)
            + "\nExpanded nodes: "
            + str(self.expanded_nodes)
            + "\nGenerated nodes: "
            + str(self.generated_nodes)
            + "\nMaximum frontier size: "
            + str(self.max_frontier_size)
            + "\nElapsed seconds: "
            + format(self.elapsed_seconds, ".6f")
        )

