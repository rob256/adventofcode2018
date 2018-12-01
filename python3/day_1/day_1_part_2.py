from itertools import cycle


def get_resulting_frequency_duplicate(input_text: str) -> int:
    int_list = [int(x) for x in input_text.splitlines()]
    sum_seen = {0}
    current_sum = 0
    for number in cycle(int_list):
        current_sum += number
        if current_sum in sum_seen:
            return current_sum
        sum_seen.add(current_sum)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_resulting_frequency_duplicate(input_text))


if __name__ == '__main__':
    main()