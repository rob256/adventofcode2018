from collections import defaultdict, deque
from typing import List, Tuple, Deque


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None
        self.before = None


def add_marble_to_board(board: Node, marble: int) -> Node:
    new_marble = Node(marble)
    next_node = board.next
    next_next_node = next_node.next
    next_node.next = new_marble
    next_next_node.before = new_marble
    new_marble.next = next_next_node
    new_marble.before = next_node
    return new_marble


def remove_marble_from_board(board: Node) -> Tuple[Node, int]:
    target_node = board.before.before.before.before.before.before.before
    target_value = target_node.value
    target_before = target_node.before
    target_next = target_node.next
    target_before.next = target_next
    target_next.before = target_before
    return target_next, target_value


def place_marble(marble: int, current_pos: Node) -> Tuple[int, Node]:
    if marble % 23 == 0:
        new_position, score = remove_marble_from_board(current_pos)
        return marble + score, new_position

    new_position = add_marble_to_board(current_pos, marble)

    return 0, new_position


def get_game_details(input_text: str) -> Tuple[int, int]:
    number_of_players = int(input_text.split()[0])
    last_marble_worth = int(input_text.split()[6])
    return number_of_players, last_marble_worth


def setup_board() -> Node:
    board = Node(0)
    board.next = board
    board.before = board
    return board


def get_answer(input_text: str) -> int:
    number_of_players, last_marble_worth = get_game_details(input_text)
    player_scores = defaultdict(int)
    current_player = 0
    current_pos = setup_board()
    for i in range(1, last_marble_worth + 1):
        if i % 1000 == 0:
            print(f'{i}...')
        current_player = (current_player + 1) % number_of_players
        score, current_pos = place_marble(i, current_pos)
        player_scores[current_player] += score

    return max(player_scores.values())


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    # print(get_answer("9 players; last marble is worth 25 points"))
    # print(get_answer("10 players; last marble is worth 1618 points"))
    # print(get_answer("13 players; last marble is worth 7999 points"))
    print(get_answer("455 players; last marble is worth 7122300 points"))
    # main()
