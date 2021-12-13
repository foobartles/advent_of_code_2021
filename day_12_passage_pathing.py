

class Cave:
    def __init__(self, name: str, connecting_caves=None):
        if connecting_caves is None:
            connecting_caves = []
        self.name = name
        self.is_big = name.isupper()
        self.connecting_caves = connecting_caves

    def __str__(self):
        return self.name


class CaveSystem:
    def __init__(self, caves, starting_cave):
        self.caves = caves
        self.starting_cave = starting_cave
        self.distinct_paths = []

    def calculate_number_of_distinct_paths(self, visit_small_twice=False):
        self.distinct_paths = []
        self.distinct_paths_search(self.starting_cave, [], visit_small_twice)
        return len(self.distinct_paths)

    def distinct_paths_search(self, curr, path, can_visit_small_twice=False, has_visited_small_twice=False):
        path = path + [curr]
        if curr.name == 'end':
            self.distinct_paths.append(path)
        for cave in curr.connecting_caves:
            if cave.is_big:
                # can revisit any big cave
                self.distinct_paths_search(cave, path, can_visit_small_twice, has_visited_small_twice)
            elif cave not in path:
                # cave not yet visited on this path
                self.distinct_paths_search(cave, path, can_visit_small_twice, has_visited_small_twice)
            elif can_visit_small_twice and path.count(cave) < 2 and not has_visited_small_twice \
                    and cave.name != 'start' and cave.name != 'end':
                # revisit small cave once if we haven't visited a small cave twice on this path yet, excluding start/end
                self.distinct_paths_search(cave, path, can_visit_small_twice, True)

    def print_distinct_paths(self):
        for path in self.distinct_paths:
            path_str = ''
            for cave in path:
                path_str += str(cave) + ','
            print(path_str[:-1])


def parse_input_for_caves(inp):
    caves = []
    cave_name_dict = {}
    for line in inp:
        split = line.strip().split('-')
        left_cave_name = split[0]
        if left_cave_name in cave_name_dict:
            left_cave = cave_name_dict[left_cave_name]
        else:
            left_cave = Cave(left_cave_name)
            cave_name_dict[left_cave_name] = left_cave
            caves.append(left_cave)
        right_cave_name = split[1]
        if right_cave_name in cave_name_dict:
            right_cave = cave_name_dict[right_cave_name]
        else:
            right_cave = Cave(right_cave_name, [left_cave])
            cave_name_dict[right_cave_name] = right_cave
            caves.append(right_cave)

        if right_cave not in left_cave.connecting_caves:
            left_cave.connecting_caves.append(right_cave)
        if left_cave not in right_cave.connecting_caves:
            right_cave.connecting_caves.append(left_cave)

    return caves, cave_name_dict['start']


def main():
    inp = []
    with open('puzzle_inputs/day_12.txt', 'r') as f:
        for line in f.readlines():
            inp.append(line.strip())

    caves, starting_cave = parse_input_for_caves(inp)
    cave_system = CaveSystem(caves, starting_cave)

    print(f"part one solution: {cave_system.calculate_number_of_distinct_paths()}")
    print(f"part two solution: {cave_system.calculate_number_of_distinct_paths(True)}")


if __name__ == '__main__':
    main()
