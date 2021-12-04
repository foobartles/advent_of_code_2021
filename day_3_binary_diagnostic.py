from typing import List
from math import floor


class BinaryDiagnostic:
    def __init__(self, diagnostic_report: List[str]):
        self.diagnostic_report = diagnostic_report
        self._report_length = len(diagnostic_report)
        self._binary_length = len(diagnostic_report[0])
        self.zero_bit_list = [set() for _ in range(self._binary_length)]
        self.one_bit_list = [set() for _ in range(self._binary_length)]

        self._initial_analysis()

    def _initial_analysis(self):
        for report in self.diagnostic_report:
            for i in range(self._binary_length):
                if report[i] == '0':
                    self.zero_bit_list[i].add(report)
                elif report[i] == '1':
                    self.one_bit_list[i].add(report)

    def calculate_gamma(self) -> str:
        gamma = ''
        for binaries in self.zero_bit_list:
            if len(binaries) > floor(self._report_length / 2):
                gamma += '0'
            else:
                gamma += '1'

        return gamma

    def calculate_epsilon(self) -> str:
        epsilon = ''
        for binaries in self.zero_bit_list:
            if len(binaries) < floor(self._report_length / 2):
                epsilon += '0'
            else:
                epsilon += '1'

        return epsilon

    def calculate_power_consumption(self) -> int:
        gamma_int = int(self.calculate_gamma(), 2)
        epsilon_int = int(self.calculate_epsilon(), 2)

        return gamma_int * epsilon_int

    def calculate_oxygen_generator_rating(self) -> str:
        rating = set(self.diagnostic_report)
        if len(self.zero_bit_list[0]) > len(self.one_bit_list[0]):
            # more 0 bits
            rating = rating.intersection(self.zero_bit_list[0])
        else:
            # more or equal 1 bits
            rating = rating.intersection(self.one_bit_list[0])

        for i in range(1, self._binary_length):
            if len(rating) == 1:
                break
            if len(self.zero_bit_list[i].intersection(rating)) > len(self.one_bit_list[i].intersection(rating)):
                # more 0 bits
                rating = rating.intersection(self.zero_bit_list[i])
            else:
                # more or equal 1 bits
                rating = rating.intersection(self.one_bit_list[i])

        return rating.pop()

    def calculate_co2_scrubber_rating(self) -> str:
        rating = set(self.diagnostic_report)
        if len(self.one_bit_list[0]) < len(self.zero_bit_list[0]):
            # less 1 bits
            rating = rating.intersection(self.one_bit_list[0])
        else:
            # less or equal 0 bits
            rating = rating.intersection(self.zero_bit_list[0])

        for i in range(1, self._binary_length):
            if len(rating) == 1:
                break
            if len(self.one_bit_list[i].intersection(rating)) < len(self.zero_bit_list[i].intersection(rating)):
                # less 1 bits
                rating = rating.intersection(self.one_bit_list[i])
            else:
                # less or equal 0 bits
                rating = rating.intersection(self.zero_bit_list[i])

        return rating.pop()

    def calculate_life_support_rating(self) -> int:
        oxygen_rating_int = int(self.calculate_oxygen_generator_rating(), 2)
        co2_rating_int = int(self.calculate_co2_scrubber_rating(), 2)

        return oxygen_rating_int * co2_rating_int


if __name__ == '__main__':
    diagnostics = []
    with open('puzzle_inputs/day_3.txt', 'r') as f:
        for line in f:
            diagnostics.append(line.strip())

    binary_diagnostic = BinaryDiagnostic(diagnostics)
    part_one_solution = binary_diagnostic.calculate_power_consumption()
    print(f"part one solution: {part_one_solution}")

    part_two_solution =binary_diagnostic.calculate_life_support_rating()
    print(f"part two solution: {part_two_solution}")
