from collections import deque

from utils.matrix import Matrix

_directions = {
    ".": {
        (0, 1): [(0, 1)],
        (0, -1): [(0, -1)],
        (1, 0): [(1, 0)],
        (-1, 0): [(-1, 0)],
    },
    "|" : {
        (0, 1) : [(0, 1)],
        (0, -1) : [(0, -1)],
        (1, 0) : [(0, 1), (0, -1)],
        (-1, 0) : [(0, 1), (0, -1)],
    },
    "-": {
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)],
        (1, 0): [(1, 0)],
        (-1, 0): [(-1, 0)],
    },
    "\\": {
        (0, 1): [(1, 0)],
        (0, -1): [(-1, 0)],
        (1, 0): [(0, 1)],
        (-1, 0): [(0, -1)],
    },
    "/" : {
        (0, 1): [(-1, 0)],
        (0, -1): [(1, 0)],
        (1, 0): [(0, -1)],
        (-1, 0): [(0, 1)],
    }
}

class TheFloorWillBeLava:
    def __init__(self, _contraption):
        self._contraption = Matrix(_contraption)

    def get_energized_tiles_count(self, start: tuple[int, int], direction: tuple[int, int]) -> int:
        energized = set()
        queue = deque([(start, direction)])
        while queue:
            coordinate, direction = queue.popleft()
            if self._contraption.is_out_of_bounds(coordinate) or (coordinate, direction) in energized:
                continue
            x, y = coordinate
            for dx, dy in _directions[self._contraption[coordinate]][direction]:
                queue.append(((x + dx, y + dy), (dx, dy)))
            energized.add((coordinate, direction))
        return len(set(point for point,_ in energized))

    def get_max_energized_tiles_count(self) -> int:
        max_energized = float('-inf')
        for x in range(0, self._contraption.len_x):
            max_energized = max(max_energized,
                                self.get_energized_tiles_count((x, 0), (0, 1)),
                                self.get_energized_tiles_count((x, self._contraption.len_y - 1), (0, -1)))
        for y in range(0, self._contraption.len_y):
            max_energized = max(max_energized,
                                self.get_energized_tiles_count((0, y), (1, 0)),
                                self.get_energized_tiles_count((self._contraption.len_x - 1, y), (-1, 0)))
        return max_energized