from lib import Matrix
from typing import Callable
import sys


"""
아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    # lines: list[str] = sys.stdin.readlines()
    lines: list[str] = [
    "3 3",
    "1 2 3",
    "4 5 6",
    "7 8 9"
]

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)

    print(modmat ** B)


if __name__ == "__main__":
    main()