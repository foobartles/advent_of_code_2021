from typing import List

def count_depth_increases(data: List[int]) -> int:
    num_increased = 0

    for i in range(0, len(data)):
        if i == 0:
            continue
        if data[i] > data[i-1]:
            num_increased += 1

    return num_increased

def count_depth_sum_increases(data: List[int]) -> int:
    num_increased = 0

    for i in range(0, len(data)):
        if i + 3 > len(data):
            break

        first_three = sum(data[i:i+3])
        next_three = sum(data[i+1:i+4])

        if first_three < next_three:
            num_increased += 1

    return num_increased

if __name__ == '__main__':
    submarine_data = []
    with open('puzzle_inputs/day_one.txt', 'r') as f:
        for line in f:
            submarine_data.append(int(line))

    print(f"part one solution: {count_depth_increases(submarine_data)}")
    print(f"part two solution: {count_depth_sum_increases(submarine_data)}")