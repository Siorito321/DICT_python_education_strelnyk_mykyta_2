import re


class RegExp:
    """ Class for matching a regular expression pattern against an expression."""

    def __init__(self, answer) -> None:
        self.regexp = answer.split("|")[0]
        self.exp = answer.split("|")[1]

    def if_parser(self) -> bool:
        """
        Check if the expression matches the pattern.

        Returns:
        bool: True if there is a match, False otherwise.
        """
        return re.match(self.regexp, self.exp) is not None


while True:
    try:
        reg = RegExp(input("Input your value>"))
        print(reg.if_parser())
    except IndexError:
        print("Please, input correct values!")
        continue
