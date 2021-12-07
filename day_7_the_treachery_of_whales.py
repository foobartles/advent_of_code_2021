def calculate_fuel_cost(p1: int, p2: int, constant_fuel_rate=True) -> int:
    diff = abs(p1 - p2)
    if constant_fuel_rate:
        return diff
    else:
        # infinite series sum formula
        return diff * (diff + 1) // 2


def calculate_cheapest_alignment_cost(crab_sub_positions, constant_fuel_rate=True) -> int:
    return min(
        sum(
            calculate_fuel_cost(new_position, current_position, constant_fuel_rate)
            for current_position in crab_sub_positions
        )
        for new_position in range(max(crab_sub_positions))
    )


def main():
    with open('puzzle_inputs/day_7.txt', 'r') as f:
        crab_sub_positions = [int(x) for x in f.readline().split(',')]

    print(f"part one solution: {calculate_cheapest_alignment_cost(crab_sub_positions)}")
    print(f"part two solution: {calculate_cheapest_alignment_cost(crab_sub_positions, False)}")


if __name__ == '__main__':
    main()
