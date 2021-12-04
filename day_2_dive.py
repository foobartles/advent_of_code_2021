from enum import Enum
from typing import List


class Direction(Enum):
    forward = 0
    down = 1
    up = 2


class Command:
    def __init__(self, direction, units):
        self.direction = direction
        self.units = units


class Position:
    def __init__(self, depth, horizontal, aim=0):
        self.depth = depth
        self.horizontal = horizontal
        self.aim = aim


def calculate_horizontal_depth_position(course_data: List[Command]) -> Position:
    depth = 0
    horizontal = 0

    for command in course_data:
        if command.direction == Direction.forward.name:
            horizontal += command.units
        elif command.direction == Direction.down.name:
            depth += command.units
        elif command.direction == Direction.up.name:
            depth -= command.units

    return Position(depth, horizontal)


def calculate_horizontal_depth_with_aim_position(course_data: List[Command]) -> Position:
    depth = 0
    horizontal = 0
    aim = 0

    for command in course_data:
        if command.direction == Direction.forward.name:
            horizontal += command.units
            depth += aim * command.units
        elif command.direction == Direction.down.name:
            aim += command.units
        elif command.direction == Direction.up.name:
            aim -= command.units

    return Position(depth, horizontal, aim)


if __name__ == '__main__':
    submarine_commands = []
    with open('puzzle_inputs/day_2.txt', 'r') as f:
        for line in f:
            split_line = line.split()
            submarine_commands.append(Command(split_line[0], int(split_line[1])))

    part_one_solution = calculate_horizontal_depth_position(submarine_commands)
    print(f"part one solution: {part_one_solution.horizontal * part_one_solution.depth}")
    part_two_solution = calculate_horizontal_depth_with_aim_position(submarine_commands)
    print(f"part two solution: {part_two_solution.horizontal * part_two_solution.depth}")
