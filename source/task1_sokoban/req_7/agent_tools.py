"""Small search helpers shared by the two agent files.

Distances here are real path lengths found by BFS on the map, not Manhattan
or Euclidean distances.
"""

from collections import deque

from ..req_5.gui_model import Cell, DIRECTIONS

INF = 10 ** 6


def shift(cell: Cell, action: str, times: int = 1) -> Cell:
    dx, dy = DIRECTIONS[action]
    return cell[0] + dx * times, cell[1] + dy * times


def bfs_distances(sources, passable) -> dict[Cell, int]:
    """Number of steps from the nearest source to every reachable cell."""
    dist = {cell: 0 for cell in sources if cell in passable}
    queue = deque(dist)
    while queue:
        cell = queue.popleft()
        for action in DIRECTIONS:
            nxt = shift(cell, action)
            if nxt in passable and nxt not in dist:
                dist[nxt] = dist[cell] + 1
                queue.append(nxt)
    return dist


def push_distances(floor, goals) -> dict[Cell, int]:
    """Minimum pushes to bring a lone box from each cell to some goal.

    Reverse BFS from the goals by "pulling": a box can arrive at c from
    p = c - d only if the player can stand at p - d. Cells missing from the
    result are dead squares: a box there can never reach a goal.
    """
    dist = {goal: 0 for goal in goals}
    queue = deque(goals)
    while queue:
        cell = queue.popleft()
        for action in DIRECTIONS:
            before = shift(cell, action, -1)
            stand = shift(cell, action, -2)
            if before in floor and stand in floor and before not in dist:
                dist[before] = dist[cell] + 1
                queue.append(before)
    return dist


def push_spots(view, push_dist, boxes, blocked):
    """Every useful push (stand cell, action, box) for the agent in ``view``.

    Useful means: the box is not already ours on a goal, the cell behind the
    box is free, and after the push the box is still not dead. Pushes that
    bring a box closer to a goal are marked as ``improving``.
    """
    owners = dict(view.state.owners)
    spots = []
    for box in boxes:
        if owners.get(box) == view.agent_id:
            continue
        for action in DIRECTIONS:
            stand, target = shift(box, action, -1), shift(box, action)
            if (stand not in view.floor or stand in boxes or target in boxes
                    or target in blocked or target not in push_dist):
                continue
            improving = push_dist[target] < push_dist.get(box, INF)
            # A box on a goal owned by nobody/the opponent must leave first.
            if box in view.goals or improving:
                spots.append((stand, action, box, improving))
    return spots


def approach_spot(view, push_dist):
    """Find a free waypoint toward a useful push, even if its stand is blocked.

    In a two-agent match the opponent can occupy the support square needed for
    a push. Moving to a neighboring waypoint lets both agents leave that
    deadlock instead of repeatedly returning a wall-facing action.
    """
    boxes = view.state.boxes
    owners = dict(view.state.owners)
    passable = view.floor - boxes - {view.opponent}
    walk_dist = bfs_distances([view.me], passable)
    candidates = []
    for box in boxes:
        if owners.get(box) == view.agent_id:
            continue
        for action in DIRECTIONS:
            stand = shift(box, action, -1)
            target = shift(box, action)
            if (stand not in view.floor or target in boxes
                    or target == view.opponent or target not in push_dist):
                continue
            improving = push_dist[target] < push_dist.get(box, INF)
            if box not in view.goals and not improving:
                continue
            waypoints = [stand]
            if stand == view.opponent:
                waypoints = [
                    shift(stand, direction, -1)
                    for direction in DIRECTIONS
                ]
            for waypoint in waypoints:
                if waypoint in walk_dist:
                    score = (walk_dist[waypoint]
                             + 2 * push_dist[target]
                             + (1 if stand == view.opponent else 0))
                    candidates.append((score, waypoint, action))
    if not candidates:
        return None
    _, waypoint, action = min(candidates)
    return waypoint, action
