from typing import List, Union, Tuple, Dict, Set
from collections import deque, defaultdict
import copy


DIRECTIONS = [
    (0, -1),
    (-1, 0),
    (1, 0),
    (0, 1),
]


BoardPiece = Union["Player", str]
Board = Dict[int, Dict[int, BoardPiece]]


def sort_order(pos):
    return pos.y, pos.x


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack_power = 3
        self.health = 200

    def is_alive(self):
        return self.health > 0

    def move(self, board: Board, players: List["Player"]) -> None:
        if not self.in_range_of_enemy(board):
            self.move_towards_closest_enemy(board, players)
        if self.in_range_of_enemy(board):
            self.attack_lowest_enemy(board)

    def in_range_of_enemy(self, board: Board) -> bool:
        for _x, _y in DIRECTIONS:
            board_piece = board[self.x + _x][self.y + _y]
            if self.is_enemy(board_piece):
                return True
        return False

    def is_enemy(self, board_piece: BoardPiece):
        if isinstance(board_piece, Player):
            if board_piece.player_type == self.enemy:
                return True
        return False

    def move_towards_closest_enemy(self, board: Board, players: List["Player"]) -> None:
        closest_enemy_square = self.get_closest_enemy_square(board, players)
        old_closest_enemy = self._old_get_closest_enemy_square(board)
        if closest_enemy_square != old_closest_enemy:
            print('something wrong')
        if closest_enemy_square:
            self.move_towards_coord(board, *closest_enemy_square)

    def get_valid_neighbours(self, board: Board) -> List[Tuple[int, int]]:
        valid_neighbours = []
        for neighbour in get_neighbours(self.x, self.y):
            if get_piece(board, neighbour) == '.':
                valid_neighbours.append(neighbour)
        return valid_neighbours

    def move_towards_coord(self, board: Board, x: int, y: int) -> None:
        my_neighbours = set(self.get_valid_neighbours(board))
        if x == 21 and y == 11 and (21, 9) in my_neighbours:
            print('maybe here')
        old_next_x, old_next_y = self._find_cord_to_move_to(board, x, y)
        next_x, next_y = self.get_closest_coord_from_list(board, (x, y), my_neighbours)
        if old_next_x != next_x or old_next_y != next_y:
            print('here')
        board[self.x][self.y] = '.'
        board[next_x][next_y] = self
        self.x = next_x
        self.y = next_y

    def get_closest_coord_from_list(self, board: Board, from_coord: Tuple[int, int], to_coords: Set[Tuple[int, int]]) -> Union[Tuple[int, int], None]:
        if from_coord in to_coords:
            return from_coord

        move_queue = deque([])
        for neighbour in get_neighbours(*from_coord):
            move_queue.append((neighbour, 1))

        board_copy = copy_board(board)

        target_coord_depth = []

        while move_queue:
            (x, y), depth = move_queue.popleft()
            if board_copy[x][y] != '.':
                continue
            if (x, y) in to_coords:
                target_coord_depth.append((depth, y, x))
            board_copy[x][y] = depth
            neighbours = get_neighbours(x, y)
            for neighbour in neighbours:
                board_piece = get_piece(board_copy, neighbour)
                if board_piece == '.':
                    move_queue.append((neighbour, depth + 1))

        if target_coord_depth:
            closest_coord = min(target_coord_depth)
            return closest_coord[2], closest_coord[1]
        return None

    def get_closest_enemy_square(self, board: Board, players: List["Player"]) -> Union[Tuple[int, int], None]:
        enemy_neighbours = self.get_enemy_neighbours(players)
        return self.get_closest_coord_from_list(board, (self.x, self.y), enemy_neighbours)

    def get_enemy_neighbours(self, players: List["Player"]) -> Set[Tuple[int, int]]:
        enemy_neighbours = set()
        for player in players:
            if self.is_enemy(player) and player.is_alive():
                enemy_neighbours.update(get_neighbours(player.x, player.y))
        return enemy_neighbours

    def _old_get_closest_enemy_square(self, board: Board) -> Union[Tuple[int, int], None]:
        move_queue = deque([n for n in self.get_valid_neighbours(board)])
        board_copy = copy_board(board)

        while move_queue:
            x, y = move_queue.popleft()
            if board_copy[x][y] != '.':
                continue
            board_copy[x][y] = 'x'
            neighbours = get_neighbours(x, y)
            for neighbour in neighbours:
                board_piece = get_piece(board_copy, neighbour)
                if self.is_enemy(board_piece):
                    return x, y
                elif board_piece == '.':
                    move_queue.append(neighbour)
        return None

    def _find_cord_to_move_to(self, board: Board, x: int, y: int) -> Tuple[int, int]:
        valid_moves = set(self.get_valid_neighbours(board))
        if (x, y) in valid_moves:
            return x, y
        move_queue = deque([p for p in get_neighbours(x, y) if get_piece(board, p) == '.'])
        board_copy = copy_board(board)

        while move_queue:
            x, y = move_queue.popleft()
            if (x, y) in valid_moves:
                return x, y
            if board_copy[x][y] == 'x':
                continue
            board_copy[x][y] = 'x'
            for neighbour in get_neighbours(x, y):
                board_piece = get_piece(board_copy, neighbour)
                if board_piece == '.':
                    move_queue.append(neighbour)

    def attack_lowest_enemy(self, board: Board) -> None:
        lowest_enemy = self.get_lowest_enemy(board)
        self.attack(board, lowest_enemy)

    def get_lowest_enemy(self, board: Board) -> "Player":
        enemies = []
        for neighbour in get_neighbours(self.x, self.y):
            board_piece = get_piece(board, neighbour)
            if self.is_enemy(board_piece):
                enemies.append(board_piece)

        lowest_health = float('inf')
        lowest_enemy = None
        for enemy in enemies:
            if enemy.health < lowest_health:
                lowest_health = enemy.health
                lowest_enemy = enemy

        return lowest_enemy

    def attack(self, board: Board, enemy: "Player") -> None:
        print(f'{self}({self.x},{self.y}) attacking {enemy}({enemy.x},{enemy.y},{enemy.health})')
        enemy.health = max(0, enemy.health - self.attack_power)
        if not enemy.is_alive():
            board[enemy.x][enemy.y] = '.'

    def __repr__(self):
        return f'{self.player_type[0]}'


class Goblin(Player):
    player_type = 'GOBLIN'
    enemy = 'ELF'

    def __init__(self, x, y):
        super(Goblin, self).__init__(x, y)


class Elf(Player):
    player_type = 'ELF'
    enemy = 'GOBLIN'

    def __init__(self, x, y):
        super(Elf, self).__init__(x, y)


def copy_board(board: Board) -> Board:
    return copy.deepcopy(board)


def get_piece(board: Board, coord: Tuple[int, int]) -> BoardPiece:
    return board[coord[0]][coord[1]]


def get_neighbours(x: int, y: int) -> List[Tuple[int, int]]:
    board_pieces = []
    for _x, _y in DIRECTIONS:
        board_pieces.append((x + _x, y + _y))
    return board_pieces


def sort_players_by_coord(player_list: List[Player]):
    return sorted(player_list, key=lambda pos: (pos.y, pos.x))


def move_game(board: Board, elves: List[Elf], goblins: List[Goblin]) -> bool:
    for player in [player for player in sort_players_by_coord(elves + goblins) if player.is_alive()]:
        if not(at_least_one_alive(elves) and at_least_one_alive(goblins)):
            return False
        if player.is_alive():
            player.move(board, elves + goblins)
        print_board(board)
        print()
    return True


def at_least_one_alive(players: List[Player]) -> bool:
    for player in players:
        if player.is_alive():
            return True
    return False


def game_is_still_active(elves: List[Elf], goblins: List[Goblin]) -> bool:
    if at_least_one_alive(elves) and at_least_one_alive(goblins):
        return True
    return False


def parse_board_input(input_text: str) -> Tuple[Board, List[Elf], List[Goblin]]:
    board = defaultdict(dict)
    elves = []
    goblins = []
    for y, line in enumerate(input_text.splitlines()):
        for x, text in enumerate(line):
            if text == 'G':
                board_piece = Goblin(x, y)
                goblins.append(board_piece)
            elif text == 'E':
                board_piece = Elf(x, y)
                elves.append(board_piece)
            elif text == "#":
                board_piece = "#"
            else:
                board_piece = text
            board[x][y] = board_piece
    return board, elves, goblins


def print_board(board: Board):
    rows = len(board)
    columns = len(board[0])

    for y in range(rows):
        for x in range(columns):
            print(board[x][y], end='')
        print()


def get_total_health(players: List[Player]) -> int:
    return sum([player.health for player in players])


def get_answer(input_text: str) -> int:
    board, elves, goblins = parse_board_input(input_text)
    print_board(board)
    print()
    game_move = 0
    while game_is_still_active(elves, goblins):
        game_move += 1
        print(f'Turn {game_move}')
        finished_full_round = move_game(board, elves, goblins)
        print_board(board)

    if not finished_full_round:
        game_move -= 1

    elves_total_health = get_total_health(elves)
    goblins_total_health = get_total_health(goblins)

    return game_move * (elves_total_health + goblins_total_health)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


GAME_1 = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""


GAME_2 = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""

GAME_3 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""

GAME_4 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""

GAME_5 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""

GAME_6 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""

GAME_7 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""

MY_INPUT = """################################
##############..##.#############
###############.##.#############
#####..G#######....#########..##
###......########..########...##
####..#G.#######.G...######...##
####......######...G.#####..####
#####......#####.....#.....G####
###.G..#.#..G..#.G.G....#.######
###..#...#.....G.......#########
###......#....##..........######
###..#.G.#....G...........######
####.G.......G#####......G######
#####....#G..#######.....#######
####........#########...######.#
#######.....#########E..######.#
########....#########.#..#####.#
########....#########E#.E.###..#
########..E.#########......E...#
#######......#######.....E.....#
#######..G....#####.......##.###
#######........G........E.######
#######....................#####
########...............#....####
########.....E..G......##.######
##...#..#.#............##.######
#G.#.#..#.....E........#########
#.................E....#########
###...............#...##########
#####.....#.........#.##########
#####...####.#..#..##..#########
################################"""

if __name__ == '__main__':
    # main()
    # print(get_answer(GAME_1))
    # print(get_answer(GAME_2))
    # print(get_answer(GAME_3))
    # print(get_answer(GAME_4))
    # print(get_answer(GAME_5))
    # print(get_answer(GAME_6))
    # print(get_answer(GAME_7))
    print(get_answer(MY_INPUT))
