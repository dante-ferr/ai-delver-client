from utils.rotate_matrix import rotate_matrix
import numpy as np


class AutotileRule:
    display: tuple[int, int]

    def __init__(
        self,
        rule_matrix: list[list[int]],
        display: tuple[int, int],
    ):
        self.rule_matrix = np.array(rule_matrix)
        self.display = display


def get_rule_group(
    rule_matrix: list[list[int]], display: tuple[int, int], amount: int = 4
):
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    if amount > 4:
        raise ValueError("Amount must be less than or equal to 4")

    x, y = display
    if amount == 2:
        angles = [0, 90]
        displays = [(x, y), (x, y + 1)]
    else:
        angles = [0, 90, 180, 270][:amount]
        displays = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)][:amount]

    rule_matrixes = [rotate_matrix(rule_matrix, angle) for angle in angles]

    return [AutotileRule(rm, d) for rm, d in zip(rule_matrixes, displays)]
