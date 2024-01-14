import re
import unittest
from math import isnan, nan
from statistics import mean
from typing import Optional


class ParseError(Exception):
    pass


class Reader:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def is_end(self):
        return self.pos == len(self.text)

    def peek(self, count: int = 1):
        return self.text[self.pos : self.pos + count]

    def read(self, expect: Optional[str] = None, count=None):
        count = count or len(expect or " ")
        value = self.peek(count)
        if expect is not None and value != expect:
            raise ValueError("Unexpected value", value)
        self.pos += len(value)
        return value

    def __str__(self):
        return str(self.text[: self.pos]) + f"<{self.peek()}>"


KEY_VALUE_EXPRESSION = re.compile(r"([A-Za-z0-9]+)=(.*)")


def parse_atom(reader):
    if reader.peek(3) == "NaN":
        reader.read("NaN", count=3)
        return nan

    number = None
    exponent = None
    sign = None

    while reader.peek() not in ";]":
        match reader.read():
            case "+":
                if number is not None or exponent is not None:
                    raise ValueError("Invalid sign position", "+")
                if sign is not None:
                    raise ValueError("Invalid sign combination", sign, "+")
                sign = 1
            case "-":
                if number is not None or exponent is not None:
                    raise ValueError("Invalid sign position", "+")
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

    if number is None:
        raise ValueError("Number should contain at least one digit")

    return (sign or +1) * number / 10 ** (exponent or 0)


def parse_nested_list(reader: Reader):
    def gen():
        _ = reader.read("[")
        if reader.peek() == "]":
            _ = reader.read("]")
        else:
            while True:
                yield (parse_nested_list if reader.peek() == "[" else parse_atom)(
                    reader
                )
                match reader.read():
                    case ";":
                        continue
                    case "]":
                        break
                    case _:
                        raise ValueError("Unexpected token when parsing list")

    return list(gen())


def parse_key_value_pair(pair):
    match = KEY_VALUE_EXPRESSION.fullmatch(pair)
    if not match:
        raise ParseError("Invalid key-value pair", pair)
    reader = Reader(match.group(2))
    try:
        value = parse_nested_list(reader)
        if reader.peek():
            raise ParseError("Extra symbols left in the string")
        return match.group(1), value
    except ValueError as e:
        raise ParseError(
            "Error when parsing",
            reader,
        ) from e


def average_expression(e):
    match e:
        case []:
            return 0
        case list(l):
            return mean(average_expression(part) for part in l)
        case value:
            return value


def parse_arguments(string):
    string = string.strip()
    if not string:
        raise ParseError("There should be at least one argument", string)
    return [parse_key_value_pair(pair) for pair in string.split() if pair]


def dump_arguments(arguments, accuracy: int) -> str:
    return " ".join(f"{arg}={value:.{accuracy}f}" for arg, value in arguments)


def parse_compute_averages(input_arguments: str) -> str:
    arguments = parse_arguments(input_arguments)
    return dump_arguments(
        ((arg, average_expression(e)) for arg, e in arguments), accuracy=2
    )


class TestParsing(unittest.TestCase):
    def test_parse_atom(self):
        self.assertEqual(parse_atom(Reader("12")), 12)
        self.assertEqual(parse_atom(Reader("5.7")), 5.7)
        self.assertEqual(parse_atom(Reader("-4.5555")), -4.5555)
        self.assertEqual(parse_atom(Reader("-0.5678")), -0.5678)
        self.assertTrue(isnan(parse_atom(Reader("NaN"))))

    def test_malformed_atom(self):
        self.assertRaises(ValueError, parse_atom, Reader(".1.2"))
        self.assertRaises(ValueError, parse_atom, Reader("--5"))
        self.assertRaises(ValueError, parse_atom, Reader("6,7"))
        self.assertRaises(ValueError, parse_atom, Reader("nan"))
        self.assertRaises(ValueError, parse_atom, Reader("2NaN"))

    def test_parse_simple_list(self):
        self.assertEqual(parse_nested_list(Reader("[]")), [])
        self.assertEqual(parse_nested_list(Reader("[123]")), [123])
        self.assertEqual(parse_nested_list(Reader("[1.0;2.0;3.0;4.0]")), [1, 2, 3, 4])

    def test_parse_nested_list(self):
        self.assertEqual(parse_nested_list(Reader("[[];[]]")), [[], []])
        self.assertEqual(
            parse_nested_list(Reader("[1.0;[2.0;[3.0]];4.0]")), [1, [2, [3]], 4]
        )

    def test_malformed_nested_list(self):
        def test(expr):
            self.assertRaises(ValueError, parse_nested_list, Reader(expr))

        test("[;-5]")
        test("[[],[]]")
        test("[[][]]")
        test("[4;]")
        test("[NaN5]")

    def test_parse_key_value_pair(self):
        self.assertEqual(parse_key_value_pair("a0=[0]"), ("a0", [0]))
        self.assertEqual(parse_key_value_pair("arg=[0.056]"), ("arg", [0.056]))
        self.assertEqual(parse_key_value_pair("arg36=[[1];NaN]"), ("arg36", [[1], nan]))

    def test_parse_arguments(self):
        self.assertRaises(ParseError, parse_arguments, "")
        self.assertEqual(
            parse_arguments("arg36=[[1]] a=[5.678]"), [("arg36", [[1]]), ("a", [5.678])]
        )

    def test_compute_average_expression(self):
        self.assertEqual(average_expression([]), 0)
        self.assertEqual(average_expression([1, 2, 3]), 2)
        self.assertEqual(average_expression([1, [2, [4]], 2]), 2)
        self.assertTrue(isnan(average_expression([1, [2, [nan]], 2])))
        self.assertEqual(average_expression([1, [2, [4]], [3, [6, [8]]]]), 3)

    def test_dump_arguments(self):
        self.assertEqual(dump_arguments([("arg", 0.056)], accuracy=2), "arg=0.06")
        self.assertEqual(
            dump_arguments([("a", 1), ("b", 0.24)], accuracy=1), "a=1.0 b=0.2"
        )


if __name__ == "__main__":
    unittest.main()
