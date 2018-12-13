from collections import defaultdict
from typing import List, Tuple


def place_marble(board: List[int], marble: int, current_pos) -> Tuple[int, int]:
    if len(board) == 0:
        board.append(marble)
        return 0, 0
    elif len(board) == 1:
        board.append(marble)
        return 0, 1

    if marble % 23 == 0:
        target_marble = (current_pos - 7) % len(board)
        target_score = board[target_marble]
        if target_marble == len(board) - 1:
            new_position = 0
        else:
            new_position = target_marble
        board.pop(target_marble)
        return marble + target_score, new_position

    new_position = (current_pos + 2) % len(board)
    if new_position == 0:
        new_position = len(board)

    board.insert(new_position, marble)

    return 0, new_position


def get_game_details(input_text: str) -> Tuple[int, int]:
    number_of_players = int(input_text.split()[0])
    last_marble_worth = int(input_text.split()[6])
    return number_of_players, last_marble_worth


def get_answer(input_text: str) -> int:
    number_of_players, last_marble_worth = get_game_details(input_text)
    player_scores = defaultdict(int)
    board = []
    current_player = -1
    current_pos = 0
    for i in range(last_marble_worth + 1):
        current_player = (current_player + 1) % number_of_players
        score, current_pos = place_marble(board, i, current_pos)
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
