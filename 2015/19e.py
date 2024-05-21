#! ./bin/python3

from lark import Lark

grammar = """
    start: H | O
    H: H O | O H | "H"
    O: H H | "O"
"""

parser = Lark(grammar)
print(parser.parse("HOHOHO"))
