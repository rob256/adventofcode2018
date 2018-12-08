from typing import Tuple, Iterable, List


class DependencyNode(object):
    def __init__(self, name):
        self.name = name
        self.depends_on = set()
        self.releases = set()
        self.left = node_build_time(self.name)

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


def step_workers(workers: List[DependencyNode]) -> Iterable[DependencyNode]:
    for i, worker in enumerate(workers):
        if worker:
            worker.left -= 1
            if worker.left <= 0:
                workers[i] = None
                yield worker


def workers_are_working(workers: List[DependencyNode]) -> bool:
    for worker in workers:
        if worker:
            return True
    return False


def a_worker_is_available(workers: List[DependencyNode]) -> bool:
    for worker in workers:
        if worker is None:
            return True
    return False


def get_build_time(dependency_base_nodes: Iterable[DependencyNode]) -> int:
    def node_ready(node: DependencyNode) -> bool:
        for child in node.depends_on:
            if child not in seen_nodes:
                return False
        return True

    def node_finished(node):
        seen_nodes.add(node)
        available_nodes.update(node.releases)

    workers = [None, None, None, None, None]

    seen_nodes = set()
    available_nodes = set(dependency_base_nodes)

    time_taken = -1

    while available_nodes or workers_are_working(workers):
        time_taken += 1

        for node in step_workers(workers):
            node_finished(node)

        if not a_worker_is_available(workers):
            continue

        for node in sorted(available_nodes, key=lambda x: x.name):
            if node_ready(node) and a_worker_is_available(workers):
                assign_node_to_available_worker(workers, node)
                available_nodes.remove(node)
    return time_taken


def node_build_time(node_name: str) -> int:
    return 60 + 1 + ord(node_name) - ord('A')


def assign_node_to_available_worker(workers: List[int], build_time: int) -> None:
    for i, worker in enumerate(workers):
        if worker is None:
            workers[i] = build_time
            return


def get_answer(input_text: str) -> int:
    step_pairs = get_dependency_pairs(input_text)
    dependency_base_nodes = create_dependency_graph(step_pairs)
    build_time = get_build_time(dependency_base_nodes)
    return build_time


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
