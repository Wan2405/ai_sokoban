"""Agent BFS: chon cho day bang h, di toi do bang BFS."""
from collections import deque
import heapq

from .agent_tools import (
    INF, approach_spot, bfs_distances, push_distances, push_spots, shift,
)
from ..req_5.gui_model import DIRECTIONS

cache = {}
NAME = "BFS"
MAX_WALK = INF


class Graph:
    # do thi cac o di duoc: AL[u] = [(v, chi phi)], giong Graph trong BTVN
    def __init__(self, cells):
        self.AL = {}
        for u in cells:
            self.AL[u] = []
            for action in DIRECTIONS:
                v = shift(u, action)
                if v in cells:
                    self.AL[u].append((v, 1))


class BFS:
    def search(self, g, src, dst):
        expanded = []
        queue = deque([src])
        parent = {src: None}
        while queue:
            u = queue.popleft()
            expanded.append(u)
            if u == dst:
                break
            for v, _ in g.AL.get(u, []):
                if v not in parent:
                    parent[v] = u
                    queue.append(v)

        if dst in parent:
            cur = dst
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
        else:
            path = []
        return expanded, path


ALGORITHM = BFS()


def choose_target(view, max_walk=INF):
    # Buoc 1: chon cho day thung tot nhat (nho nhat h = di bo + 2 * so lan day con lai)
    key = (view.floor, view.goals)
    if key not in cache:
        cache[key] = push_distances(view.floor, view.goals)
    push_dist = cache[key]
    boxes, me, opp = view.state.boxes, view.me, view.opponent
    walk_dist = bfs_distances([me], view.floor - boxes - {opp})
    frontier = []
    for stand, action, box, improving in push_spots(view, push_dist, boxes, {opp}):
        if stand not in walk_dist or walk_dist[stand] > max_walk:
            continue
        h = walk_dist[stand] + 2 * push_dist[shift(box, action)]
        if not improving:
            h += 3  # cuop thung cua doi thu
        heapq.heappush(frontier, (h, stand, action))
    if not frontier:
        return approach_spot(view, push_dist)
    _, stand, action = heapq.heappop(frontier)
    return stand, action


def stay(view):
    # dam vao tuong de dung yen
    for action in DIRECTIONS:
        if shift(view.me, action) not in view.floor:
            return action
    return "North"


def to_action(view, path):
    # buoc dau cua path = o ke ben, doi ra ten huong
    for action in DIRECTIONS:
        if shift(view.me, action) == path[1]:
            return action
    return stay(view)


def choose_action(view, time_limit=1.0):
    target = choose_target(view, MAX_WALK)
    if target is None:
        return stay(view)
    stand, action = target
    if stand == view.me:
        return action  # dang dung dung cho thi day
    # Buoc 2: tim duong di bo toi o stand bang BFS
    cells = view.floor - view.state.boxes - {view.opponent}
    g = Graph(cells)
    expanded, path = ALGORITHM.search(g, view.me, stand)
    if len(path) < 2:
        return stay(view)
    return to_action(view, path)
