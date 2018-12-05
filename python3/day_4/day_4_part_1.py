from collections import defaultdict
from operator import itemgetter

def get_answer(input_text: str) -> int:
    sorted_input = sorted(input_text.splitlines())
    current_guard_id = 0
    guard_asleep_total = defaultdict(int)
    guard_minute_sleep = {}
    sleeping_minute = 0
    for log in sorted_input:
        parts = log.split()
        minute = int(parts[1][3:-1])
        if parts[2] == 'Guard':
            current_guard_id = int(parts[3][1:])
        elif parts[2] == 'falls':
            sleeping_minute = minute
        elif parts[2] == 'wakes':
            sleeping_time = minute - sleeping_minute
            guard_asleep_total[current_guard_id] += sleeping_time
            if current_guard_id not in guard_minute_sleep:
                guard_minute_sleep[current_guard_id] = defaultdict(int)
            for x in range(sleeping_time):
                guard_minute_sleep[current_guard_id][sleeping_minute + x] += 1
    print(guard_asleep_total)
    print(guard_minute_sleep)

    sorted_guard_asleep_total = sorted(guard_asleep_total.items(), key=itemgetter(1), reverse=True)
    most_sleepy_guard = sorted_guard_asleep_total[0][0]
    sorted_guard_minute_sleep = sorted(guard_minute_sleep[most_sleepy_guard].items(), key=itemgetter(1), reverse=True)
    max_minute = sorted_guard_minute_sleep[0][0]
    return most_sleepy_guard * max_minute


def main():
    with open('input.txt') as input_file:
        input_text = input_file.read().rstrip('\n')
    print(get_answer(input_text))


if __name__ == '__main__':
    main()
