from collections import deque

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f'Node({self.value})'


def append_node(last_node: Node, value: int) -> Node:
    if value > 9:
        last_node = append_node(last_node, 1)
    new_node = Node(value % 10)
    first_node = last_node.next
    last_node.next = new_node
    new_node.next = first_node
    return new_node


def move_elf(elf: Node, times: int) -> Node:
    next = elf
    for _ in range(times):
        next = next.next
    return next


def node_value_from(first_node: Node, from_node: int) -> int:
    starting_node = move_elf(first_node, from_node)
    next = starting_node
    total_value = 0
    for x in range(10):
        total_value *= 10
        total_value += next.value
        next = next.next
    return total_value


def get_answer(target_value_str: str) -> int:
    first_node = Node(3)
    first_node.next = first_node
    last_node = append_node(first_node, 7)

    elf1 = first_node
    elf2 = first_node.next

    node_value_digits = len(target_value_str)
    running_nodes = deque([0 for _ in range(node_value_digits)])

    running_nodes[-2] = 3
    running_nodes[-1] = 7

    next = last_node
    x = 2 - node_value_digits

    target_value = int(target_value_str)

    node_value = 37

    while True:
        last_node = append_node(last_node, elf1.value + elf2.value)
        elf1 = move_elf(elf1, elf1.value + 1)
        elf2 = move_elf(elf2, elf2.value + 1)

        x += 1

        next = next.next
        removed = running_nodes.popleft()
        added = next.value
        running_nodes.append(added)

        node_value = node_value - (removed * 10 ** (node_value_digits - 1))
        node_value = node_value * 10
        node_value = node_value + added

        if node_value == target_value:
            break

    return x


def main():
    print(get_answer('51589'))
    print(get_answer('01245'))
    print(get_answer('92510'))
    print(get_answer('702831'))


if __name__ == '__main__':
    main()
