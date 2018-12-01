def get_resulting_frequency(input_text: str) -> int:
    int_list = [int(x) for x in input_text.splitlines()]
    return sum(int_list)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_resulting_frequency(input_text))


if __name__ == '__main__':
    main()