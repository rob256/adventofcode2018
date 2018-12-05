from typing import List
import re


def map_to_fabric_graph(fabric_graph: List[List], fabric_input: str, overlaps: set) -> None:
    m = re.search(r'#[0-9]+ @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)', fabric_input)
    start_x = int(m.group(1))
    start_y = int(m.group(2))
    width = int(m.group(3))
    height = int(m.group(4))
    for _x in range(width):
        x = start_x + _x
        for _y in range(height):
            y = start_y + _y
            fabric_graph[x][y] += 1
            if fabric_graph[x][y] == 2:
                overlaps.add((x, y))


def get_number_of_overlaps(input_text: str) -> int:
    all_inputs = input_text.splitlines()
    fabric_graph = [1000 * [0] for i in range(1000)]
    all_overlaps = set()
    for fabric_input in all_inputs:
        map_to_fabric_graph(fabric_graph, fabric_input, all_overlaps)
    return len(all_overlaps)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_number_of_overlaps(input_text))


if __name__ == '__main__':
    main()
