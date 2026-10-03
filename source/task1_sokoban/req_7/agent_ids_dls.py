"""Agent IDS/DLS: chọn chỗ đẩy bằng h và tìm đường theo DLS lặp tầng."""
import heapq

from .agent_tools import (
    INF, approach_spot, bfs_distances, push_distances, push_spots, shift,
)
from ..req_5.gui_model import DIRECTIONS

cache = {}
NAME = "IDS/DLS"
MAX_WALK = 10


class Graph:
    # do thi cac o di duoc: AL[u] = [(v, chi phi)], giong Graph trong BTVN
    def __init__(self, cells):
        self.AL = {}
        self.H = {}
        for u in cells:
            self.AL[u] = []
            for action in DIRECTIONS:
                v = shift(u, action)
                if v in cells:
                    self.AL[u].append((v, 1))


class DLS:
    def __init__(self, LIM):
        self.LIM = LIM

    def search(self, g, src, dst):
        expanded = []
        path = []

        def visit(u, depth, ancestors):
            expanded.append(u)
            if u == dst:
                return [u]
            if depth == self.LIM:
                return None
            for v, _ in g.AL.get(u, []):
                if v not in ancestors:
                    result = visit(v, depth + 1, ancestors | {v})
                    if result is not None:
                        return [u] + result
            return None

        result = visit(src, 0, {src})
        if result is not None:
            path = result
        return expanded, path


class IDS:
    # thu DLS voi LIM = 0, 1, 2, ... cho toi khi tim thay (duong ngan nhat)
    def __init__(self, MAX_LIM):
        self.MAX_LIM = MAX_LIM

    def search(self, g, src, dst):
        expanded = []
        path = []
        for limit in range(self.MAX_LIM + 1):
            iteration_expanded, iteration_path = DLS(limit).search(g, src, dst)
            expanded.extend(iteration_expanded)
            if iteration_path:
                path = iteration_path
                break
        return expanded, path


ALGORITHM = IDS(MAX_LIM=MAX_WALK)


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
    # Buoc 2: tim duong di bo toi o stand bang thuat toan cua file nay
    cells = view.floor - view.state.boxes - {view.opponent}
    g = Graph(cells)
    expanded, path = ALGORITHM.search(g, view.me, stand)
    if len(path) < 2:
        return stay(view)
    return to_action(view, path)
