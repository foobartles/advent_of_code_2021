from typing import List
import copy


class BingoNumber:
    number = -1
    is_marked = False

    def __str__(self):
        number_string = str(self.number)
        if self.is_marked:
            number_string = '(' + number_string + ')'
        while len(number_string) < 5:
            number_string = " " + number_string

        return number_string


class BingoBoard:
    def __init__(self, board_data: List[List[int]]):
        self.numbers_dict = {}
        self.is_winning = False
        self.board = [[BingoNumber() for i in range(5)] for j in range(5)]
        self.parse_board_data(board_data)

    def parse_board_data(self, board_data):
        for i in range(5):
            for j in range(5):
                number = board_data[i][j]
                self.board[i][j].number = number
                if number in self.numbers_dict:
                    self.numbers_dict[number].append(self.board[i][j])
                else:
                    self.numbers_dict[number] = [self.board[i][j]]

    def mark_number(self, number):
        if number in self.numbers_dict:
            for bingo_number in self.numbers_dict[number]:
                bingo_number.is_marked = True

    def check_for_win(self) -> bool:
        row_counter = 0
        column_counter = 0
        for i in range(5):
            for j in range(5):
                if self.board[i][j].is_marked:
                    row_counter += 1
                if self.board[j][i].is_marked:
                    column_counter += 1
                if row_counter == 5 or column_counter == 5:
                    self.is_winning = True
                    return True
            row_counter = 0
            column_counter = 0

        self.is_winning = False
        return False

    def calculate_score(self, last_called_number=1) -> int:
        score_sum = 0
        for i in range(5):
            for j in range(5):
                if not self.board[i][j].is_marked:
                    score_sum += self.board[i][j].number
        return score_sum * last_called_number

    def __str__(self):
        board_string = ""
        for i in range(5):
            for j in range(5):
                board_string += str(self.board[i][j]) + ' '
            board_string += '\n'
        return board_string


class BingoSubsystem:
    def __init__(self, numbers_to_draw, boards):
        self.numbers_to_draw = numbers_to_draw
        self.bingo_boards = boards

    def calculate_board_score(self, find_losing_board=False) -> int:
        boards = copy.deepcopy(self.bingo_boards)
        winning_boards_count = 0
        for i in range(len(self.numbers_to_draw)):
            for board in boards:
                if not board.is_winning:
                    board.mark_number(self.numbers_to_draw[i])
                    if i >= 4:
                        # enough numbers have been drawn to win now, start checking for winning boards
                        if board.check_for_win():
                            if find_losing_board:
                                winning_boards_count += 1
                                if len(boards) == winning_boards_count:
                                    return board.calculate_score(self.numbers_to_draw[i])
                            else:
                                return board.calculate_score(self.numbers_to_draw[i])
        return -1

    def __str__(self):
        boards_string = ''
        for board in self.bingo_boards:
            boards_string += str(board)
            boards_string += '-'*50 + '\n'
        return boards_string


if __name__ == '__main__':
    drawn_numbers = []
    bingo_boards = []
    with open('puzzle_inputs/day_4.txt', 'r') as f:
        lines = f.readlines()
        bingo_board = []
        for i in range(len(lines)):
            if i == 0:
                drawn_numbers = [int(x) for x in lines[i].strip().split(',')]
                continue
            if lines[i].strip() == "":
                if len(bingo_board) > 0:
                    parsed_board = BingoBoard(bingo_board)
                    bingo_boards.append(parsed_board)
                bingo_board = []
            else:
                bingo_board.append([int(x) for x in lines[i].strip().split()])
        last_board = BingoBoard(bingo_board)
        bingo_boards.append(last_board)

    bingo_subsystem = BingoSubsystem(drawn_numbers, bingo_boards)
    print(f"part one solution: {bingo_subsystem.calculate_board_score()}")
    print(f"part two solution: {bingo_subsystem.calculate_board_score(True)}")
