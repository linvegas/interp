import io
import sys

VARS = {}

def eval_expr(expr: str) -> int:
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

        elif token in VARS: stack.append(VARS[token])

        else: print("UNDENTIFIED TOKEN:", f"'{token}'")

    return stack[0]

def eval_stmt(stmt: str) -> None:
    (lhs, rhs) = stmt.split(maxsplit=1)

    match lhs:
        case "print": print(eval_expr(rhs.strip()))
        case _:
            expr = rhs.split("=")[1].strip()
            VARS[lhs.strip()] = eval_expr(expr)

def main():
    if len(sys.argv) < 2:
        print("USAGE: lang.py <file>")
        exit(1)

    source = io.open(sys.argv[1]).read()

    for line in source.split("\n"):
        if line.strip() != "": eval_stmt(line)

if __name__ == "__main__":
    main()
