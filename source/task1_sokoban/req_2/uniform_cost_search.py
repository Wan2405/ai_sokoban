import heapq
import time

from source.task1_sokoban.req_2.search_node import SearchNode
from source.task1_sokoban.req_2.search_result import SearchResult


class UniformCostSearch:
    """Mo rong node co path cost g(n) nho nhat."""

    def __init__(self, problem):
        self.problem = problem

    def search(self):
        start_time = time.perf_counter()

        initial_node = SearchNode(self.problem.initial_state)

        frontier = []
        entry_number = 0
        heapq.heappush(frontier, (0, entry_number, initial_node))

        explored = set()
        best_path_cost = {self.problem.initial_state: 0}

        expanded_nodes = 0
        generated_nodes = 1
        max_frontier_size = 1

        while len(frontier) > 0:
            priority, current_entry_number, current_node = heapq.heappop(frontier)
            current_state = current_node.state

            if current_state in explored:
                continue

            if current_node.path_cost != best_path_cost[current_state]:
                continue

            if self.problem.is_goal(current_state):
                elapsed_seconds = time.perf_counter() - start_time

                return SearchResult(
                    True,
                    current_node.get_solution_actions(),
                    current_node.path_cost,
                    expanded_nodes,
                    generated_nodes,
                    max_frontier_size,
                    elapsed_seconds,
                    current_state,
                )

            explored.add(current_state)
            expanded_nodes = expanded_nodes + 1

            successors = self.problem.get_successors(current_state)

            for action, next_state, step_cost in successors:
                if next_state in explored:
                    continue

                new_path_cost = current_node.path_cost + step_cost

                if (
                    next_state not in best_path_cost
                    or new_path_cost < best_path_cost[next_state]
                ):
                    best_path_cost[next_state] = new_path_cost
                    child_node = SearchNode(
                        next_state,
                        current_node,
                        action,
                        new_path_cost,
                    )

                    entry_number = entry_number + 1
                    heapq.heappush(
                        frontier,
                        (new_path_cost, entry_number, child_node),
                    )
                    generated_nodes = generated_nodes + 1

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        elapsed_seconds = time.perf_counter() - start_time

        return SearchResult(
            False,
            [],
            None,
            expanded_nodes,
            generated_nodes,
            max_frontier_size,
            elapsed_seconds,
        )

