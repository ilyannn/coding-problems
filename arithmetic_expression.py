import inspect
import operator
from itertools import pairwise
from math import factorial


## METHOD 1


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


## METHOD 2


class PostfixConverter:
    def __init__(
        self,
        operator_order: list = None,
        brackets: str = "()[]{}",
        whitespace: str = " ",
        unary: str = "",
    ):
        self.whitespace = whitespace
        self.open = {brackets[i]: brackets[i + 1] for i in range(0, len(brackets), 2)}
        self.close = {brackets[i + 1]: brackets[i] for i in range(0, len(brackets), 2)}
        
        operator_order = operator_order or []
        precedence = {}
        for p, ops in enumerate(reversed(operator_order)):
            for op in ops:
                precedence[op] = p
        for op in self.open:
            precedence[op] = -1
        self.precedence = precedence
        self.precedence_unary = {u: len(operator_order) for u in unary}

    def convert(self, expression) -> list:
        stack = []
        prefix_context = True
        for ch in expression:
            if ch in self.whitespace:
                continue

            if ch in self.open:
                stack.append(ch)
                prefix_context = True
                continue

            if ch in self.close:
                if stack and stack[-1] is None:
                    stack.pop()
                while stack[-1] not in self.open:
                    yield stack.pop()
                if self.open[stack.pop()] != ch:
                    raise ValueError("Mismatched bracket")
                prefix_context = False
                continue

            if prefix_context:
                yield None

            if prefix_context and ch in self.precedence_unary:
                p = self.precedence_unary[ch]
            elif ch in self.precedence:
                p = self.precedence[ch]
            else: 
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
                p.default == inspect.Parameter.empty
                for p in inspect.signature(op).parameters.values()
            )
            if arity:
                stack[-arity:] = [op(*stack[-arity:])]
            else:
                stack.append(op())

        return stack.pop()
    finally:
        if stack:
            raise ValueError("Unexpected values left in stack")


DIGITS = {str(n): lambda x, y=n: 10 * x + y for n in range(10)}
DIGITS[None] = lambda: 0

ALL_OPS = {
    **DIGITS,
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "&": operator.and_,
    "|": operator.or_,
    "^": operator.xor,
    "~": operator.invert,
    "!": lambda x, y: factorial(x) if x else (1 - y),
}


def analyze2(expression):
    arithmetics = PostfixConverter(["!", "*/&|%", "+-"])
    return eval_postfix(arithmetics.convert(expression), ALL_OPS)


if __name__ == "__main__":
    while e := input():
        print(analyze2(e))
