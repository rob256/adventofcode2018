from typing import List, Tuple, Dict


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


def get_sum_of_square(power_grid: List[List[int]], x: int, y: int, size: int, cached: Dict[Tuple[int, int, int], int]={}) -> int:
    if (x, y, size) in cached:
        return cached[(x, y, size)]
    if size == 1:
        total_sum = power_grid[x][y]
        cached[(x, y, 1)] = total_sum
        return total_sum
    else:
        total_sum = get_sum_of_square(power_grid, x, y, size - 1)
        for _x in range(size):
            total_sum += power_grid[x + _x][y]
        for _y in range(size):
            total_sum += power_grid[x][y + _y]
        total_sum += power_grid[x][y]
    return total_sum


def get_sum_matrix(power_grid: List[List[int]]) -> List[List[int]]:
    sum_matrix = [[0 for _ in range(300)] for _ in range(300)]
    for y in range(300):
        sum_matrix[0][y] = power_grid[0][y]
        for x in range(1, 300):
            sum_matrix[x][y] = sum_matrix[x][y - 1] + power_grid[x][y]
    return sum_matrix


def get_square_sum(sum_matrix, x, y, size, previous_sum):
    if previous_sum is not None:
        if y == 0:
            first_col = sum_matrix[x - 1][y + size - 1]
            next_col = sum_matrix[x + size - 1][y + size - 1]
        else:
            first_col = sum_matrix[x - 1][y + size - 1] - sum_matrix[x - 1][y - 1]
            next_col = sum_matrix[x + size - 1][y + size - 1] - sum_matrix[x + size - 1][y - 1]
        return previous_sum - first_col + next_col
    total_sum = 0
    for _s in range(size):
        if y == 0:
            total_sum += sum_matrix[x + _s][y + size - 1]
        else:
            total_sum += sum_matrix[x + _s][y + size - 1] - sum_matrix[x + _s][y - 1]
    return total_sum


def find_max_power_coord(sum_matrix: List[List[int]]) -> Tuple[int, int, int]:
    max_sum = float('-inf')
    max_square = None
    for s in range(1, 301):
        for y in range(301 - s):
            previous_sum = None
            for x in range(301 - s):
                square_sum = get_square_sum(sum_matrix, x, y, s, previous_sum=previous_sum)
                if square_sum > max_sum:
                    max_square = (x + 1, y + 1, s)
                    max_sum = square_sum
                previous_sum = square_sum
                # print(f'{s}: {x + 1} {y + 1} = {square_sum}')
    return max_square, max_sum


def get_answer(grid_serial_number: int) -> Tuple[int, int]:
    power_grid = make_power_grid(grid_serial_number)
    sum_matrix = get_sum_matrix(power_grid)
    max_square = find_max_power_coord(sum_matrix)
    return max_square


if __name__ == '__main__':
    # main()
    # print(get_cell_power(8, 3, 5))
    # print(get_cell_power(57, 122, 79))
    # print(get_cell_power(39, 217, 196))
    # print(get_cell_power(71, 101, 153))
    # print(get_answer(18))
    # print(get_answer(42))
    print(get_answer(8979))
