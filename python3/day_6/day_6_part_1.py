from collections import defaultdict, deque, namedtuple
from operator import itemgetter
from typing import List, Tuple, Iterable, Deque, Set


ALL_DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

Point = namedtuple('Point', ['owner', 'depth'])


def get_all_coords(input_text: str) -> List[Tuple[int, int]]:
    all_coords = []
    for coord_string in input_text.splitlines():
        x, y = map(int, coord_string.replace(' ', '').split(','))
        all_coords.append((x, y))
    return all_coords


def get_max_left(coords: List[Tuple[int, int]]) -> int:
    max_left = float('inf')
    for x, _ in coords:
        max_left = min(max_left, x)
    return max_left


def get_max_right(coords: List[Tuple[int, int]]) -> int:
    max_right = float('-inf')
    for x, _ in coords:
        max_right = max(max_right, x)
    return max_right


def get_max_top(coords: List[Tuple[int, int]]) -> int:
    max_top = float('inf')
    for _, y in coords:
        max_top = min(max_top, y)
    return max_top


def get_max_bottom(coords: List[Tuple[int, int]]) -> int:
    max_bottom = float('-inf')
    for _, y in coords:
        max_bottom = max(max_bottom, y)
    return max_bottom


def get_coord_matrix(max_right: int, max_bottom: int) -> List[List[Point]]:
    matrix = []
    for _ in range(max_right + 1):
        row = []
        for _ in range(max_bottom + 1):
            row.append(Point(0, 0))
        matrix.append(row)
    return matrix


def make_initial_coord_queue(all_coords: List[Tuple[int, int]]) -> Deque[Tuple[int, int, int, int]]:
    coord_queue = deque([])
    for i, (x, y) in enumerate(all_coords):
        coord_queue.append((i + 1, x, y, 0))
    return coord_queue


def get_max_area(area_counts: dict, inf_coords: Set[int]) -> int:
    if not area_counts:
        return 0
    for coord_id, area in sorted(area_counts.items(), key=itemgetter(1), reverse=True):
        if coord_id not in inf_coords:
            return area


def print_matrix(matrix: List[List[Point]]) -> None:
    matrix_width = len(matrix)
    matrix_height = len(matrix[0])

    for x in range(matrix_height):
        row = [matrix[y][x].owner for y in range(matrix_width)]
        print(' '.join([str(i) for i in row]))


def get_inf_coords(matrix: List[List[Point]], left: int, right: int, top: int, bottom: int) -> Set[int]:
    inf_coords = set()
    height = top - bottom + 1
    width = right - left + 1
    for x in range(width):
        top_point = matrix[left + x][top]
        bottom_point = matrix[left + x][bottom]
        inf_coords.add(top_point.owner)
        inf_coords.add(bottom_point.owner)

    for y in range(height):
        left_point = matrix[left][bottom + y]
        right_point = matrix[right][bottom + y]
        inf_coords.add(left_point.owner)
        inf_coords.add(right_point.owner)

    return inf_coords


def get_answer(input_text: str) -> int:
    all_coords = get_all_coords(input_text)
    max_left = get_max_left(all_coords)
    max_top = get_max_top(all_coords)
    max_bottom = get_max_bottom(all_coords)
    max_right = get_max_right(all_coords)
    coord_matrix = get_coord_matrix(max_right, max_bottom)
    area_counts = defaultdict(int)
    coord_queue = make_initial_coord_queue(all_coords)
    inf_coords = set()

    def is_valid(x: int, y: int) -> bool:
        if x < max_left or x > max_right or y < max_top or y > max_bottom:
            return False
        if coord_matrix[x][y][0] > 0:
            return False
        return True

    def get_valid_neighbours(x: int, y: int, depth: int) -> Iterable[Tuple[int, int, int]]:
        for x_delta, y_delta in ALL_DIRECTIONS:
            new_x, new_y = x + x_delta, y + y_delta
            if is_valid(new_x, new_y):
                yield new_x, new_y, depth + 1

    while coord_queue:
        coord_id, x, y, depth = coord_queue.popleft()
        if coord_matrix[x][y][0]:
            existing_entry = coord_matrix[x][y][0]
            existing_depth = coord_matrix[x][y][1]
            if existing_entry != coord_id and existing_entry != -1 and existing_depth == depth:
                area_counts[existing_entry] -= 1
                coord_matrix[x][y] = Point(-1, 0)
            continue
        coord_matrix[x][y] = Point(coord_id, depth)
        area_counts[coord_id] += 1
        for neighbour in get_valid_neighbours(x, y, depth):
            coord_queue.append((coord_id, *neighbour))

    inf_coords = get_inf_coords(coord_matrix, max_left, max_right, max_bottom, max_top)

    return get_max_area(area_counts, inf_coords)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
