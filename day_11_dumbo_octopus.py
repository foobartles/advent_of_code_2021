import copy


class Octopus:
    def __init__(self, cords, energy, neighbors, has_flashed=False):
        self.cords = cords
        self.energy = energy
        self.neighbors = neighbors
        self.has_flashed = False


def parse_input(octo_inp):
    octo_cords_dict = {}
    octopuses = []
    for row in range(len(octo_inp)):
        for col in range(len(octo_inp[row])):
            cords = (row, col)
            new_octo = Octopus(cords, int(octo_inp[row][col]), [])
            octo_cords_dict[cords] = new_octo
            octopuses.append(new_octo)

    for octo in octopuses:
        neighbors = []
        row, col = octo.cords[0], octo.cords[1]
        neighbors.append(octo_cords_dict.get((row-1, col-1)))
        neighbors.append(octo_cords_dict.get((row, col-1)))
        neighbors.append(octo_cords_dict.get((row+1, col-1)))
        neighbors.append(octo_cords_dict.get((row-1, col)))
        neighbors.append(octo_cords_dict.get((row+1, col)))
        neighbors.append(octo_cords_dict.get((row-1, col+1)))
        neighbors.append(octo_cords_dict.get((row, col+1)))
        neighbors.append(octo_cords_dict.get((row+1, col+1)))
        octo.neighbors = [i for i in neighbors if i]

    return octopuses


def simulate_steps(octopuses, steps=100, synchronizing=False, debug=False):
    number_of_flashes = 0
    if debug:
        print('before any steps: ')
        print_octopuses_energy(octopuses)
    for step in range(steps):
        flashing = []
        flashed = []
        for octo in octopuses:
            octo.energy += 1
            if octo.energy > 9 and not octo.has_flashed:
                flashing.append(octo)
        while len(flashing) > 0:
            octo = flashing.pop(0)
            octo.has_flashed = True
            flashed.append(octo)
            for neighbor in octo.neighbors:
                neighbor.energy += 1
                if neighbor.energy > 9 and not neighbor.has_flashed and neighbor not in flashing:
                    flashing.append(neighbor)
        for octo in flashed:
            number_of_flashes += 1
            octo.energy = 0
            octo.has_flashed = False
        if debug:
            print('after step ' + str(step + 1) + ': ')
            print_octopuses_energy(octopuses)
        if synchronizing and len(flashed) == len(octopuses):
            return step + 1
    return number_of_flashes


def print_octopuses_energy(octopuses, row_len=10):
    line = ''
    for i in range(1, len(octopuses) + 1):
        line += str(octopuses[i-1].energy)
        if i % row_len == 0:
            line += '\n'
    print(line + '\n')


def main():
    inp = []
    with open('puzzle_inputs/day_11.txt', 'r') as f:
        for line in f.readlines():
            inp.append(line.strip())

    octopuses = parse_input(inp)

    print(f"part one solution: {simulate_steps(copy.deepcopy(octopuses), 100)}")
    print(f"part two solution: {simulate_steps(copy.deepcopy(octopuses), 9999999999, True)}")


if __name__ == '__main__':
    main()
