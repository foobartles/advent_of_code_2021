SYNTAX_ERROR_SCORE_TABLE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTO_COMPLETION_SCORE_TABLE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def parse_bad_chunk(chunk: str):
    # if chunk is illegal, return illegal char
    # if chunk is incomplete, return array of incomplete opening brackets
    chunk_start_stack = []
    for char in chunk:
        if char == ')':
            if chunk_start_stack[-1] == '(':
                chunk_start_stack.pop(-1)
            else:
                return char
        elif char == ']':
            if chunk_start_stack[-1] == '[':
                chunk_start_stack.pop(-1)
            else:
                return char
        elif char == '}':
            if chunk_start_stack[-1] == '{':
                chunk_start_stack.pop(-1)
            else:
                return char
        elif char == '>':
            if chunk_start_stack[-1] == '<':
                chunk_start_stack.pop(-1)
            else:
                return char
        else:
            chunk_start_stack.append(char)
    return chunk_start_stack


def correct_incomplete_line(incomplete_chunk):
    completing_chars = []
    for i in range(len(incomplete_chunk)-1, -1, -1):
        if incomplete_chunk[i] == '(':
            completing_chars.append(')')
        elif incomplete_chunk[i] == '[':
            completing_chars.append(']')
        elif incomplete_chunk[i] == '{':
            completing_chars.append('}')
        elif incomplete_chunk[i] == '<':
            completing_chars.append('>')
    return completing_chars


def calculate_chunk_scores(chunks):
    syntax_error_score = 0
    incomplete_scores = []
    for chunk in chunks:
        bad_chunk = parse_bad_chunk(chunk)
        if len(bad_chunk) == 1:
            # calculate score of illegal chunk
            syntax_error_score += SYNTAX_ERROR_SCORE_TABLE[bad_chunk]
        elif len(bad_chunk) > 1:
            chunk_score = 0
            for completing_char in correct_incomplete_line(bad_chunk):
                chunk_score *= 5
                chunk_score += AUTO_COMPLETION_SCORE_TABLE[completing_char]
            incomplete_scores.append(chunk_score)

    return syntax_error_score, find_middle_score(incomplete_scores)


def find_middle_score(scores) -> int:
    sorted_scores = scores.copy()
    sorted_scores.sort()
    return sorted_scores[(len(sorted_scores) // 2)]


def main():
    inp = []
    with open('puzzle_inputs/day_10.txt', 'r') as f:
        for line in f.readlines():
            inp.append(line.strip())

    scores = calculate_chunk_scores(inp)
    print(f"part one solution: {scores[0]}")
    print(f"part two solution: {scores[1]}")


if __name__ == '__main__':
    main()