import re
from typing import List, Tuple


Registers = List[int]


def addr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] + registers[b]
    return new_registers


def addi(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] + b
    return new_registers


def mulr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] * registers[b]
    return new_registers


def muli(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] * b
    return new_registers


def banr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] & registers[b]
    return new_registers


def bani(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] & b
    return new_registers


def borr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] | registers[b]
    return new_registers


def bori(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a] | b
    return new_registers


def setr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = registers[a]
    return new_registers


def seti(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = a
    return new_registers


def gtir(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if a > registers[b] else 0
    return new_registers


def gtri(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if registers[a] > b else 0
    return new_registers


def gtrr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if registers[a] > registers[b] else 0
    return new_registers


def eqir(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if a == registers[b] else 0
    return new_registers


def eqri(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if registers[a] == b else 0
    return new_registers


def eqrr(registers: Registers, a, b, c):
    new_registers = registers[:]
    new_registers[c] = 1 if registers[a] == registers[b] else 0
    return new_registers


operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def get_cpu_operations(input_text: str) -> Tuple[List[List[int]], List[List[int]]]:
    cpu_operations = []
    before_operation = None
    operation = None
    after_operation = None

    part_2_operations = []
    for line in input_text.splitlines():
        if line.startswith('Before: '):
            m = re.search(r'Before: .*\[(.*), (.*), (.*), (.*)\]', line)
            before_operation = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
        elif line.startswith('After: '):
            m = re.search(r'After: .*\[(.*), (.*), (.*), (.*)\]', line)
            after_operation = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
            cpu_operations.append((before_operation, operation, after_operation))
            before_operation = None
        elif line:
            operation = list(map(int, line.split()))
            if not before_operation:
                part_2_operations.append(operation)

    return cpu_operations, part_2_operations


def get_operator_map(cpu_operations):
    operator_map = {}

    for x in range(16):
        operator_map[x] = operations[:]

    for before, instruction, after in cpu_operations:
        passed = 0
        instruction_index = instruction[0]
        for operation in operator_map[instruction_index][:]:
            if operation(before, *instruction[1:]) != after:
                operator_map[instruction_index].remove(operation)

    removed_operator = set()
    removed_operator_in_loop = True

    while removed_operator_in_loop:
        removed_operator_in_loop = False
        for x in range(16):
            ops = operator_map[x]
            if len(ops) == 1 and x not in removed_operator:
                removed_operator.add(x)
                removed_operator_in_loop = True
                for y in range(16):
                    if y == x:
                        continue
                    if ops[0] in operator_map[y]:
                        operator_map[y].remove(ops[0])
                continue

    return {k: v[0] for k, v in operator_map.items()}


def get_answer(input_text: str) -> int:
    cpu_operations, part_2_operations = get_cpu_operations(input_text)
    operator_map = get_operator_map(cpu_operations)
    total_passed_multi = 0
    registers = [0, 0, 0, 0]
    for cpu_operation in part_2_operations:
        instruction = cpu_operation[0]
        registers = operator_map[instruction](registers, *cpu_operation[1:])

    return registers[0]


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
