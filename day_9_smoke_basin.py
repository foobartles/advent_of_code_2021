import math


class HeatMap:
    def __init__(self, heat_map):
        self.heat_map = heat_map

    def find_low_points(self):
        low_points_dict = {}
        for i in range(len(self.heat_map)):
            for j in range(len(self.heat_map[i])):
                curr = self.heat_map[i][j]
                is_low_point = True
                if i > 0 and self.heat_map[i - 1][j] <= curr:
                    # check position above
                    is_low_point = False
                if i < (len(self.heat_map) - 1) and self.heat_map[i + 1][j] <= curr:
                    # check position below
                    is_low_point = False
                if j > 0 and self.heat_map[i][j - 1] <= curr:
                    # check position left
                    is_low_point = False
                if j < len(self.heat_map[i]) - 1 and self.heat_map[i][j + 1] <= curr:
                    # check position right
                    is_low_point = False
                if is_low_point:
                    low_points_dict[(i, j)] = curr
        return low_points_dict

    def calculate_low_points_risk_level(self):
        low_points = self.find_low_points().values()
        calculation = 0
        for point in low_points:
            calculation += 1 + point
        return calculation

    def find_touching_points_in_basin(self, point):
        points_touching_in_basin = []
        if point[0] > 0 and self.heat_map[point[0] - 1][point[1]] < 9:
            # check position above
            points_touching_in_basin.append((point[0] - 1, point[1]))
        if point[0] < len(self.heat_map) - 1 and self.heat_map[point[0] + 1][point[1]] < 9:
            # check position below
            points_touching_in_basin.append((point[0]+1, point[1]))
        if point[1] > 0 and self.heat_map[point[0]][point[1] - 1] < 9:
            # check position left
            points_touching_in_basin.append((point[0], point[1]-1))
        if point[1] < len(self.heat_map[point[0]]) - 1 and self.heat_map[point[0]][point[1] + 1] < 9:
            # check position right
            points_touching_in_basin.append((point[0], point[1] + 1))
        return points_touching_in_basin

    def find_basin_sizes(self, number_to_find=3):
        low_points_dict = self.find_low_points()
        basin_sizes = []
        for low_point in low_points_dict:
            points_in_basin = set()
            points_in_basin.add(low_point)
            new_points = set()
            while True:
                for point in points_in_basin:
                    touching_points = set(self.find_touching_points_in_basin(point)).difference(points_in_basin)
                    for touching in touching_points:
                        new_points.add(touching)
                for new in new_points:
                    points_in_basin.add(new)
                if len(new_points) == 0:
                    break
                else:
                    new_points = set()
            basin_sizes.append((len(points_in_basin)))

        return basin_sizes

    def calculate_largest_basin_sizes_product(self, number_to_find=3):
        basin_sizes = self.find_basin_sizes()
        basin_sizes.sort()
        return math.prod(basin_sizes[-number_to_find:])


def main():
    inp = []
    with open('puzzle_inputs/day_9.txt', 'r') as f:
        for line in f.readlines():
            inp.append([int(x) for x in line.strip()])

    heat_map = HeatMap(inp)

    print(f"part one solution: {heat_map.calculate_low_points_risk_level()}")
    print(f"part two solution: {heat_map.calculate_largest_basin_sizes_product()}")


if __name__ == '__main__':
    main()
