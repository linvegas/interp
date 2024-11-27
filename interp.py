import io
import sys

class Program:
    count = 0
    lines: list[str]
    vars: dict[str, str] = {}

    def __init__(self, lines: list[str]):
        self.lines = lines

    def eval_expr(self, expr: str) -> int:
        stack = []

        for token in expr.split():
            if token.isdigit(): stack.append(int(token))

            elif token == "+":
                result = 0
                for num in stack: result += num
                stack.clear()
                stack.append(result)

            elif token == "-":
                result = stack[0]
                for i, num in enumerate(stack):
                    if i == 0: continue
                    result -= num
                stack.clear()
                stack.append(result)

            elif token == "*":
                result = 1
                for num in stack: result *= num
                stack.clear()
                stack.append(result)

            elif token == "/":
                result = stack[0]
                for i, num in enumerate(stack):
                    if i == 0: continue
                    result /= num
                stack.clear()
                stack.append(result)

            elif token in self.vars: stack.append(self.vars[token])

            else: print("UNIDENTIFIED TOKEN:", f"'{token}'")

        return stack[0]

    def eval_cond(self, cond: str) -> bool:
        (lhs, operand, rhs) = cond.split()
        match operand:
            case ">": return self.eval_expr(lhs) > self.eval_expr(rhs)
            case _: print(f"UNIDENTIFIED OPERAND: {operand}")

    def eval_stmt(self, stmt: str) -> None:
        # (lhs, rhs) = stmt.split(maxsplit=1)
        lhs = stmt.split()[0]

        match lhs:
            case "print":
                print(self.eval_expr(stmt.split(maxsplit=1)[1].strip()))
                self.count += 1
            case "if":
                if self.eval_cond(stmt.split(maxsplit=1)[1].strip()): self.count += 1
                else:
                    while self.lines[self.count].split()[0] != "end": self.count += 1
                    self.count += 1
            case "end": self.count += 1
            case _:
                expr = stmt.split(maxsplit=1)[1].split("=")[1].strip()
                self.vars[lhs.strip()] = self.eval_expr(expr)
                self.count += 1

    def run(self):
        while self.count < len(self.lines) - 1:
            if self.lines[self.count].strip() != "": self.eval_stmt(self.lines[self.count])
            else: self.count += 1


def main():
    if len(sys.argv) < 2:
        print("USAGE: interp.py <file>")
        exit(1)

    source = io.open(sys.argv[1]).read().split("\n")

    Program(source).run()

if __name__ == "__main__":
    main()
