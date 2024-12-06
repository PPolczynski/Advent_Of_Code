_guard = "^"
_obstacle = "#"
_initial_direction = (-1, 0)
_rotations = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)
}

class GuardGallivant:
    def __init__(self, maze: list[str]):
        self._maze = maze
        self._rows_cnt = len(maze)
        self._columns_cnt = len(maze[0])

        def get_initial_position():
            for row_id, row in enumerate(self._maze):
                for column_id, column in enumerate(row):
                    if column == _guard:
                        return row_id, column_id

        self._guard_position = get_initial_position()

    def _is_out_of_bounds(self, row_id: int, column_id: int) -> bool:
        return 0 > column_id or column_id >= self._columns_cnt or 0 > row_id or row_id >= self._rows_cnt

    def get_guard_move_count(self) -> int:
        row_id, column_id = self._guard_position
        offset_r, offset_c = _initial_direction
        visited = set()
        while True:
            visited.add((row_id, column_id))
            nxt_r, nxt_c = row_id + offset_r, column_id + offset_c
            if self._is_out_of_bounds(nxt_r, nxt_c):
                break
            elif self._maze[nxt_r][nxt_c] == _obstacle:
                offset_r, offset_c = _rotations[(offset_r, offset_c)]
            else:
                row_id, column_id = nxt_r, nxt_c
        return len(visited)

    def get_possible_loop_count(self) -> int:
        initial_position = self._guard_position
        row_id, column_id = initial_position
        offset_r, offset_c = _initial_direction
        known_possible_obstacles = set()
        visited = set()
        while True:
            nxt_r, nxt_c = row_id + offset_r, column_id + offset_c
            if self._is_out_of_bounds(nxt_r, nxt_c):
                break
            elif self._maze[nxt_r][nxt_c] == _obstacle:
                offset_r, offset_c = _rotations[(offset_r, offset_c)]
            else:
                if ((nxt_r, nxt_c) not in visited
                        and (nxt_r, nxt_c) not in known_possible_obstacles
                        and self._simulate_obstacle_loops((row_id, column_id), (nxt_r, nxt_c), (offset_r, offset_c))):
                    known_possible_obstacles.add((nxt_r, nxt_c))
                visited.add((row_id, column_id))
                row_id, column_id = nxt_r, nxt_c
        return len(known_possible_obstacles)

    def _simulate_obstacle_loops(self, current_position: tuple[int, int],
                           simulated_obstacle: tuple[int, int], s_direction: tuple[int, int]) -> bool:
        row_id, column_id = current_position
        offset_r, offset_c = s_direction
        visited = set()
        while True:
            nxt_r, nxt_c = row_id + offset_r, column_id + offset_c
            if self._is_out_of_bounds(nxt_r, nxt_c):
                return False
            elif (row_id, column_id, offset_r, offset_c) in visited:
                # self._print_loop(simulated_obstacle, visited)
                return True
            elif self._maze[nxt_r][nxt_c] == _obstacle or (nxt_r, nxt_c) == simulated_obstacle:
                offset_r, offset_c = _rotations[(offset_r, offset_c)]
            else:
                visited.add((row_id, column_id, offset_r, offset_c))
                row_id, column_id = nxt_r, nxt_c

    def _print_loop(self, new_obstacle: tuple[int, int], visited: set) -> None:
        out = []
        visited_dict = dict()
        for row_id, column_id, offset_r, offset_c in list(visited):
            if (row_id, column_id) in visited_dict:
                visited_dict[(row_id, column_id)] = "+"
            else:
                visited_dict[(row_id, column_id)] = "|" if abs(offset_r) == 1 else "-"
        for row_id, row in enumerate(self._maze):
            out.append([])
            for column_id, column in enumerate(row):
                if (row_id, column_id) == new_obstacle:
                    out[row_id].append("o")
                elif (row_id, column_id) in visited_dict:
                    out[row_id].append(visited_dict[row_id, column_id])
                else:
                    out[row_id].append(column)
        print("***")
        for row in out:
            print("".join(row))
        print("***")
