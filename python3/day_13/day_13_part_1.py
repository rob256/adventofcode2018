from collections import defaultdict
from operator import itemgetter
from typing import Tuple, Dict, List

N, E, S, W = 0, 1, 2, 3
ARROWS = ['^', '>', 'v', '<']
ARROW_REPLACEMENT = ['|', '-', '|', '-']

DIRECTION = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0),
}


class Arrow(object):
    arrow_id = 0

    def __init__(self, x, y, direction):
        self.id = Arrow.arrow_id
        self.x = x
        self.y = y
        self.direction = direction
        self.next_move = 0
        Arrow.arrow_id += 1

    def handle_board_place(self, board_place: str) -> None:
        if board_place in ['|', '-']:
            return
        elif board_place == '/':
            if self.direction == N:
                self.direction = E
            elif self.direction == E:
                self.direction = N
            elif self.direction == S:
                self.direction = W
            elif self.direction == W:
                self.direction = S
        elif board_place == '\\':
            if self.direction == N:
                self.direction = W
            elif self.direction == E:
                self.direction = S
            elif self.direction == S:
                self.direction = E
            elif self.direction == W:
                self.direction = N
        elif board_place == '+':
            self.turn()

    def turn(self) -> None:
        if self.next_move == 0:  # LEFT
            self.direction = (self.direction - 1) % 4
        elif self.next_move == 2:  # FORWARD
            self.direction = (self.direction + 1) % 4
        self.next_move = (self.next_move + 1) % 3

    def __repr__(self):
        return f'{self.id}: ({self.x}, {self.y})'


def analyse_board(board_input: str) -> Tuple[Dict[int, Dict[int, str]], List[Arrow]]:
    board = defaultdict(dict)
    arrows = []
    arrow_id = 0
    for y, line in enumerate(board_input.splitlines()):
        for x, piece in enumerate(line):
            if piece in ARROWS:
                arrows.append(Arrow(x, y, ARROWS.index(piece)))
                piece = ARROW_REPLACEMENT[ARROWS.index(piece)]
                arrow_id += 1
            board[x][y] = piece
    return board, arrows


def sort_arrows_by_coord(arrows: List[Arrow]) -> List[Arrow]:
    return sorted(arrows, key=lambda x: (x.y, x.x))


def move_arrow_on_board(arrow: Arrow, board: Dict[int, Dict[int, str]]) -> None:
    arrow.x = arrow.x + DIRECTION[arrow.direction][0]
    arrow.y = arrow.y + DIRECTION[arrow.direction][1]
    next_place = board[arrow.x][arrow.y]
    arrow.handle_board_place(next_place)


def get_answer(input_text: str) -> Tuple[int, int]:
    board, arrows = analyse_board(input_text)
    occupied_squares = {(arrow.x, arrow.y) for arrow in arrows}
    print(arrows)
    while True:
        print('Next Move')
        for arrow in sort_arrows_by_coord(arrows):
            x = arrow.x
            y = arrow.y
            move_arrow_on_board(arrow, board)
            new_x = arrow.x
            new_y = arrow.y
            if (new_x, new_y) in occupied_squares:
                return new_x, new_y
            occupied_squares.remove((x, y))
            occupied_squares.add((new_x, new_y))
            print(arrows)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
