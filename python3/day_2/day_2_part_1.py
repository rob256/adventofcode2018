from collections import Counter


def get_checksum(input_text: str) -> int:
    twos = 0
    threes = 0

    for line in input_text.splitlines():
        word_counter = Counter(list(line))
        for k, v in word_counter.items():
            if v == 2:
                twos += 1
                break
        for k, v in word_counter.items():
            if v == 3:
                threes += 1
                break

    return twos * threes


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_checksum(input_text))


if __name__ == '__main__':
    main()