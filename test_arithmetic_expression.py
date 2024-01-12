import unittest
from arithmetic_expression import *


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.reader = Reader("example_input")

    def test_is_end(self):
        for _ in range(13):
            self.reader.read()
        self.assertTrue(self.reader.is_end())

    def test_read_and_peek(self):
        for letter in ["e", "x", "a", "m", "p", "l", "e", "_", "i", "n", "p", "u", "t"]:
            self.assertEqual(self.reader.peek(), letter)
            self.assertEqual(self.reader.read(), letter)

    def tearDown(self):
        self.reader = None


class LoggerTests(unittest.TestCase):
    def setUp(self):
        reader = Reader("example_input")
        self.logger = Logger(reader=reader)

    def test_call(self):
        with self.logger("test"):
            self.assertIn((0, "test"), self.logger.contexts)

    def tearDown(self):
        self.logger = None


class Analyze1Tests(unittest.TestCase):
    def test_analyze1(self):
        self.assertEqual(analyze1("1&!0|!!!1"), 1)
        self.assertEqual(analyze1("1&0|!1&1"), 0)


class PostfixConverterTests(unittest.TestCase):
    def check_conversions(
        self, converter: PostfixConverter, examples: dict, ops: dict = None
    ):
        for example, expected in examples.items():
            result = "".join(ch or "_" for ch in converter.convert(example))
            self.assertEqual(
                result, expected, f"Conversion failed for example: {example}"
            )
            if ops:
                value = eval_postfix(converter.convert(example), ops)
                try:
                    true_value = eval(example)
                    self.assertEqual(value, true_value)
                except:
                    pass

    def test_empty(self):
        empty = PostfixConverter()
        self.check_conversions(
            empty,
            {
                #       "": "", -- not a valid expression
                "2": "_2",
                " 2  ": "_2",
                " 235 ": "_235",
            },
            ops=DIGITS,
        )

    def test_plus(self):
        plus = PostfixConverter(["+"])
        self.check_conversions(
            plus,
            {
                "+5": "__5+",
                "3+5": "_3_5+",
                "2 + 34 + 5": "_2_34+_5+",
            },
            ops={
                **DIGITS,
                "+": operator.add,
            },
        )

    def test_boolean(self):
        boolean = PostfixConverter(["!", "&", "^|"])
        self.check_conversions(
            boolean,
            {
                "1|0": "_1_0|",
                "!0": "__0!",
                "1|!0": "_1__0!|",
                "1|0|1": "_1_0|_1|",
                "1|!0|!1": "_1__0!|__1!|",
                "1|!!0": "_1___0!!|",
                " 1 & 0 | 1 & 1 ": "_1_0&_1_1&|",
                " !1 & 0 | !1 & !!0 ": "__1!_0&__1!___0!!&|",
                " 1 & (0 | 1) & 1 ": "_1_0_1|&_1&",
            },
            ALL_OPS,
        )

    def test_arithmetics(self):
        arith = PostfixConverter(["!", "*/", "+-"])
        self.check_conversions(
            arith,
            {
                "+5": "__5+",
                "3+5": "_3_5+",
                "3!": "_3_!",
                "!0": "__0!",
                "3! + !0": "_3_!__0!+",
                "2 + 34 + -5": "_2_34+__5-+",
                "2 - 3 + 4 - 5 + 6 * 7": "_2_3-_4+_5-_6_7*+",
            },
            ALL_OPS,
        )

    def test_unary(self):
        arith = PostfixConverter(["!", "*/", "+-"], unary="!+-")
        self.check_conversions(
            arith,
            {
                "4/-2": "_4__2-/",
                "--2": "___2--",
                "2 - -1": "_2__1--",
            },
            ALL_OPS,
        )

    def test_brackets(self):
        arith = PostfixConverter(["!", "*/", "+-"])
        self.check_conversions(
            arith,
            {
                "1 * 2 - 3 * 4 / 2 + 5": "_1_2*_3_4*_2/-_5+",
                "1 * (2 - 3) * 4 / 2 + 5": "_1_2_3-*_4*_2/_5+",
                "({1 * 2} - [(3 * 4) / 2] + 5)": "_1_2*_3_4*_2/-_5+",
                "((1 * 2) - 3 * (4 / 2 + 5))": "_1_2*_3_4_2/_5+*-",
            },
            ALL_OPS,
        )


class Analyze2Tests(unittest.TestCase):
    def test_analyze2(self):
        self.assertEqual(analyze2("2+34+-5"), 31)
        self.assertEqual(analyze2("2-3+4-5+6*7"), 40)


if __name__ == "__main__":
    unittest.main()
