import re
from collections import defaultdict
from typing import Dict


Board = Dict[int, Dict[int, str]]


def get_clay_coords(input_text: str):
    for line in input_text.splitlines():
        # x=581, y=396..399
        m = re.search(r'.=(.*), .=(.*)\.\.(.*)', line)
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        for i in range(b, c + 1):
            if line.startswith('x'):
                yield a, i
            else:
                yield i, a


def print_board(board: Board, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x in board and y in board[x]:
                print(board[x][y], end='')
            else:
                print('.', end='')
        print()


def print_local_board(board: Board, current_x: int, current_y: int):
    print_board(board, current_x - 20, current_x + 20, current_y - 10, current_y + 10)


def get_answer(input_text: str):
    board = defaultdict(lambda: defaultdict(lambda: '.'))

    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    for x, y in get_clay_coords(input_text):
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        board[x][y] = '#'

    print_board(board, min_x, max_x, min_y, max_y)

    total_water = 0
    flowing_water = [(500, min_y - 1)]
    water_operation = [0]
    water_blocked = [[0,0]]

    while flowing_water:
        print()
        x, y = flowing_water[-1]
        # print_local_board(board, x, y)
        if y > max_y:
            board[x][y] = '|'
            water_blocked.pop()
            water_operation.pop()
            flowing_water.pop()
            total_water -= 1
            continue
        if water_blocked[-1][0] == 1 and water_blocked[-1][1] == 1:
            if flowing_water[-1][1] != flowing_water[-2][1]:
                board[x][y] = '~'
                # Left
                _x = -1
                while True:
                    if board[x + _x][y] == '#':
                        break
                    board[x + _x][y] = '~'
                    x -= 1
                # Right
                _x = 1
                while True:
                    if board[x + _x][y] == '#':
                        break
                    board[x + _x][y] = '~'
                    x += 1
                water_blocked.pop()
                water_operation.pop()
                flowing_water.pop()
                continue

        if water_operation[-1] == 0:
            board[x][y] = '|'
            if board[x][y + 1] == '.':
                flowing_water.append((x, y + 1))
                water_operation.append(0)
                water_blocked.append([0, 0])
                total_water += 1
                continue
            elif board[x][y + 1] == '#' or board[x][y + 1] == '~':
                water_operation[-1] = 1
            elif board[x][y + 1] == '|':
                water_blocked.pop()
                water_operation.pop()
                flowing_water.pop()
                continue
        if water_operation[-1] == 1:
            if water_blocked[-1][0] == 1:
                if flowing_water[-2][1] == flowing_water[-1][1]:
                    water_blocked[-2][0] = 1
                water_operation[-1] = 2
            elif board[x - 1][y] == '.':
                flowing_water.append((x - 1, y))
                water_operation.append(0)
                water_blocked.append([0, 0])
                total_water += 1
                continue
            elif board[x - 1][y] == '#':
                water_blocked[-1][0] = 1
                if flowing_water[-2][1] == flowing_water[-1][1]:
                    water_blocked[-2][0] = 1
                water_operation[-1] = 2
            else:
                water_operation[-1] = 2
        if water_operation[-1] == 2:
            if water_blocked[-1][1] == 1:
                if flowing_water[-2][1] == flowing_water[-1][1]:
                    water_blocked[-2][1] = 1
                water_blocked.pop()
                water_operation.pop()
                flowing_water.pop()
                continue
            if board[x + 1][y] == '.':
                flowing_water.append((x + 1, y))
                water_operation.append(0)
                water_blocked.append([0, 0])
                total_water += 1
                continue
            elif board[x + 1][y] == '#':
                if flowing_water[-2][1] == flowing_water[-1][1]:
                    water_blocked[-2][1] = 1
                water_blocked[-1][1] = 1
            elif board[x + 1][y] == '|':
                water_blocked.pop()
                water_operation.pop()
                flowing_water.pop()

    print_board(board, min_x, max_x, min_y, max_y)

    return total_water


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
