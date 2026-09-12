"""Synthetic large brute-force fixture; never scientific data."""


def normalize_grid(rows):
    width = max((len(row) for row in rows), default=0)
    return [row.ljust(width, ".") for row in rows]


def rectangle_score(grid, top, left, bottom, right):
    score = 0
    blocked = 0
    border = 0
    for row in range(top, bottom + 1):
        for column in range(left, right + 1):
            cell = grid[row][column]
            if cell == "#":
                blocked += 1
            elif cell.isdigit():
                score += int(cell)
            else:
                score += 1
            if row in (top, bottom) or column in (left, right):
                border += 1
    if blocked:
        return None
    return score - border


def candidate_key(candidate):
    score, top, left, bottom, right = candidate
    area = (bottom - top + 1) * (right - left + 1)
    return score, -area, -top, -left, -bottom, -right


def best_rectangle(rows):
    grid = normalize_grid(rows)
    height = len(grid)
    width = len(grid[0]) if grid else 0
    best = None
    for top in range(height):
        for left in range(width):
            for bottom in range(top, height):
                for right in range(left, width):
                    score = rectangle_score(grid, top, left, bottom, right)
                    if score is None:
                        continue
                    candidate = (score, top, left, bottom, right)
                    if best is None or candidate_key(candidate) < candidate_key(best):
                        best = candidate
    return best


def render_answer(candidate):
    if candidate is None:
        return "NONE"
    score, top, left, bottom, right = candidate
    return f"{score} {top} {left} {bottom} {right}"


def parse(text):
    lines = [line.rstrip("\n") for line in text.splitlines()]
    if not lines:
        return []
    height, width = map(int, lines[0].split())
    rows = lines[1 : 1 + height]
    if len(rows) != height:
        raise ValueError("missing grid rows")
    if any(len(row) != width for row in rows):
        raise ValueError("invalid grid width")
    return rows


def solve(text):
    rows = parse(text)
    return render_answer(best_rectangle(rows))


def brute_force_reference(rows):
    """A deliberately verbose cross-check used only by the synthetic fixture."""
    grid = normalize_grid(rows)
    candidates = []
    for top in range(len(grid)):
        for left in range(len(grid[0])):
            for height in range(1, len(grid) - top + 1):
                for width in range(1, len(grid[0]) - left + 1):
                    bottom = top + height - 1
                    right = left + width - 1
                    score = rectangle_score(grid, top, left, bottom, right)
                    if score is not None:
                        candidates.append((score, top, left, bottom, right))
    if not candidates:
        return None
    return max(candidates, key=candidate_key)


def self_check(rows):
    direct = best_rectangle(rows)
    reference = brute_force_reference(rows)
    return direct == reference


def format_grid(rows):
    return "\n".join(normalize_grid(rows))


def dimensions(rows):
    normalized = normalize_grid(rows)
    return len(normalized), len(normalized[0]) if normalized else 0


def occupied_cells(rows):
    normalized = normalize_grid(rows)
    return sum(cell != "#" for row in normalized for cell in row)


def blocked_cells(rows):
    normalized = normalize_grid(rows)
    return sum(cell == "#" for row in normalized for cell in row)


def summary(rows):
    height, width = dimensions(rows)
    return {
        "height": height,
        "width": width,
        "occupied": occupied_cells(rows),
        "blocked": blocked_cells(rows),
    }


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
