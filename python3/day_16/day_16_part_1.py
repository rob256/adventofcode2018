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


def get_cpu_operations(input_text: str) -> Tuple[List[int], List[int], List[int]]:
    cpu_operations = []
    before_operation = None
    operation = None
    after_operation = None
    for line in input_text.splitlines():
        if line.startswith('Before: '):
            m = re.search(r'Before: .*\[(.*), (.*), (.*), (.*)\]', line)
            before_operation = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
        elif line.startswith('After: '):
            m = re.search(r'After: .*\[(.*), (.*), (.*), (.*)\]', line)
            after_operation = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
            cpu_operations.append((before_operation, operation, after_operation))
        elif line:
            operation = list(map(int, line.split()))
    return cpu_operations



def get_answer(input_text: str) -> int:
    cpu_operations = get_cpu_operations(input_text)
    total_passed_multi = 0
    for before, instruction, after in cpu_operations:
        passed = 0
        for operation in operations:
            if operation(before, *instruction[1:]) == after:
                passed += 1
        if passed >= 3:
            total_passed_multi += 1
    return total_passed_multi


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
