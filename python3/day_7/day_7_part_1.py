from typing import Tuple, Iterable


class DependencyNode(object):
    def __init__(self, name):
        self.name = name
        self.depends_on = set()
        self.releases = set()

    def __repr__(self):
        return f"Node<{self.name}>"


def get_base_nodes(all_nodes: Iterable[DependencyNode]) -> Iterable[DependencyNode]:
    for node in all_nodes:
        if not node.depends_on:
            yield node


def create_dependency_graph(step_pairs: Iterable[Tuple[str, str]]) -> Iterable[DependencyNode]:
    all_nodes = {}
    for step_from, step_to in step_pairs:
        node_from = all_nodes.get(step_from, DependencyNode(step_from))
        node_to = all_nodes.get(step_to, DependencyNode(step_to))
        node_from.releases.add(node_to)
        node_to.depends_on.add(node_from)
        all_nodes[step_from] = node_from
        all_nodes[step_to] = node_to
    return get_base_nodes(all_nodes.values())


def get_dependency_pairs(input_text: str) -> Iterable[Tuple[str, str]]:
    for text_line in input_text.splitlines():
        step_from = text_line.split()[1]
        step_to = text_line.split()[7]
        yield step_from, step_to


def get_build_order(dependency_base_nodes: Iterable[DependencyNode]) -> str:
    def node_ready(node: DependencyNode) -> bool:
        for child in node.depends_on:
            if child not in seen_nodes:
                return False
        return True

    build_order = ""
    seen_nodes = set()
    available_nodes = set(dependency_base_nodes)
    while available_nodes:
        for node in sorted(available_nodes, key=lambda x: x.name):
            if node_ready(node):
                seen_nodes.add(node)
                available_nodes.remove(node)
                build_order += node.name
                available_nodes.update(node.releases)
                break
    return build_order


def get_answer(input_text: str) -> str:
    step_pairs = get_dependency_pairs(input_text)
    dependency_base_nodes = create_dependency_graph(step_pairs)
    return get_build_order(dependency_base_nodes)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
