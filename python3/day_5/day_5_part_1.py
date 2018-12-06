def chars_react(char_1, char_2):
    ord_1 = ord(char_1)
    ord_2 = ord(char_2)
    if ord_1 > ord_2:
        return chars_react(char_2, char_1)
    if ord_1 == ord_2:
        return False
    return ord_2 - ord_1 == 32


def get_answer(input_text: str) -> int:
    total_string = input_text
    x = 0
    while True:
        char_1, char_2 = total_string[x], total_string[x + 1]
        if chars_react(char_1, char_2):
            total_string = total_string[:x] + total_string[x + 2:]
            x = max(0, x - 1)
        else:
            x += 1
        if x >= len(total_string) - 1:
            break
    return len(total_string)


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))

# def main():
#     print(get_answer('dabAcCaCBAcCcaDA'))


if __name__ == '__main__':
    main()
