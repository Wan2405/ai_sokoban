
from __future__ import annotations

from math import inf

from ..req_5.gui_model import DIRECTIONS

NAME = "Other-DFS"


def shift(cell, action):
    dx, dy = DIRECTIONS[action]
    return cell[0] + dx, cell[1] + dy


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def choose_action(view, time_limit):
    del time_limit
    floor = set(view.floor)
    boxes = set(view.state.boxes)
    opp = view.opponent
    legal = []

    for action in DIRECTIONS:
        nxt = shift(view.me, action)
        if nxt not in floor or nxt == opp:
            continue
        if nxt in boxes:
            pushed = shift(nxt, action)
            if pushed in floor and pushed not in boxes and pushed != opp:
                legal.append(action)
        else:
            legal.append(action)

    if not legal:
        return "South"

    goals = tuple(view.goals)
    if not goals:
        return legal[0]

    def score_after(player, box_set, action):
        nxt = shift(player, action)
        if nxt in box_set:
            pushed = shift(nxt, action)
            new_boxes = set(box_set)
            new_boxes.remove(nxt)
            new_boxes.add(pushed)
            box_set = new_boxes
            player = pushed
        else:
            player = nxt

        # Prefer moving closer to goals while avoiding boxes already near goals.
        goal_distance = 0
        for box in box_set:
            if box in goals:
                goal_distance -= 3
            else:
                goal_distance += min(manhattan(box, goal) for goal in goals)
        player_distance = min(manhattan(player, goal) for goal in goals)
        return -(goal_distance + player_distance)

    best_action = legal[0]
    best_score = -inf
    for action in legal:
        score = score_after(view.me, set(view.state.boxes), action)
        if score > best_score:
            best_score = score
            best_action = action
    return best_action
