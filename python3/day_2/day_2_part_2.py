def words_differ_by_one(word1: str, word2: str) -> [str, None]:
    differences = 0
    last_difference = 0
    for i in range(len(word1)):
        c1 = word1[i]
        c2 = word2[i]
        if c1 != c2:
            differences += 1
            last_difference = i
            if differences > 1:
                return
    if differences == 1:
        return word1[:last_difference] + word1[last_difference + 1:]


def get_common_phrase(input_text: str) -> str:
    words_list = input_text.splitlines()
    for word1 in words_list:
        for word2 in words_list:
            word_diff = words_differ_by_one(word1, word2)
            if word_diff:
                return word_diff


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_common_phrase(input_text))


if __name__ == '__main__':
    main()