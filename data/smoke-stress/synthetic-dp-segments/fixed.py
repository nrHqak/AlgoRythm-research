"""Synthetic stress fixture: dynamic programming for sequence partitions."""

from __future__ import annotations

from math import inf


def _validate_values(values):
    if not isinstance(values, list):
        raise ValueError("values must be a list")
    for index, value in enumerate(values):
        if not isinstance(value, int):
            raise ValueError(f"value {index} is not an integer")
        if value < 0:
            raise ValueError("values must be non-negative")
    return len(values)

def _validate_limits(max_segments, penalty):
    if not isinstance(max_segments, int) or max_segments < 1:
        raise ValueError("max_segments must be a positive integer")
    if not isinstance(penalty, int) or penalty < 0:
        raise ValueError("penalty must be a non-negative integer")

def _make_cost_table(values):
    length = len(values)
    costs = [[0] * (length + 1) for _ in range(length)]
    for start in range(length):
        minimum = inf
        maximum = -inf
        for end in range(start + 1, length + 1):
            value = values[end - 1]
            minimum = min(minimum, value)
            maximum = max(maximum, value)
            costs[start][end] = (minimum, maximum)
    return costs

def _segment_cost(costs, start, end, penalty):
    minimum, maximum = costs[start][end]
    return maximum - minimum + penalty

def _make_dp(length, max_segments):
    table = []
    parents = []
    for _prefix in range(length + 1):
        table.append([inf] * (max_segments + 1))
        parents.append([None] * (max_segments + 1))
    table[0][0] = 0
    return table, parents

def _candidate(table, costs, start, end, groups, penalty):
    previous = table[start][groups - 1]
    if previous == inf:
        return inf
    return previous + _segment_cost(costs, start, end, penalty)

def _best_split(table, costs, end, groups, penalty):
    best_cost = inf
    best_start = None
    for start in range(end):
        cost = _candidate(table, costs, start, end, groups, penalty)
        if cost < best_cost:
            best_cost = cost
            best_start = start
    return best_cost, best_start

def _fill_group(table, parents, costs, length, groups, penalty):
    for end in range(1, length + 1):
        cost, start = _best_split(table, costs, end, groups, penalty)
        table[end][groups] = cost
        parents[end][groups] = start

def _fill_tables(table, parents, costs, length, max_segments, penalty):
    for groups in range(1, max_segments + 1):
        _fill_group(table, parents, costs, length, groups, penalty)

def _best_terminal(table, length, max_segments):
    options = []
    for groups in range(1, max_segments + 1):
        options.append((table[length][groups], groups))
    if not options:
        return None, None
    cost, groups = min(options)
    if cost == inf:
        return None, None
    return cost, groups

def _trace_segments(parents, length, groups):
    segments = []
    end = length
    while groups > 0:
        start = parents[end][groups]
        if start is None:
            return []
        segments.append((start, end))
        end = start
        groups -= 1
    if end != 0:
        return []
    segments.reverse()
    return segments

def _assert_cover(segments, length):
    if length == 0:
        if segments:
            raise RuntimeError("empty input cannot have segments")
        return
    if not segments:
        raise RuntimeError("non-empty input must have segments")
    cursor = 0
    for start, end in segments:
        if start != cursor or end <= start:
            raise RuntimeError("segments do not form a valid partition")
        cursor = end
    if cursor != length:
        raise RuntimeError("segments do not cover the sequence")

def _recompute(values, segments, penalty):
    total = 0
    for start, end in segments:
        part = values[start:end]
        total += max(part) - min(part) + penalty
    return total

def minimum_partition_cost(values, max_segments, penalty):
    """Return the least range-plus-penalty cost over bounded partitions."""
    length = _validate_values(values)
    _validate_limits(max_segments, penalty)
    if length == 0:
        return 0
    costs = _make_cost_table(values)
    table, parents = _make_dp(length, max_segments)
    _fill_tables(table, parents, costs, length, max_segments, penalty)
    best_cost, groups = _best_terminal(table, length, max_segments)
    if best_cost is None:
        return None
    segments = _trace_segments(parents, length, groups)
    _assert_cover(segments, length)
    if _recompute(values, segments, penalty) != best_cost:
        raise RuntimeError("reconstructed cost disagrees with dynamic program")
    return best_cost
