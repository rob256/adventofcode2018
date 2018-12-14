import re
from collections import namedtuple
from typing import List, Tuple


Point = namedtuple('Point', ['x', 'y', 'vol_x', 'vol_y'])
# class Point(object):
#     def __init__(self, x, y, vol_x, vol_y):
#         self.x = x
#         self.y = y
#         self.vol_x = vol_x
#         self.vol_y = vol_y


def get_all_points(input_text: str) -> List[Point]:
    # position=< 9,  1> velocity=< 0,  2>
    points = []
    for line in input_text.splitlines():
        m = re.search(r'position=<(.*), (.*)> velocity=<(.*), (.*)>', line)
        point = Point(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
        points.append(point)
    return points


def get_two_different_points(all_points: List[Point]) -> Tuple[Point, Point]:
    point1 = all_points[0]
    for point in all_points:
        if point.vol_y != point1.vol_y:
            return point1, point


def get_y_intersection(point1: Point, point2: Point) -> int:
    if point1.vol_y < point2.vol_y:
        return get_y_intersection(point2, point1)
    total_y_vol = point1.vol_y - point2.vol_y
    total_y = point2.y - point1.y
    print(f'{total_y} {total_y_vol}')
    y_intersection = int(total_y / total_y_vol)
    return y_intersection


def get_starting_iterations(point: Point, y_intersection: int) -> int:
    # Return less than the intersection
    # point.y - (point.vol_y * X) = y
    # point.y - y = point.vol_y * X
    # (point.y - y) / point.vol_y = X
    return int(((point.y - y_intersection) / point.vol_y) - 10)


def get_max_y(points: List[Point], moves: int) -> int:
    return max([p.y + p.vol_y * moves for p in points])


def get_min_y(points: List[Point], moves: int) -> int:
    return min([p.y + p.vol_y * moves for p in points])


def get_max_x(points: List[Point], moves: int) -> int:
    return max([p.x + p.vol_x * moves for p in points])


def get_min_x(points: List[Point], moves: int) -> int:
    return min([p.x + p.vol_x * moves for p in points])


def print_points(points: List[Point], moves: int) -> None:
    min_x = get_min_x(points, moves)
    max_x = get_max_x(points, moves)
    min_y = get_min_y(points, moves)
    max_y = get_max_y(points, moves)
    x_diff = max_x - min_x + 1
    y_diff = max_y - min_y + 1
    board = [[' ' for _ in range(x_diff)] for _ in range(y_diff)]
    for point in points:
        board[(point.y + point.vol_y * moves) - min_y][(point.x + point.vol_x * moves) - min_x - 1] = '#'

    for row in board:
        print(''.join(row))


def get_answer(input_text: str) -> str:
    all_points = get_all_points(input_text)
    point1, point2 = get_two_different_points(all_points)
    print(point1)
    print(point2)
    y_intersection = abs(get_y_intersection(point1, point2)) - 20
    for x in range(y_intersection, y_intersection + 1000):
        if get_max_y(all_points, x) - get_min_y(all_points, x) <= 15:
            print(x)
            print_points(all_points, x)
            print()


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
