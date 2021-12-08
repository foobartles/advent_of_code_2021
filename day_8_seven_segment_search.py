from typing import List

ZERO_SEGMENTS = ['a', 'b', 'c', 'e', 'f', 'g']
ONE_SEGMENTS = ['c', 'f']
TWO_SEGMENTS = ['a', 'c', 'd', 'e', 'g']
THREE_SEGMENTS = ['a', 'c', 'd', 'f', 'g']
FOUR_SEGMENTS = ['b', 'c', 'd', 'f']
FIVE_SEGMENTS = ['a', 'b', 'd', 'f', 'g']
SIX_SEGMENTS = ['a', 'b', 'd', 'e', 'f', 'g']
SEVEN_SEGMENTS = ['a', 'c', 'f']
EIGHT_SEGMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
NINE_SEGMENTS = ['a', 'b', 'c', 'd', 'f', 'g']


class NoteEntry:
    def __init__(self, signal_patterns: List[str], output_value: List[str]):
        self.signal_patterns = signal_patterns
        self.output_value = output_value

    def __str__(self):
        result = ''
        for pattern in self.signal_patterns:
            result += pattern + ' '
        result += '| '
        for output in self.output_value:
            result += output + ' '
        return result


def calculate_num_of_easy_digits(note_entries: List[NoteEntry]) -> int:
    easy_digits_count = 0
    for note in note_entries:
        for output_number in note.output_value:
            if len(output_number) == len(ONE_SEGMENTS) or len(output_number) == len(FOUR_SEGMENTS) or \
                    len(output_number) == len(SEVEN_SEGMENTS) or len(output_number) == len(EIGHT_SEGMENTS):
                easy_digits_count += 1

    return easy_digits_count


def decipher_crossed_wires(note_entry: NoteEntry) -> int:
    # calculate sets of segments making up "easy" segments
    easy_segments = [1, 4, 7, 8]
    easy_segment_map = dict.fromkeys(easy_segments)
    for signal_pattern in note_entry.signal_patterns:
        pattern_length = len(signal_pattern)
        if pattern_length == len(ONE_SEGMENTS):
            easy_segment_map[1] = set(signal_pattern)
        elif pattern_length == len(FOUR_SEGMENTS):
            easy_segment_map[4] = set(signal_pattern)
        elif pattern_length == len(SEVEN_SEGMENTS):
            easy_segment_map[7] = set(signal_pattern)
        elif pattern_length == len(EIGHT_SEGMENTS):
            easy_segment_map[8] = set(signal_pattern)

    # loop through output values and leverage sets calculated above to deduct deciphered output number
    translated_output = ''
    for output_value in note_entry.output_value:
        output_value_set = set(output_value)
        output_value_length = len(output_value)
        # first three are easy segments
        if output_value_length == 2:
            translated_output += '1'
        elif output_value_length == 3:
            translated_output += '7'
        elif output_value_length == 4:
            translated_output += '4'
        elif output_value_length == 5:
            if len(output_value_set.intersection(easy_segment_map[1])) == 2:
                # 2 intersections with 1, must be 3
                translated_output += '3'
            elif len(output_value_set.intersection(easy_segment_map[4])) == 3:
                # 3 intersections with 4, must be 5
                translated_output += '5'
            else:
                # only 5 length output value left is 2
                translated_output += '2'
        elif output_value_length == 6:
            if len(output_value_set.intersection(easy_segment_map[4])) == 4:
                # 4 intersections with 4, must be 9
                translated_output += '9'
            elif len(output_value_set.intersection(easy_segment_map[1])) == 2:
                # 2 intersections with 1, must be 0
                translated_output += '0'
            else:
                # only 6 length output value left is 6
                translated_output += '6'
        elif output_value_length == 7:
            translated_output += '8'
    return int(translated_output)


def decipher_and_calculate_note_entries(note_entries: List[NoteEntry]) -> int:
    deciphered_entries_sum = 0
    for entry in note_entries:
        deciphered_entries_sum += decipher_crossed_wires(entry)

    return deciphered_entries_sum


def main():
    note_entries = []
    with open('puzzle_inputs/day_8.txt', 'r') as f:
        for line in f.readlines():
            entry = line.split(' | ')
            note_entries.append(NoteEntry(entry[0].strip().split(' '), entry[1].strip().split(' ')))

    print(f"part one solution: {calculate_num_of_easy_digits(note_entries)}")
    print(f"part two solution: {decipher_and_calculate_note_entries(note_entries)}")


if __name__ == '__main__':
    main()
