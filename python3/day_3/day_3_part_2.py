from typing import List
import re


def map_to_fabric_graph(fabric_graph: List[List[set]], fabric_input: str, overlaps: set, all_ids: set) -> None:
    m = re.search(r'#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)', fabric_input)
    fabric_id = int(m.group(1))
    start_x = int(m.group(2))
    start_y = int(m.group(3))
    width = int(m.group(4))
    height = int(m.group(5))
    all_ids.add(fabric_id)
    for _x in range(width):
        x = start_x + _x
        for _y in range(height):
            y = start_y + _y
            if fabric_graph[x][y]:
                overlaps.update(fabric_graph[x][y])
                overlaps.add(fabric_id)
            fabric_graph[x][y].add(fabric_id)


def get_number_of_overlaps(input_text: str) -> int:
    all_inputs = input_text.splitlines()
    fabric_graph = []
    for x in range(1000):
        fabric_row = [set() for i in range(1000)]
        fabric_graph.append(fabric_row)
    all_overlaps = set()
    all_ids = set()
    for fabric_input in all_inputs:
        map_to_fabric_graph(fabric_graph, fabric_input, all_overlaps, all_ids)
    return list(all_ids - all_overlaps)[0]


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_number_of_overlaps(input_text))


if __name__ == '__main__':
    main()
