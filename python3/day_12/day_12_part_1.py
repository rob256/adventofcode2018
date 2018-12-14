from typing import List, Dict, Tuple


def convert_to_number_list(plant_string: str) -> List[int]:
    number_list = []
    for x in list(plant_string):
        if x == '#':
            number_list.append(1)
        else:
            number_list.append(0)
    return number_list


def get_rule_output_from_rule_line(line: str) -> Tuple[Tuple[int, ...], int]:
    rule_input, _, rule_output_str = line.split()
    rule_tuple = tuple(convert_to_number_list(rule_input))
    if rule_output_str == '#':
        rule_output = 1
    else:
        rule_output = 0
    return rule_tuple, rule_output


def parse_input(input_text: str, padding: int=30) -> Tuple[List[int], Dict[Tuple[int, ...], int]]:
    input_lines = input_text.splitlines()
    initial_state_line = input_lines[0].split()[2]
    initial_state = convert_to_number_list(initial_state_line)
    padding_left = [0 for _ in range(padding)]
    padding_right = [0 for _ in range(padding)]
    initial_state = padding_left + initial_state + padding_right
    all_rules = {}
    for line in input_lines[2:]:
        rule, output = get_rule_output_from_rule_line(line)
        all_rules[rule] = output
    return initial_state, all_rules


def apply_rules(state: List[int], rules: Dict[Tuple[int, ...], int]) -> List[int]:
    new_state = state[:]
    for x in range(len(state) - 4):
        current_focus = (state[x], state[x + 1], state[x + 2], state[x + 3], state[x + 4])
        if current_focus in rules:
            new_state[x + 2] = rules[current_focus]
        else:
            new_state[x + 2] = 0
    return new_state


def sum_plants(state: List[int], start_at: int=-30) -> int:
    total_sum = 0
    for i, plant in enumerate(state):
        if plant:
            total_sum += i + start_at
    return total_sum


def get_answer(input_text: str) -> int:
    padding = 230
    generations = 200
    initial_state, rules = parse_input(input_text, padding=padding)
    new_state = initial_state[:]
    print(''.join(['#' if x else '.' for x in new_state]))
    for i in range(generations):
        new_state = apply_rules(new_state, rules)
    plant_sum = sum_plants(new_state, start_at=-padding)
    return plant_sum


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
