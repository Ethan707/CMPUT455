import collections
from board_util import BLACK, WHITE, EMPTY

SCORE_MAP = [0, 1, 10, 100, 1000, 1000000]


def calc_score(counts, color):
    if color == BLACK:
        my_count, opp_count, open_count = counts
    else:
        opp_count, my_count, open_count = counts

    # Is blocked
    if my_count >= 1 and opp_count >= 1:
        return 0

    return SCORE_MAP[my_count] - SCORE_MAP[opp_count]


def get_counts(board, five_line):
    b_count = 0
    w_count = 0
    e_count = 0

    for p in five_line:
        stone = board.board[p]
        if stone == BLACK:
            b_count += 1
        elif stone == WHITE:
            w_count += 1
        else:
            e_count += 1

    return b_count, w_count, e_count


def evaluate(board, color):

    score = 0
    total = board.rows + board.cols + board.diags

    for line in total:
        for i in range(len(line) - 5):
            counts = get_counts(board, line[i:i + 5])
            score += calc_score(counts, color)

    return score
