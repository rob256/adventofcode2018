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


def get_answer(score_of_nodes: int) -> int:
    first_node = Node(3)
    first_node.next = first_node
    last_node = append_node(first_node, 7)

    elf1 = first_node
    elf2 = first_node.next

    for x in range(score_of_nodes + 10):
        last_node = append_node(last_node, elf1.value + elf2.value)
        elf1 = move_elf(elf1, elf1.value + 1)
        elf2 = move_elf(elf2, elf2.value + 1)

    return node_value_from(first_node, score_of_nodes)


def main():
    print(get_answer(5))
    print(get_answer(18))
    print(get_answer(2018))
    print(get_answer(702831))


if __name__ == '__main__':
    main()
