"""Synthetic stress fixture: layered dynamic programming on a weighted grid."""

from __future__ import annotations

from math import inf

def _validate_weights(weights):
    if not weights or not weights[0]:
        raise ValueError("weights must be a non-empty rectangular list")
    width = len(weights[0])
    for row in weights:
        if len(row) != width:
            raise ValueError("weights must be rectangular")
        if any(not isinstance(value, int) or value < 0 for value in row):
            raise ValueError("weights must be non-negative integers")
    return len(weights), width
def _validate_coupons(coupons):
    if not isinstance(coupons, int):
        raise ValueError("coupons must be an integer")
    if coupons < 0:
        raise ValueError("coupons cannot be negative")
    if coupons > 4:
        raise ValueError("the synthetic fixture supports at most four coupons")
def _normalize_blocked(blocked, height, width):
    normalized = set()
    for row, column in blocked or []:
        if row < 0 or row >= height or column < 0 or column >= width:
            raise ValueError("blocked coordinate is outside the grid")
        normalized.add((row, column))
    return normalized
def _make_table(height, width, coupons):
    table = []
    for _row in range(height):
        row_states = []
        for _column in range(width):
            row_states.append([inf] * (coupons + 1))
        table.append(row_states)
    return table
def _make_parent_table(height, width, coupons):
    parents = []
    for _row in range(height):
        row_states = []
        for _column in range(width):
            row_states.append([None] * (coupons + 1))
        parents.append(row_states)
    return parents
def _candidate_predecessors(table, row, column, used):
    candidates = []
    if row > 0:
        candidates.append((table[row - 1][column][used], row - 1, column))
    if column > 0:
        candidates.append((table[row][column - 1][used], row, column - 1))
    return candidates
def _best_predecessor(table, row, column, used):
    candidates = _candidate_predecessors(table, row, column, used)
    if not candidates:
        return inf, None
    best_cost, best_row, best_column = min(candidates, key=lambda item: item[0])
    if best_cost == inf:
        return inf, None
    return best_cost, (best_row, best_column, used)
def _ordinary_transition(table, row, column, used, weight):
    previous_cost, previous_state = _best_predecessor(table, row, column, used)
    if previous_cost == inf:
        return inf, None
    return previous_cost + weight, previous_state
def _coupon_transition(table, row, column, used):
    previous_cost, previous_state = _best_predecessor(table, row, column, used - 1)
    if previous_cost == inf:
        return inf, None
    return previous_cost, previous_state
def _choose_transition(ordinary, discounted):
    ordinary_cost, ordinary_parent = ordinary
    discounted_cost, discounted_parent = discounted
    if discounted_cost < ordinary_cost:
        return discounted_cost, discounted_parent, True
    return ordinary_cost, ordinary_parent, False

def _initialize_start(table, parents, start_weight, coupons):
    table[0][0][0] = start_weight
    parents[0][0][0] = (None, False)
    for used in range(1, coupons + 1):
        table[0][0][used] = 0
        parents[0][0][used] = (None, True)

def _fill_cell(table, parents, row, column, weight, coupons):
    for used in range(coupons + 1):
        ordinary = _ordinary_transition(table, row, column, used, weight)
        discounted = (inf, None)
        if used > 1:
            discounted = _coupon_transition(table, row, column, used)
        cost, parent, used_coupon = _choose_transition(ordinary, discounted)
        table[row][column][used] = cost
        parents[row][column][used] = (parent, used_coupon)

def _fill_table(weights, blocked, coupons, table, parents):
    height = len(weights)
    width = len(weights[0])
    for row in range(height):
        for column in range(width):
            if row == 0 and column == 0:
                continue
            if (row, column) in blocked:
                continue
            weight = weights[row][column]
            _fill_cell(table, parents, row, column, weight, coupons)

def _best_terminal_state(table, height, width):
    terminal = table[height - 1][width - 1]
    best_cost = min(terminal)
    if best_cost == inf:
        return None, None
    return best_cost, terminal.index(best_cost)

def _trace_path(parents, height, width, used):
    path = []
    row, column = height - 1, width - 1
    while True:
        path.append((row, column))
        entry = parents[row][column][used]
        if entry is None:
            return []
        previous, used_coupon = entry
        if previous is None:
            break
        if used_coupon:
            used -= 1
        row, column, _previous_used = previous
    path.reverse()
    return path

def _assert_path_shape(path, height, width):
    if not path:
        return
    if path[0] != (0, 0) or path[-1] != (height - 1, width - 1):
        raise RuntimeError("reconstructed path has invalid endpoints")
    for previous, current in zip(path, path[1:]):
        row_change = current[0] - previous[0]
        column_change = current[1] - previous[1]
        if (row_change, column_change) not in {(1, 0), (0, 1)}:
            raise RuntimeError("reconstructed path contains an invalid move")

def minimum_route_cost(weights, blocked, coupons):
    """Return minimum entry cost moving right/down, with optional free cells."""
    height, width = _validate_weights(weights)
    _validate_coupons(coupons)
    blocked_cells = _normalize_blocked(blocked, height, width)
    if (0, 0) in blocked_cells or (height - 1, width - 1) in blocked_cells:
        return None
    table = _make_table(height, width, coupons)
    parents = _make_parent_table(height, width, coupons)
    _initialize_start(table, parents, weights[0][0], coupons)
    _fill_table(weights, blocked_cells, coupons, table, parents)
    best_cost, used = _best_terminal_state(table, height, width)
    if best_cost is None:
        return None
    path = _trace_path(parents, height, width, used)
    _assert_path_shape(path, height, width)
    return best_cost
