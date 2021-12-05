from typing import List


class Vent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x + self.y) < (other.x + other.y)

    def __str__(self):
        return str(self.x) + ',' + str(self.y)


class VentLine:
    def __init__(self, vent1: Vent, vent2: Vent):
        self.vent1 = vent1
        self.vent2 = vent2

    def bigger_x_vent(self) -> Vent:
        if self.vent2.x > self.vent1.x:
            return self.vent2
        else:
            return self.vent1

    def bigger_y_vent(self) -> Vent:
        if self.vent2.y > self.vent1.y:
            return self.vent2
        else:
            return self.vent1

    def __str__(self):
        return str(self.vent1) + ' -> ' + str(self.vent2)


class OceanFloorVentMap:
    def __init__(self, vent_lines: List[VentLine]):
        self.vent_lines = vent_lines
        # 2d array of vents, diagram[row][column] or diagram[y][x]
        self.diagram = []
        self.danger_points_count = 0
        self.max_x = 0
        self.max_y = 0

    def calculate_danger_points(self, include_diagonals=False) -> int:
        self.diagram = []
        self.danger_points_count = 0
        for vent_line in self.vent_lines:
            # look for biggest x and y coords for printing purposes
            big_x_vent, big_y_vent = vent_line.bigger_x_vent(), vent_line.bigger_y_vent()
            if big_x_vent.x > self.max_x:
                self.max_x = big_x_vent.x
            if big_y_vent.y > self.max_y:
                self.max_y = big_y_vent.y
    
            # add empty rows until there are enough rows for new vent line
            while big_y_vent.y >= len(self.diagram):
                self.diagram.append([])

            vent1, vent2 = vent_line.vent1, vent_line.vent2
            if vent1.x == vent2.x:
                # straight line exists between two vents along y coordinate
                # top to bottom
                small_y = min(vent1.y, vent2.y)
                x = vent1.x
                for y in range(small_y, big_y_vent.y + 1):
                    # add 0s until there are enough columns for new vent line
                    while x >= len(self.diagram[y]):
                        self.diagram[y].append(0)
                    self.increment_vent_count(x, y)
            elif vent_line.vent1.y == vent_line.vent2.y:
                # straight line exists between two vents along x coordinate
                # left to right
                small_x = min(vent_line.vent1.x, vent_line.vent2.x)
                y = vent1.y
                # add 0s until there are enough columns for new vent line
                while big_x_vent.x >= len(self.diagram[y]):
                    self.diagram[y].append(0)
                for x in range(small_x, big_x_vent.x+1):
                    self.increment_vent_count(x, y)
            else:
                # diagonal line
                if include_diagonals:
                    x, y = vent1.x, vent1.y
                    if vent1.x < vent2.x and vent1.y < vent2.y:
                        # top left to bottom right
                        # while vent2.y >= len(self.diagram):
                        while x <= vent2.x and y <= vent2.y:
                            # add 0s until there are enough columns for new vent line
                            while vent2.x >= len(self.diagram[y]):
                                self.diagram[y].append(0)
                            self.increment_vent_count(x, y)
                            x += 1
                            y += 1
                    elif vent1.x < vent2.x and vent1.y > vent2.y:
                        # bottom left to top right
                        while x <= vent2.x and y >= vent2.y:
                            # add 0s until there are enough columns for new vent line
                            while vent2.x >= len(self.diagram[y]):
                                self.diagram[y].append(0)
                            self.increment_vent_count(x, y)
                            x += 1
                            y -= 1
                    elif vent1.x > vent2.x and vent1.y < vent2.y:
                        # top right to bottom left
                        while x >= vent2.x and y <= vent2.y:
                            # add 0s until there are enough columns for new vent line
                            while vent1.x >= len(self.diagram[y]):
                                self.diagram[y].append(0)
                            self.increment_vent_count(x, y)
                            x -= 1
                            y += 1
                    elif vent1.x > vent2.x and vent1.y > vent2.y:
                        # bottom right to top left
                        while x >= vent2.x and y >= vent2.y:
                            # add 0s until there are enough columns for new vent line
                            while vent1.x >= len(self.diagram[y]):
                                self.diagram[y].append(0)
                            self.increment_vent_count(x, y)
                            x -= 1
                            y -= 1
        return self.danger_points_count

    def increment_vent_count(self, x, y):
        self.diagram[y][x] += 1
        if self.diagram[y][x] == 2:
            self.danger_points_count += 1

    def __str__(self):
        diagram_string = ''
        while self.max_y >= len(self.diagram):
            self.diagram.append([])
        for row in self.diagram:
            while self.max_x >= len(row):
                row.append(0)
            for vent_counter in row:
                if vent_counter == 0:
                    diagram_string += '.'
                else:
                    diagram_string += str(vent_counter)
            diagram_string += '\n'
        return diagram_string


if __name__ == '__main__':
    lines = []
    with open('puzzle_inputs/day_5.txt', 'r') as f:
        for line in f:
            split_line = line.split(' -> ')
            left_coord = split_line[0].split(',')
            right_coord = split_line[1].split(',')
            parsed_vent_line = VentLine(Vent(int(left_coord[0]), int(left_coord[1])),
                                 Vent(int(right_coord[0]), int(right_coord[1])))
            lines.append(parsed_vent_line)

    vent_map = OceanFloorVentMap(lines)

    print(f"part one solution: {vent_map.calculate_danger_points()}")
    print(f"part two solution: {vent_map.calculate_danger_points(True)}")

