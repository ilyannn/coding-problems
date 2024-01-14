# * Feel free to import and use anything from the standard library!
# * You can look at the test cases in the main_test.py file.
# * Feel free to copy the test cases into your IDE of choice
#   and copy your code back here. Just make sure it runs.
import re
from math import nan, isnan
from statistics import mean
from typing import Optional


# Raise this error for any invalid input, preferably with a clear error message
class ParseError(Exception):
    pass


class Reader:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def is_end(self):
        return self.pos == len(self.text)

    def read(self, expect: Optional[set | str] = None):
        if value := self.peek():
            self.pos += 1
        if expect is not None:
            if value not in expect:
                raise ValueError("Unexpected value", value)
        return value

    def peek(self, count=1):
        return self.text[self.pos : self.pos + count]

    def __str__(self):
        return str(self.text[: self.pos]) + f"[{self.peek()}]"


KEY_VALUE_EXPRESSION = re.compile(r"([A-Za-z0-9]+)=(.*)")


def parse_atom(reader):
    if reader.peek(3) == "NaN":
        for _ in range(3):
            reader.read()
        return nan
    number = None
    exponent = None
    sign = None
    while reader.peek() not in ";]":
        match reader.read():
            case "+":
                if sign is not None:
                    raise ValueError("Invalid sign combination", sign, "+")
                sign = 1
            case "-":
                if sign is not None:
                    raise ValueError("Invalid sign combination", sign, "-")
                sign = -1
            case ".":
                if exponent is not None:
                    raise ValueError("Can't have two decimal dots")
                exponent = 0
            case digit if digit.isdigit():
                number = 10 * (number or 0) + int(digit)
                if exponent is not None:
                    exponent += 1
            case anything:
                raise ValueError("Unexpected token", anything)

    if reader.peek() == ";":
        _ = reader.read(";")

    return (sign or +1) * number / 10 ** (exponent or 0)


assert parse_atom(Reader("12")) == 12
assert parse_atom(Reader("5.7")) == 5.7
assert parse_atom(Reader("-4.5555")) == -4.5555
assert isnan(parse_atom(Reader("NaN")))


def parse_nested_list(reader: Reader):
    def gen():
        _ = reader.read("[")
        while True:
            match reader.peek():
                case "]":
                    break
                case "[":
                    yield parse_nested_list(reader)
                case _:
                    yield parse_atom(reader)
        _ = reader.read("]")

    return list(gen())


assert parse_nested_list(Reader("[1.0;2.0;3.0;4.0]")) == [1, 2, 3, 4]
assert parse_nested_list(Reader("[]")) == []


def parse_key_value_pair(pair):
    match = KEY_VALUE_EXPRESSION.fullmatch(pair)
    if not match:
        raise ParseError("Invalid key-value pair", pair)
    reader = Reader(match.group(2))
    try:
        return match.group(1), parse_nested_list(reader)
    except ValueError:
        raise ParseError(
            "Error when parsing",
            reader,
        )

assert parse_key_value_pair("arg=[0.05]") == ("arg", [0.05])
assert parse_key_value_pair("arg36=[1;NaN]") == ("arg36", [1, nan])

def compute_average_expression(e):
    match e:
        case []:
            return 0
        case list(l):
            return mean(compute_average_expression(part) for part in l)
        case value:
            return value


def parse_arguments(string):
    return [parse_key_value_pair(pair) for pair in string.split()]


def dump_arguments(arguments, accuracy: int) -> str:
    return " ".join(f"{arg}={value:0.{accuracy}}" for arg, value in arguments)


# This function shouldn't be renamed so it can be imported in the tests
def parse_compute_averages(input_arguments: str) -> str:
    arguments = parse_arguments(input_arguments)
    return dump_arguments(
        ((arg, compute_average_expression(e)) for arg, e in arguments), accuracy=2
    )
