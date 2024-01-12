import inspect
import operator
from itertools import pairwise
from math import factorial


class Reader:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def is_end(self):
        return self.pos == len(self.text)

    def read(self):
        if value := self.peek():
            self.pos += 1
        return value

    def peek(self):
        if self.is_end():
            return None
        return self.text[self.pos]


class LoggerContext:
    def __init__(self, logger, context):
        self.logger = logger
        self.context = context

    def __enter__(self):
        self.logger.contexts.append((self.logger.reader.pos, self.context))
        print(self.logger, "enter")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.logger, "exit")
        self.logger.contexts.pop()


class Logger:
    def __init__(self, reader):
        self.contexts = []
        self.reader = reader
        _read = reader.read

        def read():
            print(self, f"[{reader.peek()}]")
            ch = _read()
            return ch

        self.reader.read = read

    def __call__(self, context):
        return LoggerContext(self, context)

    def __str__(self):
        return self.contexts[0][1] + "".join(
            " " * (c[0] - p[0]) + c[1] for p, c in pairwise(self.contexts)
        )


def analyze1(expression):
    data = Reader("(" + expression + ")")
    logger = Logger(reader=data)

    def consume_not():
        with logger("!"):
            negate = False
            while data.peek() == "!":
                assert data.read() == "!"
                negate = not negate
            return negate != consume_brackets()

    def consume_brackets():
        with logger("b"):
            if data.peek() == "(":
                assert data.read() == "("
                value = consume_or()
                assert data.read() == ")"
                return value
            assert data.peek() in "01"
            return data.read() == "1"

    def consume_and():
        with logger("&"):
            value = consume_not()
            while data.peek() == "&":
                assert data.read() == "&"
                value2 = consume_and()
                value = value and value2
            return value

    def consume_or():
        with logger("|"):
            value = consume_and()
            while data.peek() in "|^":
                op = data.read()
                next_value = consume_and()
                value = (value or next_value) if op == "|" else (value != next_value)
            return value

    return int(consume_brackets())


def ascending(seq) -> bool:
    return all(x <= y for x, y in pairwise(seq))


class PostfixConverter:
    def __init__(
        self,
        operator_order: list = None,
        brackets: str = "()[]{}",
        whitespace: str = " ",
    ):
        self.whitespace = whitespace
        self.open_brackets = {
            brackets[i]: brackets[i + 1] for i in range(0, len(brackets), 2)
        }
        self.close_brackets = {
            brackets[i + 1]: brackets[i] for i in range(0, len(brackets), 2)
        }

        operator_order = operator_order or []
        precedence = {}
        for p, ops in enumerate(reversed(operator_order)):
            for op in ops:
                precedence[op] = p
        for op in self.open_brackets:
            precedence[op] = -1
        self.precedence = precedence

    def convert(self, expression) -> list:
        stack = []
        prefix_context = True
        for ch in expression:
            if ch in self.whitespace:
                continue

            if ch in self.open_brackets:
                stack.append(ch)
                prefix_context = True
                continue

            if ch in self.close_brackets:
                if stack and stack[-1] is None:
                    stack.pop()
                while stack[-1] not in self.open_brackets:
                    yield stack.pop()
                if self.open_brackets[stack.pop()] != ch:
                    raise ValueError("Mismatched bracket")
                prefix_context = False
                continue

            if prefix_context:
                yield None

            p = self.precedence.get(ch)
            if p is None:
                yield ch
                prefix_context = False
                continue

            if prefix_context:
                while stack and p < self.precedence[stack[-1]]:
                    yield stack.pop()
            else:
                while stack and p <= self.precedence[stack[-1]]:
                    yield stack.pop()
            stack.append(ch)
            prefix_context = True

        if prefix_context:
            yield None
        yield from stack[::-1]


def eval_postfix(seq, ops: dict):
    stack = []
    try:
        for ch in seq:
            op = ops[ch]
            arity = sum(
                p.default == inspect._empty
                for p in inspect.signature(op).parameters.values()
            )
            if arity:
                stack[-arity:] = [op(*stack[-arity:])]
            else:
                stack.append(op())

        return stack.pop()
    finally:
        pass


#        if stack:
#            raise ValueError("Unexpected values left in stack")


def check_conversions(converter, examples: dict, ops: dict = None):
    for example, expected in examples.items():
        result = "".join(ch or "_" for ch in converter.convert(example))
        assert result == expected, f"Conversion failed for example: {example}"
        if ops:
            value = eval_postfix(converter.convert(example), ops)
            print(example, "=", value)


empty = PostfixConverter()
plus = PostfixConverter(["+"])
boolean = PostfixConverter(["!", "&", "^|"])
arith = PostfixConverter(["!", "*/", "+-"])

DIGITS = {str(n): lambda x, y=n: 10 * x + y for n in range(10)}
DIGITS[None] = lambda: 0

if True:
    check_conversions(
        empty,
        {
            #       "": "",
            "2": "_2",
            " 2  ": "_2",
            " 235 ": "_235",
        },
        ops=DIGITS,
    )

    check_conversions(
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

ALL_OPS = {
    **DIGITS,
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "**": operator.pow,
    "<<": operator.lshift,
    ">>": operator.rshift,
    "&": operator.and_,
    "|": operator.or_,
    "^": operator.xor,
    "~": operator.invert,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "!": lambda x, y: factorial(x) if x else (1 - y),
}

check_conversions(
    boolean,
    {
        # "1|0": "_1_0|",
        # "!0": "__0!",
        # "1|!0": "_1__0!|",
        "1|0|1": "_1_0|_1|",
        "1|!0|!1": "_1__0!|__1!|",
        "1|!!0": "_1___0!!|",
        " 1 & 0 | 1 & 1 ": "_1_0&_1_1&|",
        " !1 & 0 | !1 & !!0 ": "__1!_0&__1!___0!!&|",
        " 1 & (0 | 1) & 1 ": "_1_0_1|&_1&",
    },
    ALL_OPS,
)

check_conversions(
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


def analyze2(expression):
    return eval_postfix(arith.convert(expression), ALL_OPS)


if __name__ == "__main__":
    while e := input():
        print(analyze2(e))
