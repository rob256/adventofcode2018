from typing import List, Tuple


def get_cell_power(grid_serial_number: int, x: int, y: int) -> int:
    rack_id = x + 10
    power_level_starts = rack_id * y
    added_serial = power_level_starts + grid_serial_number
    multiplied_rack = added_serial * rack_id
    hundreds_digit = multiplied_rack // 100 % 10
    cell_power = hundreds_digit - 5
    return cell_power


def make_power_grid(grid_serial_number: int) -> List[List[int]]:
    power_grid = []
    for x in range(1, 301):
        row = []
        power_grid.append(row)
        for y in range(1, 301):
            cell_power = get_cell_power(grid_serial_number, x, y)
            row.append(cell_power)
    return power_grid


def get_square_value(power_grid: List[List[int]], x: int, y: int) -> int:
    total_sum = 0
    for _x in range(3):
        for _y in range(3):
            total_sum += power_grid[x + _x][y + _y]
    return total_sum


def find_max_power_coord(power_grid: List[List[int]]) -> Tuple[int, int]:
    max_3x3 = float('-inf')
    best_x_y = None
    for x in range(300 - 2):
        for y in range(300 - 2):
            square_total = get_square_value(power_grid, x, y)
            if square_total > max_3x3:
                max_3x3 = square_total
                best_x_y = (x + 1, y + 1)
    return best_x_y


def get_answer(grid_serial_number: int) -> Tuple[int, int]:
    power_grid = make_power_grid(grid_serial_number)
    max_3x3 = find_max_power_coord(power_grid)
    return max_3x3


if __name__ == '__main__':
    # main()
    # print(get_cell_power(8, 3, 5))
    # print(get_cell_power(57, 122, 79))
    # print(get_cell_power(39, 217, 196))
    # print(get_cell_power(71, 101, 153))
    print(get_answer(18))
    print(get_answer(42))
    print(get_answer(8979))
