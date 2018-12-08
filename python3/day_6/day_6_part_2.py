from typing import List, Tuple


def get_distance_from_point(point: Tuple[int, int], target: Tuple[int, int]) -> int:
    x_diff = abs(point[0] - target[0])
    y_diff = abs(point[1] - target[1])
    return x_diff + y_diff


def get_distance_from_all_points(all_points: List[Tuple[int, int]], target: Tuple[int, int]) -> int:
    total_distance = 0
    for point in all_points:
        total_distance += get_distance_from_point(target, point)
    return total_distance


def get_all_coords(input_text: str) -> List[Tuple[int, int]]:
    all_coords = []
    for coord_string in input_text.splitlines():
        x, y = map(int, coord_string.replace(' ', '').split(','))
        all_coords.append((x, y))
    return all_coords


def get_answer(input_text: str) -> int:
    all_coords = get_all_coords(input_text)
    left = min([coord[0] for coord in all_coords])
    right = max([coord[0] for coord in all_coords])
    top = min([coord[1] for coord in all_coords])
    bottom = max([coord[1] for coord in all_coords])
    width = right - left + 1
    height = bottom - top + 1

    total_less_10000 = 0

    for _x in range(width + 1000):
        x = _x - 500
        for _y in range(height + 1000):
            y = _y - 500
            if get_distance_from_all_points(all_coords, (x, y)) < 10000:
                total_less_10000 += 1

    return total_less_10000


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
