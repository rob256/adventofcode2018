from typing import List, Deque
from collections import deque


def get_answer(input_text: str) -> int:
    number_list = deque(list(map(int, input_text.split())))
    return process_queue(number_list)


def process_queue(input_queue: Deque) -> int:
    child_nodes = input_queue.popleft()
    metadata_entries = input_queue.popleft()
    total_sum = 0
    child_sums = []
    if child_nodes:
        for child_node in range(child_nodes):
            metadata_sum = process_queue(input_queue)
            child_sums.append(metadata_sum)
        for metadata_entry in range(metadata_entries):
            target_child = input_queue.popleft() - 1
            if target_child >= len(child_sums):
                continue
            total_sum += child_sums[target_child]
    else:
        for metadata_entry in range(metadata_entries):
            total_sum += input_queue.popleft()
    return total_sum


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()